from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'scripts'))
sys.path.insert(0,str(REPO/'examples/phase-2'))
import design_workspace as workspace
import phase2
from build_example import populate
from render_design_specimens import SHEETS, Tokens, render, validate_config, validate_svg


class Phase2Test(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.directory=workspace.init_workspace(str(self.root),'Margin','guided',['web'],'390 × 844')
        self.cli('select','--primary','Synthetic editorial reference|overall grammar','--avoid','Decorative gradients','--do-not-copy','Original identity')
        self.cli('phase2','start')
        self.standard=populate(self.directory)

    def tearDown(self):
        self.temp.cleanup()

    def cli(self,*args,ok=True):
        result=subprocess.run([sys.executable,str(REPO/'scripts/design_workspace.py'),*args,'--root',str(self.root)],capture_output=True,text=True)
        if ok: self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        else: self.assertNotEqual(result.returncode,0,result.stdout)
        return result

    def load(self,name): return json.loads((self.standard/name).read_text())
    def save(self,name,data): (self.standard/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    def errors(self):
        _,project,refs,_=workspace.load_workspace(str(self.root))
        return phase2.validate(self.directory,project,refs,'v1')

    def test_init_scaffolds_manual_and_single_dna_source(self):
        with tempfile.TemporaryDirectory() as temp:
            d=workspace.init_workspace(temp,'Watch reading','guided',['watchos'],'Small watch')
            for name in [*phase2.DOCS,'TOKENS.json','SPECIMENS.json','REVIEW.json']:
                self.assertTrue((d/'standards/v1'/name).is_file(),name)
            self.assertTrue((d/'visual-dna.md').is_symlink())
            self.assertEqual((d/'visual-dna.md').resolve(),d/'standards/v1/VISUAL_DNA.md')
            spec=json.loads((d/'standards/v1/SPECIMENS.json').read_text())
            self.assertEqual(spec['components'],[]) # Never seed desktop tables into a watch app.
            self.assertEqual(spec['patterns'],[])

    def test_guided_cannot_start_before_gate_a(self):
        project=workspace.read_json(self.directory/'project.json');project['approval_state']['gate_a']='pending';workspace.atomic_json(self.directory/'project.json',project)
        self.cli('phase2','start',ok=False);self.cli('phase2','render',ok=False)
        self.cli('status','--require','decompose',ok=False)

    def test_direct_is_not_a_design_thinking_bypass(self):
        with tempfile.TemporaryDirectory() as temp:
            d=workspace.init_workspace(temp,'Direct','direct',['web'],None)
            project=workspace.read_json(d/'project.json')
            self.assertEqual(project['approval_state']['gate_b'],'draft')
            result=subprocess.run([sys.executable,str(REPO/'scripts/design_workspace.py'),'status','--root',temp,'--require','implement'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(json.loads(result.stdout)['can_implement'])
        project=workspace.read_json(self.directory/'project.json');project['mode']='direct';project['approval_state']['gate_a']='assumed';workspace.atomic_json(self.directory/'project.json',project)
        (self.standard/'DESIGN_STRATEGY.md').unlink()
        self.cli('approve','--gate','b',ok=False)
        populate(self.directory)
        self.cli('approve','--gate','b')
        result=json.loads(self.cli('status','--require','implement').stdout)
        self.assertEqual(result['gates']['gate_b'],'assumed')

    def test_positive_fixture_validates_and_locks(self):
        self.assertEqual(self.errors(),[])
        self.cli('approve','--gate','b')
        self.cli('status','--require','implement')
        self.assertTrue((self.standard/'LOCK.json').is_file())
        self.cli('approve','--gate','b') # Idempotent.
        self.cli('approve','--gate','c','--platform-qa','web',ok=False) # QA is still required.

    def test_each_required_manual_file_is_enforced(self):
        for name in phase2.DOCS:
            with self.subTest(name=name):
                path=self.standard/name;data=path.read_bytes();path.unlink()
                self.assertTrue(any(name in error for error in self.errors()),name)
                path.write_bytes(data)
        for name in ('TOKENS.json','SPECIMENS.json','REVIEW.json'):
            with self.subTest(name=name):
                path=self.standard/name;data=path.read_bytes();path.unlink()
                self.assertTrue(self.errors());path.write_bytes(data)

    def test_each_visual_sheet_is_enforced(self):
        for name in SHEETS:
            with self.subTest(name=name):
                path=self.standard/'evidence'/(name+'.svg');data=path.read_bytes();path.unlink()
                self.assertTrue(any(name in error for error in self.errors()))
                path.write_bytes(data)
        (self.standard/'evidence/representative-screen.svg').unlink()
        self.cli('approve','--gate','b',ok=False)

    def test_dna_count_uniqueness_and_placeholder_rejection(self):
        path=self.standard/'VISUAL_DNA.md';original=path.read_text()
        for body in ('\n'.join(f'{i}. TODO' for i in range(1,7)),
                     '\n'.join(f'{i}. A repeated principle with sufficient text but identical observable behavior.' for i in range(1,7)),
                     '\n'.join(f'{i}. Distinct principle {i} with visible focus and an observable failure condition.' for i in range(1,10)),
                     '1. One principle cannot describe the entire observable identity of a product.'):
            with self.subTest(body=body[:50]):
                path.write_text('# DNA\n\n## Principles\n'+body+'\n\n## Key-screen Visual Gestures\nA title leads with appropriate whitespace.\n\n## Approval\nApproval is recorded with a validated version lock.')
                self.assertTrue(any('5–8' in error for error in self.errors()))
        path.write_text(original)
        review=self.load('REVIEW.json');review['dna'][0]['failure']='';self.save('REVIEW.json',review)
        self.assertTrue(any('failure' in error for error in self.errors()))

    def test_scaffold_and_empty_sections_cannot_pass(self):
        for name,body in [('DESIGN_STRATEGY.md',(phase2.TEMPLATES/'design-strategy.md').read_text()),('COLOR.md','# Color\n\n## Base Palette\nTODO'),('MASTER.md','# Master\n\nLooks premium and modern.')]:
            with self.subTest(name=name):
                path=self.standard/name;original=path.read_text();path.write_text(body)
                self.assertTrue(any(name in error for error in self.errors()));path.write_text(original)

    def test_deep_analysis_requires_reasoning_chain(self):
        p=self.standard/'REFERENCE_ANALYSIS.md';p.write_text(p.read_text().replace('WHY —','Rationale —',1))
        self.assertTrue(any('WHAT' in error for error in self.errors()))

    def test_secondary_boundary_and_contract_integrity(self):
        self.cli('select','--primary','Synthetic editorial reference|overall grammar','--secondary','Second reference|photography crop only','--avoid','Decorative gradients','--do-not-copy','Original identity')
        self.cli('phase2','start');populate(self.directory)
        review=self.load('REVIEW.json');review['influence'][1].update(source='secondary:1',contribution='brand color palette')
        self.save('REVIEW.json',review)
        self.assertTrue(any('exceeds' in error for error in self.errors()))
        review['influence'][1]['decision']='rejected';self.save('REVIEW.json',review)
        self.assertFalse(any('exceeds' in error for error in self.errors()))
        (self.directory/'REFERENCE_CONTRACT.md').write_text('# A different contract')
        self.assertTrue(any('contract' in error.lower() for error in self.errors()))

    def test_unbounded_secondary_and_third_reference_fail(self):
        self.cli('select','--primary','R1|grammar','--secondary','R2',ok=False)
        self.cli('select','--primary','R1|grammar','--secondary','R2|crop','--secondary','R3|type','--secondary','R4|color',ok=False)

    def test_stale_tokens_or_altered_svgs_fail(self):
        tokens=self.load('TOKENS.json');tokens['radius']['control']=7;self.save('TOKENS.json',tokens)
        self.assertTrue(any('Stale render input' in error for error in self.errors()))
        render(self.standard)
        p=self.standard/'evidence/layout-atlas.svg';p.write_text(p.read_text().replace('Hero Decision','Wrong composition'))
        self.assertTrue(any('altered' in error for error in self.errors()))

    def test_rerender_does_not_silently_reapprove_old_review(self):
        tokens=self.load('TOKENS.json');tokens['radius']['control']=7;self.save('TOKENS.json',tokens)
        render(self.standard)
        self.assertTrue(any('review is stale' in error for error in self.errors()))
        self.cli('phase2','review','--reviewed-by','Fixture reviewer after checking updated corner role')
        self.assertEqual(self.errors(),[])

    def test_unknown_tokens_and_alias_cycles_fail(self):
        spec=self.load('SPECIMENS.json');spec['components'][0]['states'][0]['bg']='{color.missing}'
        with self.assertRaisesRegex(ValueError,'Missing token'):
            validate_config(Tokens(self.load('TOKENS.json')),spec,self.standard)
        tokens=Tokens({'a':'{b}','b':'{a}'})
        with self.assertRaisesRegex(ValueError,'Cyclic'):
            tokens.resolve('{a}')

    def test_specimen_values_cannot_duplicate_tokens(self):
        spec=self.load('SPECIMENS.json');spec['components'][0]['states'][0]['radius']=16
        with self.assertRaisesRegex(ValueError,'token reference'):
            validate_config(Tokens(self.load('TOKENS.json')),spec,self.standard)

    def test_missing_states_and_localized_samples_fail(self):
        spec=self.load('SPECIMENS.json');spec['components'][0]['states']=spec['components'][0]['states'][:1]
        with self.assertRaisesRegex(ValueError,'missing states'):
            validate_config(Tokens(self.load('TOKENS.json')),spec,self.standard)
        spec=self.load('SPECIMENS.json')
        for role in spec['typography']:role['sample']='Only English labels'
        with self.assertRaisesRegex(ValueError,'Chinese'):
            validate_config(Tokens(self.load('TOKENS.json')),spec,self.standard)

    def test_reasoned_scope_exclusions_still_generate_sheets(self):
        spec=self.load('SPECIMENS.json');spec['icons']=[];spec['icons_omission']='Text-only reading surface has no icon actions in this scoped demonstration.'
        self.save('SPECIMENS.json',spec);render(self.standard)
        text=(self.standard/'evidence/icon-style-sheet.svg').read_text()
        self.assertIn('Text-only',text)
        self.assertTrue(validate_svg(self.standard/'evidence/icon-style-sheet.svg'))
        review=self.load('REVIEW.json');review['exceptions'].append({'category':'manual-file','item':'COLOR.md'})
        self.save('REVIEW.json',review)
        self.assertTrue(any('exception' in error.lower() for error in self.errors()))

    def test_contrast_failures_are_gate_failures(self):
        tokens=self.load('TOKENS.json');tokens['color']['semantic']['text']=tokens['color']['semantic']['canvas'];self.save('TOKENS.json',tokens);render(self.standard)
        self.assertTrue(any('contrast failure' in error for error in self.errors()))

    def test_fake_images_and_malformed_svg_fail(self):
        for name,content in [('fake.png',b'rendered-evidence'),('fake.jpg',b'not an image'),('fake.md',b'# Screen'),('fake.svg',b'<svg/>')]:
            p=self.root/name;p.write_bytes(content)
            with self.subTest(name=name),self.assertRaises(ValueError):phase2.validate_image(p)
        p=self.root/'empty.svg';p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400"><rect width="400" height="400"/></svg>')
        with self.assertRaises(ValueError): validate_svg(p)

    def test_coherence_checks_and_representative_mapping_fail(self):
        review=self.load('REVIEW.json');review['checks']['smallest_target']['pass']=False;review['representative']['pattern']='invented-pattern';self.save('REVIEW.json',review)
        errors=self.errors();self.assertTrue(any('smallest_target' in e for e in errors));self.assertTrue(any('layout pattern' in e for e in errors))

    def test_negative_approval_does_not_mutate_workspace(self):
        before={str(p.relative_to(self.directory)):p.read_bytes() for p in self.directory.rglob('*') if p.is_file()}
        self.cli('approve','--gate','b','--representative-screen',str(REPO/'README.md'),ok=False)
        after={str(p.relative_to(self.directory)):p.read_bytes() for p in self.directory.rglob('*') if p.is_file()}
        self.assertEqual(before,after)

    def test_locked_mutation_blocks_implementation_and_gate_c(self):
        self.cli('approve','--gate','b')
        p=self.standard/'COLOR.md';p.write_text(p.read_text()+'\nUnreviewed global palette change.\n')
        self.cli('status','--require','implement',ok=False)
        self.cli('approve','--gate','c','--platform-qa','web',ok=False)
        self.cli('approve','--gate','b',ok=False)
        self.cli('phase2','render',ok=False)

    def test_upgrade_preserves_source_and_old_commands(self):
        self.cli('approve','--gate','b');old=(self.standard/'TOKENS.json').read_bytes()
        self.cli('phase2','upgrade','--version','v2')
        self.assertEqual((self.standard/'TOKENS.json').read_bytes(),old)
        self.assertTrue((self.standard/'LOCK.json').is_file())
        self.assertFalse((self.directory/'standards/v2/LOCK.json').exists())
        self.assertEqual((self.directory/'visual-dna.md').resolve(),self.directory/'standards/v2/VISUAL_DNA.md')
        self.cli('status','--require','implement',ok=False)
        self.cli('history')
        self.cli('phase2','start','--version','../escape',ok=False)

    def test_legacy_v2_upgrade_preserves_authored_dna_and_spacing(self):
        alias=self.directory/'visual-dna.md';original=alias.read_text();alias.unlink();alias.write_text(original)
        (self.standard/'SPACING.md').write_text('# Authored legacy spacing\nKeep the custom original relationships.')
        project=workspace.read_json(self.directory/'project.json');project['schema_version']=2;project['approval_state']['gate_b']='confirmed';project.pop('phase2_locks',None);workspace.atomic_json(self.directory/'project.json',project)
        self.cli('status','--require','implement',ok=False)
        self.cli('phase2','upgrade','--version','v2')
        self.assertEqual((self.directory/'history/visual-dna-before-phase2.md').read_text(),original)
        self.assertIn('Authored legacy spacing',(self.standard/'SPACING.md').read_text())

    def test_render_is_deterministic_valid_and_not_empty(self):
        first=render(self.standard);second=render(self.standard);self.assertEqual(first,second)
        for name in SHEETS:
            path=self.standard/'evidence'/(name+'.svg');self.assertGreater(path.stat().st_size,500)
            dims=validate_svg(path);self.assertEqual(dims['width'],1120)
            self.assertGreater(dims['height'],100)
        self.assertRegex((self.standard/'evidence/typography-specimen.svg').read_text(),r'[\u3400-\u9fff]')
        self.assertIn('selected',(self.standard/'evidence/icon-style-sheet.svg').read_text())

    def test_real_content_overflow_is_not_silently_clipped(self):
        spec=self.load('SPECIMENS.json');spec['components'][0]['states'][0]['label']='不能塞入控件的真实内容'*30;self.save('SPECIMENS.json',spec)
        before=(self.standard/'evidence/component-specimen.svg').read_bytes()
        with self.assertRaisesRegex(ValueError,'does not fit'):render(self.standard)
        self.assertEqual(before,(self.standard/'evidence/component-specimen.svg').read_bytes())

    def test_raster_imagery_and_xml_escaping(self):
        import struct,zlib
        def chunk(kind,body):
            return struct.pack('>I',len(body))+kind+body+struct.pack('>I',zlib.crc32(kind+body)&0xffffffff)
        raster=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,64,8,2,0,0,0))+chunk(b'IDAT',zlib.compress((b'\x00'+b'\x80\x90\xa0'*64)*64))+chunk(b'IEND',b'')
        image=self.standard/'evidence/test-image.png';image.write_bytes(raster)
        self.assertEqual(phase2.validate_image(image)['width'],64)
        spec=self.load('SPECIMENS.json');spec['imagery']={'mode':'image','file':'evidence/test-image.png','caption':'Synthetic raster used solely for renderer integration testing'}
        spec['title']='A & B <reading>';self.save('SPECIMENS.json',spec)
        manifest=render(self.standard)
        self.assertIn('evidence/test-image.png',manifest['inputs'])
        svg=ET.parse(self.standard/'evidence/style-tile.svg')
        self.assertTrue(any(e.tag.endswith('}image') for e in svg.iter()))
        self.assertIn('A & B <reading>',''.join(svg.getroot().itertext()))

    def test_cli_help_and_force_init_backup(self):
        for command in ('init','status','select','approve','score','audit','override','history','migrate','phase2'):
            result=subprocess.run([sys.executable,str(REPO/'scripts/design_workspace.py'),command,'--help'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
        self.cli('init','--project','New draft','--platform','watchos','--force')
        backups=list(self.root.glob('.design-director-backup-*'));self.assertEqual(len(backups),1)
        self.assertTrue((backups[0]/'standards/v1/DESIGN_STRATEGY.md').exists())


if __name__=='__main__':unittest.main()
