"""Phase 2 scaffolding, completeness validation and immutable design-lock checks."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import struct
import zlib
from pathlib import Path

from render_design_specimens import (SHEETS, Tokens, contrast, digest, local_file,
                                    nonempty, read_json, validate_config, validate_svg)

TEMPLATES = Path(__file__).resolve().parents[1]/'assets/templates/phase-2'
DOCS = {
    'MASTER.md':'master', 'DESIGN_STRATEGY.md':'design-strategy', 'VISUAL_DNA.md':'visual-dna',
    'COLOR.md':'color', 'TYPOGRAPHY.md':'typography', 'LAYOUT.md':'layout',
    'SPACING_GEOMETRY.md':'spacing-geometry', 'COMPONENTS.md':'components',
    'ICONOGRAPHY.md':'iconography', 'IMAGERY.md':'imagery', 'MOTION.md':'motion',
    'RESPONSIVE.md':'responsive', 'PAGE_PATTERNS.md':'page-patterns', 'DO_DONT.md':'do-dont',
    'REFERENCE_ANALYSIS.md':'reference-analysis', 'DESIGN_JUDGMENT.md':'design-judgment',
    'REFERENCE_INFLUENCE.md':'reference-influence',
}
CHECKS = ('color','typography','layout','geometry','components','icons','imagery','motion',
          'reference_boundary','rejected_traits','decorative_dependency','content_fit','smallest_target',
          'component_token_match','representative_manual_match')
PROVENANCE = {'Product Need', 'User Need', 'Primary Reference', 'Approved Secondary Contribution',
              'Platform Constraint', 'Accessibility Requirement', 'Explicit Proposed Decision'}
PLACEHOLDER = re.compile(r'\{\{|\}\}|\b(?:TODO|TBD|FIXME|lorem ipsum|placeholder principle|observable principle \d)\b|<!--\s*scaffold:',re.I)


def standard_path(directory, version):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', version) or version == 'current':
        raise ValueError('Version must be a simple directory name, e.g. v1 or v2')
    path = directory/'standards'/version
    if not path.resolve().is_relative_to((directory/'standards').resolve()):
        raise ValueError('Version path escapes standards')
    return path


def seed(standard, project):
    standard.mkdir(parents=True,exist_ok=True)
    for destination, template in DOCS.items():
        path = standard/destination
        if not path.exists():
            path.write_text((TEMPLATES/(template+'.md')).read_text().replace('{{PROJECT_NAME}}',project),encoding='utf-8')
    for name in ('TOKENS','SPECIMENS','REVIEW'):
        path = standard/(name+'.json')
        if not path.exists():
            path.write_text((TEMPLATES/(name.lower()+'.json')).read_text().replace('{{PROJECT_NAME}}',project),encoding='utf-8')
    for name in ('evidence','PLATFORM_OVERRIDES','PAGE_OVERRIDES'):
        (standard/name).mkdir(exist_ok=True)
    if not (standard/'SPACING.md').exists():
        (standard/'SPACING.md').write_text('# Spacing compatibility entry\n\nSee [SPACING_GEOMETRY.md](SPACING_GEOMETRY.md), the canonical spacing and geometry rules.\n')


def alias_dna(directory, version, preserve=False):
    alias = directory/'visual-dna.md'
    if alias.is_file() and not alias.is_symlink():
        if not preserve:
            raise ValueError('Legacy visual-dna.md requires phase2 upgrade; refusing to overwrite it')
        target = directory/'history'/'visual-dna-before-phase2.md'
        if not target.exists():
            shutil.copy2(alias,target)
    if alias.exists() or alias.is_symlink():
        alias.unlink()
    alias.symlink_to(Path('standards')/version/'VISUAL_DNA.md')


def sections(text):
    result = {}; current = None
    for line in text.splitlines():
        if line.startswith('## '):
            current = line[3:].strip(); result[current] = []
        elif current is not None:
            result[current].append(line)
    return {key:'\n'.join(value).strip() for key,value in result.items()}


def substantive(text):
    # Ignore structural Markdown and empty table rows, but preserve Chinese prose.
    plain = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    plain = re.sub(r'[#|*_`>\s:;\-–—]+','',plain)
    return len(plain) >= 18 and not PLACEHOLDER.search(text)


def principles(path):
    if not path.is_file():
        return []
    text = path.read_text(encoding='utf-8')
    body = sections(text).get('Principles', text)
    values = re.findall(r'^\s*\d+\.\s+(.+)$',body,re.M)
    return [v.strip() for v in values if substantive(v)]


def reference_errors(directory, project, refs):
    errors = []
    gate = project.get('approval_state',{}).get('gate_a')
    if gate != 'confirmed' and not (project.get('mode') == 'direct' and gate == 'assumed'):
        errors.append('Gate A is not confirmed (Direct still requires a recorded assumed reference lock)')
    primary = refs.get('primary')
    if not isinstance(primary,dict) or not primary.get('reference') or primary.get('contribution') in (None,'','unspecified'):
        errors.append('Primary Reference and its contribution must be recorded')
    secondary = refs.get('secondary',[])
    if not isinstance(secondary,list) or len(secondary)>2:
        errors.append('At most two Secondary References are allowed'); secondary=[]
    for index, source in enumerate(secondary,1):
        if not isinstance(source,dict) or not source.get('reference') or source.get('contribution') in (None,'','unspecified','legacy unspecified'):
            errors.append(f'Secondary {index} requires an explicit bounded contribution')
    for key in ('selected_traits','rejected_traits','do_not_copy'):
        if not isinstance(refs.get(key),list):
            errors.append(f'Reference contract must explicitly record {key}')
    contract = directory/'REFERENCE_CONTRACT.md'
    if not contract.is_file() or PLACEHOLDER.search(contract.read_text(encoding='utf-8')):
        errors.append('REFERENCE_CONTRACT.md is missing or unfinished')
    elif primary:
        text = contract.read_text(encoding='utf-8')
        for source in [primary,*secondary]:
            if isinstance(source,dict) and any(str(source.get(key,'')) not in text for key in ('reference','contribution')):
                errors.append('REFERENCE_CONTRACT.md and references.json disagree on source/contribution')
        for key in ('selected_traits','rejected_traits','do_not_copy'):
            if isinstance(refs.get(key),list) and any(str(value) not in text for value in refs[key]):
                errors.append(f'REFERENCE_CONTRACT.md does not preserve {key}')
    return errors


def validate_image(path):
    if path.suffix.lower()=='.svg':
        return validate_svg(path)
    data = path.read_bytes()
    if path.suffix.lower()=='.png':
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('Representative PNG has invalid signature')
        offset=8; chunks=[]; compressed=b''; size=None
        while offset+12<=len(data):
            length=struct.unpack('>I',data[offset:offset+4])[0]
            kind=data[offset+4:offset+8]; body=data[offset+8:offset+8+length]
            if offset+12+length>len(data):
                raise ValueError('Truncated PNG')
            crc=struct.unpack('>I',data[offset+8+length:offset+12+length])[0]
            if zlib.crc32(kind+body)&0xffffffff != crc:
                raise ValueError('PNG CRC mismatch')
            chunks.append(kind)
            if kind==b'IHDR':
                if length!=13:
                    raise ValueError('Invalid PNG IHDR')
                size=struct.unpack('>II',body[:8])
            if kind==b'IDAT': compressed+=body
            offset+=12+length
            if kind==b'IEND': break
        if not size or not all(64<=value<=16384 for value in size) or b'IEND' not in chunks or not compressed:
            raise ValueError('Representative PNG must be a complete image at a meaningful screen size')
        decoder=zlib.decompressobj()
        decoded=decoder.decompress(compressed,256*1024*1024)
        if not decoded or not decoder.eof:
            raise ValueError('PNG raster stream is incomplete or excessively large')
        return {'width':size[0],'height':size[1]}
    if path.suffix.lower() in ('.jpg','.jpeg'):
        # Check JPEG frame dimensions and terminal markers without an imaging dependency.
        if not data.startswith(b'\xff\xd8') or not data.endswith(b'\xff\xd9'):
            raise ValueError('Representative JPEG has invalid signature/end marker')
        for match in re.finditer(b'\xff[\xc0-\xc3\xc5-\xc7\xc9-\xcb\xcd-\xcf]',data):
            start=match.end()
            if start+7<=len(data):
                h,w=struct.unpack('>HH',data[start+3:start+7])
                if 64<=w<=16384 and 64<=h<=16384:
                    return {'width':w,'height':h}
        raise ValueError('Representative JPEG lacks a valid frame')
    raise ValueError('Representative evidence must be actual SVG, PNG or JPEG, not text renamed as an image')


def review_errors(standard, directory, project, refs, review, spec, dna, review_seal=True):
    errors=[]
    try:
        if review.get('status')!='ready': errors.append('REVIEW.json must be ready after actual coherence review')
        if review.get('reference_contract_sha256')!=digest(directory/'REFERENCE_CONTRACT.md'):
            errors.append('Review must load the current REFERENCE_CONTRACT.md (run phase2 start before analysis)')
        context=review['context']
        for key in ('product','users','task','content','device','smallest_target'):
            nonempty(context[key], 'context.'+key)
        if set(context['platforms'])!=set(project['target_platforms']):
            errors.append('Review platform context must match project targets')
        nonempty(review['reviewed_by'],'reviewed_by')
        if review_seal and review.get('reviewed_inputs') != review_inputs(standard):
            errors.append('Coherence review is stale or unsealed; inspect current outputs and run phase2 review')
        for inventory,category in (('components','component'),('icons','icon')):
            if not spec[inventory] and not any(item.get('category')==category for item in review.get('exceptions',[])):
                errors.append(f'{inventory} omission requires a matching bounded review exception')
        for key in CHECKS:
            check=review['checks'][key]
            if check.get('pass') is not True or not substantive(check.get('reason','')):
                errors.append(f'Coherence check incomplete or failed: {key}')
            evidence=nonempty(check['evidence'],'check evidence')
            path=local_file(standard,evidence.split('#',1)[0])
            if not path.stat().st_size: errors.append(f'Empty review evidence: {evidence}')
        records=review['dna']
        if not isinstance(records,list) or len(records)!=len(dna):
            errors.append('Every DNA principle needs a matching review record')
        else:
            expected=[f'DNA-{i}' for i in range(1,len(dna)+1)]
            if [r.get('id') for r in records]!=expected: errors.append('DNA review IDs must match numbered principles in order')
            for record in records:
                for key in ('source','pass','failure','strategy_rule'):
                    if not substantive(record.get(key,'')): errors.append(f'{record.get("id")}: substantive {key} is required')
        influence=review['influence']
        if not isinstance(influence,list) or not influence:
            errors.append('REFERENCE INFLUENCE MAP review index is required')
        else:
            for row in influence:
                for key in ('dimension','source','contribution','rationale','judgment'):
                    nonempty(row[key],'influence.'+key)
                if row['decision'] not in ('allowed','adapted','rejected'):
                    errors.append('Invalid influence decision')
                source=row['source']
                if source=='primary': approved=refs['primary']['contribution']
                elif source.startswith('secondary:'):
                    index=int(source.split(':')[1])-1
                    if not 0<=index<len(refs['secondary']): raise ValueError('Unknown secondary influence source')
                    approved=refs['secondary'][index]['contribution']
                elif source=='proposed': approved=row['contribution']
                else: raise ValueError('Influence source must identify primary, secondary:N or proposed')
                if row['decision']!='rejected' and row['contribution']!=approved:
                    errors.append(f'{source} influence exceeds its contracted contribution')
                judgment=(standard/'DESIGN_JUDGMENT.md').read_text()
                if row['judgment'] not in judgment: errors.append('Influence judgment ID missing in DESIGN_JUDGMENT.md')
        for exception in review['exceptions']:
            if exception['category'] not in ('component','motion','icon','imagery'):
                errors.append('Exceptions are bounded inventory/behavior decisions, never missing required files')
            for key in ('item','scope','reason','alternative'):
                if not substantive(exception.get(key,'')): errors.append('Bounded exception needs item, scope, reason and alternative')
        rep=review['representative']
        path=local_file(standard,rep['file'])
        if path.parent!=standard.resolve()/'evidence' or not path.name.startswith('representative-screen.'):
            errors.append('Representative screen must be evidence/representative-screen.<image extension>')
        validate_image(path)
        if rep['pattern'] not in {p['id'] for p in spec['patterns']}:
            errors.append('Representative screen must use a configured layout pattern')
        if not isinstance(rep['components'],list) or not set(rep['components']) <= {c['id'] for c in spec['components']}:
            errors.append('Representative screen references unknown components')
        if spec['components'] and not rep['components']: errors.append('Representative component mapping is missing')
        if not rep['dna_ids'] or not set(rep['dna_ids']) <= {r['id'] for r in records}:
            errors.append('Representative screen must map to valid DNA IDs')
        for key in ('viewport','rationale','strategy_rule'):
            nonempty(rep[key],'representative.'+key)
        for item in spec['components']:
            if any(p in project['target_platforms'] for p in ('web','windows')) and item['kind'] in ('button','input','tabs','navigation','chip'):
                states={s['name'] for s in item['states']}
                if 'focus' not in states:
                    errors.append(f'{item["id"]}: keyboard platform requires focus specimen')
                if 'hover' not in states and not item.get('omitted_states',{}).get('hover'):
                    errors.append(f'{item["id"]}: pointer platform needs hover state or explicit exclusion')
    except (KeyError,TypeError,ValueError,AttributeError,OSError) as exc:
        errors.append(f'Incomplete or invalid REVIEW.json: {exc}')
    return errors


def json_strings(value):
    if isinstance(value,str):
        yield value
    elif isinstance(value,dict):
        for item in value.values(): yield from json_strings(item)
    elif isinstance(value,list):
        for item in value: yield from json_strings(item)


def validate(directory, project, refs, version, evidence=True, review_seal=True):
    errors=reference_errors(directory,project,refs)
    standard=standard_path(directory,version)
    for name,template in DOCS.items():
        path=standard/name
        if not path.is_file(): errors.append(f'Missing required manual file: {name}'); continue
        text=path.read_text(encoding='utf-8')
        if PLACEHOLDER.search(text): errors.append(f'{name} contains unfinished scaffold/placeholder text')
        required=sections((TEMPLATES/(template+'.md')).read_text())
        actual=sections(text)
        for heading in required:
            if not substantive(actual.get(heading,'')):
                errors.append(f'{name}: complete section "{heading}"')
        if name=='REFERENCE_ANALYSIS.md':
            for heading,body in actual.items():
                if heading not in required: continue
                if not all(re.search(r'\b'+key+r'\b',body,re.I) for key in ('WHAT','WHY','EFFECT','FIT','ADAPT','RULE')):
                    errors.append(f'Analysis {heading} lacks WHAT → WHY → EFFECT → FIT → ADAPT → RULE')
                if not re.search(r'\b(Observed|Inferred|Proposed)\b',body):
                    errors.append(f'Analysis {heading} needs evidence labels')
        if name=='DESIGN_JUDGMENT.md' and not any(label in text for label in PROVENANCE):
            errors.append('Design judgments need valid decision provenance')
    dna=principles(standard/'VISUAL_DNA.md')
    if not 5<=len(dna)<=8 or len(set(v.lower() for v in dna))!=len(dna):
        errors.append('VISUAL_DNA.md requires 5–8 distinct substantive numbered principles')
    try:
        data=read_json(standard/'TOKENS.json')
        if data.get('meta',{}).get('status')!='ready': errors.append('TOKENS.json meta.status must be ready')
        if any(PLACEHOLDER.search(value) for value in json_strings(data)): errors.append('TOKENS.json contains placeholders')
        tokens=Tokens(data); spec=read_json(standard/'SPECIMENS.json')
        validate_config(tokens,spec,standard)
        if evidence:
            manifest=read_json(standard/'evidence/render-manifest.json')
            expected_inputs={'TOKENS.json','SPECIMENS.json'}
            if spec['imagery']['mode']=='image': expected_inputs.add(spec['imagery']['file'])
            if set(manifest['inputs'])!=expected_inputs: errors.append('Render manifest input set is incomplete')
            for name,checksum in manifest['inputs'].items():
                if digest(local_file(standard,name))!=checksum: errors.append(f'Stale render input: {name}')
            for name in SHEETS:
                file=name+'.svg'; path=standard/'evidence'/file
                validate_svg(path)
                if manifest['files'].get(file)!=digest(path): errors.append(f'Stale or altered specimen: {file}')
            for item in spec['colors']:
                if contrast(tokens.color(item['token']),tokens.color(item['pair']))<item.get('min_contrast',4.5):
                    errors.append(f'Color contrast failure: {item["token"]} / {item["pair"]}')
            review=read_json(standard/'REVIEW.json')
            errors.extend(review_errors(standard,directory,project,refs,review,spec,dna,review_seal))
    except (ValueError,OSError,KeyError,TypeError,AttributeError) as exc:
        errors.append(str(exc))
    return errors


def review_inputs(standard):
    """Bind the review to the exact manual and visuals that were inspected."""
    return {path.relative_to(standard).as_posix():digest(path)
            for path in sorted(standard.rglob('*'))
            if path.is_file() and path.name not in ('REVIEW.json','LOCK.json')}


def snapshot(directory, project, version):
    standard=standard_path(directory,version)
    files={}
    for path in sorted(standard.rglob('*')):
        if path.is_file() and path.name!='LOCK.json':
            if not path.resolve().is_relative_to(standard.resolve()):
                raise ValueError('Standard files cannot link outside the version')
            files[path.relative_to(directory).as_posix()]=digest(path)
    for name in ('REFERENCE_CONTRACT.md','references.json'):
        files[name]=digest(directory/name)
    scope={key:project.get(key) for key in ('project_name','mode','target_platforms','main_target_device')}
    return {'files':files,'scope':scope}


def lock_errors(directory, project):
    version=project['current_design_version']
    record=project.get('phase2_locks',{}).get(version)
    if not record:
        return ['A validated Phase 2 lock is missing; complete Phase 2 and approve Gate B']
    try:
        current=snapshot(directory,project,version)
    except (ValueError,OSError) as exc:
        return [str(exc)]
    if current!=record:
        return ['Gate B lock is stale: references, scope, manual or evidence changed; create a new version with phase2 upgrade']
    return []


def ensure_editable(project, version):
    if version in project.get('phase2_locks',{}):
        raise ValueError(f'{version} has been locked; use phase2 upgrade --version NEW for global changes')
