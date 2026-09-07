#!/usr/bin/env python3
"""Build the fictional Margin Phase 2 fixture; never use it as another product's default."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'scripts'))
import phase2
from render_design_specimens import Sheet, Tokens, digest, draw_component, read_json, render, wrap


def render_screen(standard, width=390):
    data=read_json(standard/'TOKENS.json'); tokens=Tokens(data); spec=read_json(standard/'SPECIMENS.json')
    sheet=Sheet('','',width);sheet.parts=[];sheet.y=tokens.role('label')['line_height']+tokens.num('{space.group}')
    margin=18 if width<360 else 28
    text=tokens.color('{color.semantic.text}'); muted=tokens.color('{color.semantic.muted}')
    sheet.text(margin,sheet.y,'静读 / Margin',size=tokens.role('body')['font_size'],weight=tokens.role('label')['weight'],fill=text)
    sheet.y+=tokens.num('{space.section}'); sheet.text(margin,sheet.y,'今日选读   文章归档   我的待读',size=tokens.role('caption')['font_size'],fill=muted)
    sheet.y+=tokens.num('{space.hero}')
    role=tokens.role('h1' if width<360 else 'display')
    for line in wrap('城市里缓慢生长的树',width-2*margin,role['font_size']):
        sheet.text(margin,sheet.y,line,size=role['font_size'],weight=role['weight'],fill=text,family=role['font_family']);sheet.y+=role['line_height']
    sheet.text(margin,sheet.y,'A quieter city',size=tokens.role('title')['font_size'],fill=muted,family=tokens.role('title')['font_family']);sheet.y+=tokens.num('{space.macro}')
    role=tokens.role('body')
    for line in wrap('用十二分钟，重新观察每天经过的街道。给今天，留下一段完整的阅读。',width-2*margin,role['font_size']):
        sheet.text(margin,sheet.y,line,size=role['font_size'],family=role['font_family'],fill=text);sheet.y+=role['line_height']
    sheet.y+=tokens.num('{space.group}');sheet.text(margin,sheet.y,'周一更新 · 约 12 分钟 · 中英双语',size=tokens.role('caption')['font_size'],fill=muted);sheet.y+=tokens.num('{space.section}')
    for id in ('read-primary','save-secondary'):
        item=next(c for c in spec['components'] if c['id']==id)
        height=draw_component(sheet,tokens,item,item['states'][0],margin,sheet.y);sheet.y+=height+tokens.num('{space.component}')
    sheet.y+=tokens.num('{space.group}')
    sheet.y=sheet.paragraph(margin,sheet.y,'一次只选一篇。下次回来，仍从这里继续。',width-2*margin,size=tokens.role('caption')['font_size'],fill=muted)
    sheet.y=max(sheet.y,812 if width==390 else 760)
    content=sheet.finish('静读 — compact representative screen').replace('fill="#F7F8F9"',f'fill="{tokens.color("{color.semantic.canvas}")}"',1)
    filename='representative-screen.svg' if width==390 else 'representative-screen-small.svg'
    (standard/'evidence'/filename).write_text(content,encoding='utf-8')


def populate(directory):
    """Supply authored fixture content into an already initialized/selected test workspace."""
    project=read_json(directory/'project.json'); version=project['current_design_version']
    standard=directory/'standards'/version
    shutil.copytree(Path(__file__).parent/'manual',standard,dirs_exist_ok=True)
    review=read_json(standard/'REVIEW.json');refs=read_json(directory/'references.json')
    review['reference_contract_sha256']=digest(directory/'REFERENCE_CONTRACT.md')
    review['context']['platforms']=project['target_platforms']
    for row in review['influence']:
        if row['source']=='primary': row['contribution']=refs['primary']['contribution']
    (standard/'REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    render_screen(standard);render_screen(standard,320);render(standard)
    # Fixture review assertions only; a real project must inspect and use phase2 review.
    review['reviewed_inputs']=phase2.review_inputs(standard)
    (standard/'REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return standard


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True,type=Path)
    parser.add_argument('--mode',choices=['guided','reference-led','direct'],default='direct')
    args=parser.parse_args()
    def cli(*values):
        subprocess.run([sys.executable,str(REPO/'scripts/design_workspace.py'),*values,'--root',str(args.root)],check=True)
    cli('init','--project','静读 / Margin','--platform','web','--mode',args.mode,'--main-target-device','390 × 844 browser')
    cli('select','--primary','Synthetic R1 editorial study (fictional fixture)|overall grammar',
        '--like','Title-led reading hierarchy','--avoid','Decorative gradients','--do-not-copy','Reference identity or article copy')
    cli('phase2','start')
    standard=populate(args.root/'.design-director')
    cli('phase2','validate')
    print(f'Example ready at {standard}. Inspect sheets before recording Gate B. No production design or automatic approval is claimed.')


if __name__=='__main__':
    main()
