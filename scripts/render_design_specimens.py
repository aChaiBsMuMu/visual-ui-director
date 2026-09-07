#!/usr/bin/env python3
"""Render scope-configured design spec sheets using only the Python standard library."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import re
import textwrap
import unicodedata
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

SHEETS = ('color-palette-board', 'typography-specimen', 'spacing-geometry-sheet',
          'layout-atlas', 'component-specimen', 'icon-style-sheet', 'style-tile')
TOKEN = re.compile(r'^\{([A-Za-z0-9_.-]+)\}$')
HEX = re.compile(r'^#[0-9a-fA-F]{6}$')
KINDS = {'button', 'surface', 'input', 'navigation', 'tabs', 'chip', 'feedback', 'text'}
REQUIRED_STATES = {
    'button': {'default', 'pressed', 'disabled', 'loading'},
    'input': {'default', 'focus', 'disabled', 'error'},
    'navigation': {'default', 'selected'}, 'tabs': {'default', 'selected', 'disabled'},
    'chip': {'default', 'selected'}, 'feedback': {'default'},
    'surface': {'default'}, 'text': {'default'},
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ValueError(f'{path}: {exc}') from exc


def local_file(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f'Expected a local relative file: {relative!r}')
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f'Missing or out-of-scope file: {relative}')
    return path


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be nonempty text')
    return value


def number(value, label, minimum=0, maximum=10000):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not minimum <= value <= maximum:
        raise ValueError(f'{label} must be a finite number in {minimum}..{maximum}')
    return value


class Tokens:
    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError('TOKENS.json must be an object')
        self.data = data

    def resolve(self, ref, trail=()):
        match = TOKEN.fullmatch(ref) if isinstance(ref, str) else None
        if not match:
            raise ValueError(f'Expected token reference {{path.to.token}}, got {ref!r}')
        key = match.group(1)
        if key in trail:
            raise ValueError(f'Cyclic token alias: {key}')
        value = self.data
        for part in key.split('.'):
            if not isinstance(value, dict) or part not in value:
                raise ValueError(f'Missing token: {key}')
            value = value[part]
        if isinstance(value, str) and TOKEN.fullmatch(value):
            return self.resolve(value, (*trail, key))
        return value

    def color(self, ref):
        value = self.resolve(ref)
        if not isinstance(value, str) or not HEX.fullmatch(value):
            raise ValueError(f'{ref} must resolve to an opaque #RRGGBB color')
        return value

    def num(self, ref, minimum=0, maximum=10000):
        return number(self.resolve(ref), str(ref), minimum, maximum)

    def role(self, name):
        value = self.resolve('{typography.roles.' + name + '}')
        if not isinstance(value, dict):
            raise ValueError(f'Typography role {name} must be an object')
        def val(key):
            return self.resolve('{typography.roles.' + name + '.' + key + '}')
        role = {key: val(key) for key in ('font_family', 'font_size', 'weight', 'line_height', 'tracking', 'color')}
        nonempty(role['font_family'], name + '.font_family')
        number(role['font_size'], name + '.font_size', 6, 160)
        number(role['weight'], name + '.weight', 100, 1000)
        number(role['line_height'], name + '.line_height', role['font_size'], 240)
        number(role['tracking'], name + '.tracking', -5, 20)
        if not isinstance(role['color'], str) or not HEX.fullmatch(role['color']):
            raise ValueError(f'{name}.color must resolve to #RRGGBB')
        return role


def contrast(a, b):
    def luminance(color):
        values = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
        values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
        return sum(v * w for v, w in zip(values, (.2126, .7152, .0722)))
    x, y = sorted((luminance(a), luminance(b)))
    return (y + .05) / (x + .05)


def validate_config(tokens, spec, root):
    """Check structure and all render-used token references; never supply a default palette."""
    try:
        if not isinstance(spec, dict) or spec.get('schema_version') != 1:
            raise ValueError('SPECIMENS.json requires schema_version 1')
        if spec.get('status') != 'ready':
            raise ValueError('SPECIMENS.json status must be ready after completing the scope configuration')
        nonempty(spec['title'], 'title')
        if not isinstance(spec['languages'], list) or not spec['languages']:
            raise ValueError('languages must declare actual content languages')
        for key in ('colors', 'typography', 'patterns', 'components', 'icons'):
            if not isinstance(spec[key], list):
                raise ValueError(f'{key} must be an array')
        for key in ('colors', 'typography', 'patterns'):
            if not spec[key]:
                raise ValueError(f'{key} cannot be empty')
        # Icons/components can be explicitly out of scope, with visible rationale.
        for key in ('components', 'icons'):
            if not spec[key]:
                nonempty(spec.get(key + '_omission'), key + '_omission')
        for color in spec['colors']:
            for key in ('role', 'usage', 'frequency', 'do', 'dont'):
                nonempty(color[key], f'color.{key}')
            if color['group'] not in ('Brand', 'Neutral', 'Semantic'):
                raise ValueError('color.group must be Brand, Neutral or Semantic')
            tokens.color(color['token']); tokens.color(color['pair'])
            threshold = color.get('min_contrast', 4.5)
            number(threshold, 'min_contrast', 1, 21)
            if threshold != 4.5:
                nonempty(color.get('contrast_reason'), 'contrast_reason for non-default threshold')
        samples = ''
        for item in spec['typography']:
            tokens.role(item['role']); samples += nonempty(item['sample'], 'typography.sample')
        if any(str(lang).lower().startswith('zh') for lang in spec['languages']) and not re.search(r'[\u3400-\u9fff]', samples):
            raise ValueError('Chinese content requires Chinese typography samples')
        if any(str(lang).lower().startswith('en') for lang in spec['languages']) and not re.search('[A-Za-z]', samples):
            raise ValueError('English content requires Latin typography samples')
        geometry = spec['geometry']
        for key in ('spacing', 'radii', 'borders', 'surfaces'):
            if not isinstance(geometry[key], list) or not geometry[key]:
                raise ValueError(f'geometry.{key} must contain scoped examples')
        for key in ('spacing', 'radii'):
            for item in geometry[key]:
                nonempty(item['label'], key + '.label'); tokens.num(item['token'], 0, 320)
        for item in geometry['borders']:
            tokens.num(item['width'], 0, 12); tokens.color(item['color'])
            nonempty(item['label'], 'border.label')
        for item in geometry['surfaces']:
            nonempty(item['label'], 'surface.label'); tokens.color(item['color'])
            tokens.num(item['radius'], 0, 100)
            shadow = tokens.resolve(item['shadow'])
            if not isinstance(shadow, dict):
                raise ValueError('shadow token must be an object')
            for key in ('dx', 'dy', 'blur', 'opacity'):
                number(shadow[key], 'shadow.' + key, -50 if key in ('dx', 'dy') else 0, 1 if key == 'opacity' else 50)
            if not HEX.fullmatch(shadow['color']):
                raise ValueError('shadow.color must be #RRGGBB')
        ids = set()
        for pattern in spec['patterns']:
            nonempty(pattern['id'], 'pattern.id')
            if pattern['id'] in ids:
                raise ValueError('Duplicate pattern ID')
            ids.add(pattern['id'])
            for key in ('name', 'purpose', 'reading_path', 'density', 'scrolling', 'avoid', 'transformation'):
                nonempty(pattern[key], 'pattern.' + key)
            if not pattern['regions']:
                raise ValueError('Pattern must have regions')
            for region in pattern['regions']:
                for key in ('x', 'y', 'w', 'h'):
                    number(region[key], 'region.' + key, 0, 100)
                if region['w'] <= 0 or region['h'] <= 0 or region['x'] + region['w'] > 100 or region['y'] + region['h'] > 100:
                    raise ValueError('Pattern region must fit its normalized 0..100 canvas')
                nonempty(region['label'], 'region.label')
                if region['level'] not in ('primary', 'secondary', 'tertiary', 'background'):
                    raise ValueError('Invalid region hierarchy')
        ids = set()
        for item in spec['components']:
            nonempty(item['id'], 'component.id')
            if item['id'] in ids:
                raise ValueError('Duplicate component ID')
            ids.add(item['id'])
            if item['kind'] not in KINDS:
                raise ValueError(f'Unsupported anatomy kind: {item["kind"]}')
            for key in ('name', 'why', 'content_rule'):
                nonempty(item[key], 'component.' + key)
            tokens.role(item['typography'])
            tokens.num(item['width'], 40, 900); tokens.num(item['height'], 20, 400)
            tokens.num(item['padding'], 0, 100)
            if not isinstance(item['states'], list) or not item['states']:
                raise ValueError('Component states are required')
            state_names = [state['name'] for state in item['states']]
            if len(set(state_names)) != len(state_names):
                raise ValueError('Duplicate component state')
            if 'default' not in state_names:
                raise ValueError('Component default state cannot be omitted')
            omitted = item.get('omitted_states', {})
            for key, reason in omitted.items():
                nonempty(reason, 'omitted state ' + key)
            missing = REQUIRED_STATES[item['kind']] - set(state_names) - set(omitted)
            if missing:
                raise ValueError(f'{item["id"]}: missing states {sorted(missing)}')
            for state in item['states']:
                nonempty(state['name'], 'state.name'); nonempty(state['label'], 'state.label')
                tokens.color(state['bg']); tokens.color(state['fg']); tokens.color(state['border'])
                tokens.num(state['border_width'], 0, 12); tokens.num(state['radius'], 0, 200)
                if 'focus' in state:
                    tokens.color(state['focus'])
                if 'active_fg' in state:
                    tokens.color(state['active_fg'])
        for item in spec['icons']:
            for key in ('name', 'source', 'accessible_label', 'container_rule'):
                nonempty(item[key], 'icon.' + key)
            grid = tokens.num(item['grid'], 8, 128)
            tokens.num(item['stroke'], 0, grid/4)
            if tokens.resolve(item['cap']) not in ('butt', 'round', 'square') or tokens.resolve(item['join']) not in ('miter', 'round', 'bevel'):
                raise ValueError('Invalid icon cap/join token')
            if not isinstance(item['paths'], list) or not item['paths']:
                raise ValueError('Icon needs actual vector paths')
            for path in item['paths']:
                if not isinstance(path, str) or not re.fullmatch(r'[MmZzLlHhVvCcSsQqTtAaEe0-9+.,\s-]+', path):
                    raise ValueError('Icon paths must be SVG path data')
            for size in item['sizes']:
                tokens.num(size, 8, 128)
            if not item['sizes']:
                raise ValueError('Icon size roles missing')
            if 'default' not in item['states']:
                raise ValueError('Icon default state cannot be omitted')
            missing_states = {'default', 'active', 'selected'} - set(item['states'])
            for state in missing_states:
                nonempty(item.get('omitted_states', {}).get(state), f'icon {state} omission reason')
            for state in item['states'].values():
                tokens.color(state['color'])
                if state['fill'] not in ('outline', 'filled'):
                    raise ValueError('Icon state fill must be outline or filled')
                if 'container' in state:
                    tokens.color(state['container']); tokens.num(state['radius'], 0, 128)
        imagery = spec['imagery']
        if imagery['mode'] == 'image':
            path = local_file(root, imagery['file'])
            if path.suffix.lower() not in ('.png', '.jpg', '.jpeg'):
                raise ValueError('Imagery renderer accepts local PNG/JPEG assets')
            nonempty(imagery['caption'], 'imagery.caption')
        elif imagery['mode'] == 'none':
            nonempty(imagery['reason'], 'imagery.reason')
        else:
            raise ValueError('imagery.mode must be image or reasoned none')
        nonempty(spec['motion_cue'], 'motion_cue')
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError(f'Incomplete or invalid SPECIMENS.json: {exc}') from exc


def visual_width(text):
    return sum(1 if unicodedata.east_asian_width(c) in 'WF' else .57 for c in text)


def wrap(text, width, size):
    lines, line = [], ''
    for char in str(text):
        if char == '\n' or (line and visual_width(line + char) * size > width):
            lines.append(line.rstrip()); line = ''
        if char != '\n':
            line += char
    if line:
        lines.append(line.rstrip())
    return lines or ['']


class Sheet:
    def __init__(self, title, subtitle, width=1120):
        self.width = width; self.parts = []; self.y = 40
        self.text(32, self.y, title, size=26, weight=600); self.y += 38
        self.y = self.paragraph(32, self.y, subtitle, width-64, size=13) + 26

    def text(self, x, y, value, size=14, fill='#25333B', weight=400, family='Arial, PingFang SC, sans-serif', tracking=0):
        self.parts.append(f'<text x="{x:g}" y="{y:g}" font-family="{escape(family, quote=True)}" font-size="{size:g}" font-weight="{weight}" letter-spacing="{tracking:g}" fill="{escape(fill, quote=True)}">{escape(str(value))}</text>')

    def paragraph(self, x, y, value, width, size=14, **kwargs):
        for line in wrap(value, width, size):
            self.text(x, y, line, size=size, **kwargs); y += size * 1.5
        return y

    def rect(self, x, y, w, h, fill='#FFFFFF', stroke='#B8C2C8', radius=0, sw=1, extra=''):
        self.parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{radius:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}" {extra}/>')

    def section(self, title):
        self.y += 12; self.text(32, self.y, title, size=20, weight=600); self.y += 30

    def finish(self, title):
        height = math.ceil(self.y + 32)
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{height}" viewBox="0 0 {self.width} {height}" role="img" aria-label="{escape(title, quote=True)}"><title>{escape(title)}</title><rect width="100%" height="100%" fill="#F7F8F9"/>' + ''.join(self.parts) + '</svg>\n'


def draw_colors(sheet, tokens, spec):
    for group in ('Brand', 'Neutral', 'Semantic'):
        items = [item for item in spec['colors'] if item['group'] == group]
        if not items:
            continue
        sheet.section(group + ' Palette')
        for item in items:
            y = sheet.y; color = tokens.color(item['token']); fg = tokens.color(item['pair'])
            sheet.rect(32, y, 180, 80, fill=color, stroke=color)
            sheet.text(44, y + 32, 'Aa 中文', size=19, fill=fg)
            sheet.text(44, y + 60, color, fill=fg)
            y = sheet.paragraph(232, y + 16, item['role'] + ' · ' + item['token'], 850, weight=600)
            y = sheet.paragraph(232, y, 'Foreground ' + item['pair'] + ' · ' + fg + f' · contrast {contrast(color, fg):.2f}:1', 850, size=12)
            for label, key in [('Use', 'usage'), ('Frequency', 'frequency'), ('Do', 'do'), ("Don't", 'dont')]:
                y = sheet.paragraph(232, y, label + ': ' + item[key], 850, size=12)
            sheet.y = max(sheet.y + 100, y + 14)


def draw_type(sheet, tokens, spec):
    for item in spec['typography']:
        role = tokens.role(item['role'])
        sheet.text(32, sheet.y, f'{item["role"]} · {role["font_size"]} / {role["line_height"]} · {role["weight"]}', size=12)
        sheet.y += 20 + role['font_size']
        for line in wrap(item['sample'], sheet.width - 64, role['font_size'] + max(0, role['tracking'])):
            sheet.text(32, sheet.y, line, size=role['font_size'], weight=role['weight'], family=role['font_family'], tracking=role['tracking'], fill=role['color'])
            sheet.y += role['line_height']
        sheet.y += 18


def draw_geometry(sheet, tokens, spec):
    g = spec['geometry']; sheet.section('Spacing scale — lengths at 1 SVG unit per token unit')
    for item in g['spacing']:
        value = tokens.num(item['token'])
        sheet.text(32, sheet.y + 15, item['label'], size=13)
        sheet.rect(220, sheet.y, max(value, .5), 16, fill='#425D6C', sw=0)
        sheet.text(570, sheet.y + 15, f'{item["token"]} = {value}', size=12); sheet.y += 35
    sheet.section('Radius roles — same rectangle, different corner relationship')
    for item in g['radii']:
        value = tokens.num(item['token']); sheet.rect(32, sheet.y, 200, 76, radius=value)
        sheet.paragraph(260, sheet.y + 22, f'{item["label"]} · {item["token"]} = {value}', 800)
        sheet.y += 96
    sheet.section('Borders and dividers')
    for item in g['borders']:
        sheet.rect(32, sheet.y, 200, 48, stroke=tokens.color(item['color']), sw=tokens.num(item['width']))
        sheet.paragraph(260, sheet.y + 22, f'{item["label"]} · {item["width"]} / {item["color"]}', 800, size=13)
        sheet.y += 72
    sheet.section('Surface hierarchy and elevation')
    for index, item in enumerate(g['surfaces']):
        s = tokens.resolve(item['shadow']); fid = f'shadow-{len(sheet.parts)}-{index}'
        sheet.parts.append(f'<defs><filter id="{fid}" x="-50%" y="-100%" width="200%" height="300%"><feDropShadow dx="{s["dx"]}" dy="{s["dy"]}" stdDeviation="{s["blur"]}" flood-color="{s["color"]}" flood-opacity="{s["opacity"]}"/></filter></defs>')
        sheet.rect(32, sheet.y, 200, 70, fill=tokens.color(item['color']), radius=tokens.num(item['radius']), sw=0, extra=f'filter="url(#{fid})"')
        sheet.paragraph(260, sheet.y + 24, f'{item["label"]} · {item["color"]} · {item["shadow"]}', 800, size=13)
        sheet.y += 108


def draw_layout(sheet, tokens, spec):
    fills = {'primary':'#CBD9E0', 'secondary':'#E1E8EC', 'tertiary':'#EEF1F3', 'background':'#FFFFFF'}
    for pattern in spec['patterns']:
        sheet.section(pattern['name'] + ' [' + pattern['id'] + ']')
        y = sheet.y; width, height = 480, 480
        sheet.rect(32, y, width, height)
        for region in pattern['regions']:
            x = 32 + region['x'] * width/100; ry = y + region['y'] * height/100
            w = region['w'] * width/100; h = region['h'] * height/100
            sheet.rect(x, ry, w, h, fill=fills[region['level']])
            label = region['label'] + f' · {region["w"]}×{region["h"]}%'
            size = 11 if w > 70 else 9
            lines = wrap(label, max(10, w-12), size)
            if len(lines) * size*1.5 > h-8:
                raise ValueError(f'Pattern {pattern["id"]}: label does not fit region {region["label"]}; shorten it or enlarge the region')
            sheet.paragraph(x+6, ry+size+4, label, max(10, w-12), size=size)
        end = y + 14
        for key in ('purpose', 'reading_path', 'density', 'scrolling', 'avoid', 'transformation'):
            end = sheet.paragraph(550, end, key.replace('_', ' ').title() + ': ' + pattern[key], 530, size=14) + 16
        sheet.y = max(y + height, end) + 26


def draw_component(sheet, tokens, item, state, x, y):
    width = tokens.num(item['width']); height = tokens.num(item['height']); pad = tokens.num(item['padding'])
    role = tokens.role(item['typography']); fg = tokens.color(state['fg'])
    sheet.rect(x, y, width, height, fill=tokens.color(state['bg']), stroke=tokens.color(state['border']), sw=tokens.num(state['border_width']), radius=tokens.num(state['radius']))
    if 'focus' in state:
        focus_x, focus_w = x, width
        if item['kind'] in ('tabs', 'navigation') and 'focus_index' in state:
            index = state['focus_index']; count = len(state.get('items', []))
            if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < count:
                raise ValueError('focus_index outside navigation items')
            focus_w = width/count; focus_x = x+index*focus_w
        sheet.rect(focus_x-4, y-4, focus_w+8, height+8, fill='none', stroke=tokens.color(state['focus']), sw=2, radius=tokens.num(state['radius'])+3)
    kind = item['kind']; label = state['label']
    if kind in ('tabs', 'navigation'):
        labels = state.get('items', [label])
        if not labels or not all(isinstance(v, str) and v for v in labels):
            raise ValueError('Navigation items must be nonempty labels')
        cell = width/len(labels)
        for index, text in enumerate(labels):
            if visual_width(text)*role['font_size'] > cell-2*pad:
                raise ValueError(f'{item["id"]}: navigation label does not fit')
            sheet.text(x+index*cell+pad, y+height/2+role['font_size']*.35, text, size=role['font_size'], fill=tokens.color(state['active_fg']) if state.get('active_index') == index and 'active_fg' in state else fg, family=role['font_family'], weight=role['weight'])
        if 'active_index' in state:
            active = state['active_index']
            if isinstance(active, bool) or not isinstance(active, int) or not 0 <= active < len(labels):
                raise ValueError('active_index outside navigation items')
            sheet.rect(x+active*cell+pad, y+height-5, cell-2*pad, 3, fill=tokens.color(state['active_fg']) if 'active_fg' in state else fg, sw=0)
    else:
        available = width-2*pad
        lines = wrap(label, available, role['font_size'] + max(0, role['tracking']))
        if len(lines)*role['line_height'] > height-2*pad:
            raise ValueError(f'{item["id"]}/{state["name"]}: real text does not fit dimensions; revise tokens or content')
        ty = y+(height-len(lines)*role['line_height'])/2+role['font_size']
        for line in lines:
            sheet.text(x+pad, ty, line, size=role['font_size'], fill=fg, family=role['font_family'], weight=role['weight'], tracking=role['tracking'])
            ty += role['line_height']
    return height


def draw_components(sheet, tokens, spec):
    if not spec['components']:
        sheet.y = sheet.paragraph(32, sheet.y, spec['components_omission'], 1056)
    for item in spec['components']:
        sheet.section(item['name'] + ' [' + item['kind'] + ']')
        sheet.y = sheet.paragraph(32, sheet.y, 'Why: ' + item['why'] + ' Content: ' + item['content_rule'], 1056, size=13) + 14
        for state in item['states']:
            sheet.text(32, sheet.y+22, state['name'], size=13)
            h = draw_component(sheet, tokens, item, state, 180, sheet.y)
            sheet.y += h+22
        for name, reason in item.get('omitted_states', {}).items():
            sheet.y = sheet.paragraph(32, sheet.y, f'{name} excluded: {reason}', 1056, size=12)
        sheet.y += 10


def draw_icon(sheet, tokens, item, state, size, x, y):
    grid = tokens.num(item['grid']); stroke = tokens.num(item['stroke'])
    color = tokens.color(state['color'])
    if 'container' in state:
        sheet.rect(x-6, y-6, size+12, size+12, fill=tokens.color(state['container']), sw=0, radius=tokens.num(state['radius']))
    sheet.parts.append(f'<g transform="translate({x:g},{y:g}) scale({size/grid:g})" stroke="{color}" stroke-width="{stroke:g}" stroke-linecap="{tokens.resolve(item["cap"])}" stroke-linejoin="{tokens.resolve(item["join"])}" fill="{color if state["fill"] == "filled" else "none"}">')
    for path in item['paths']:
        sheet.parts.append(f'<path d="{escape(path, quote=True)}"/>')
    sheet.parts.append('</g>')


def draw_icons(sheet, tokens, spec):
    if not spec['icons']:
        sheet.y = sheet.paragraph(32, sheet.y, spec['icons_omission'], 1056)
    for item in spec['icons']:
        sheet.section(item['name'])
        sheet.y = sheet.paragraph(32, sheet.y, item['source'] + ' · ' + item['container_rule'] + ' · label: ' + item['accessible_label'], 1056, size=13)+16
        # Enlarged optical grid makes stroke, caps and geometry inspectable.
        grid_x, grid_y, grid_size = 180, sheet.y, 96
        for step in range(5):
            v = step * grid_size / 4
            sheet.parts.append(f'<path d="M{grid_x+v} {grid_y} V{grid_y+grid_size} M{grid_x} {grid_y+v} H{grid_x+grid_size}" fill="none" stroke="#D0D8DD" stroke-width="0.5"/>')
        draw_icon(sheet, tokens, item, item['states']['default'], grid_size, grid_x, grid_y)
        sheet.text(300, grid_y+42, 'Optical grid / enlarged geometry', size=13)
        sheet.y += 124
        for name, state in item['states'].items():
            sheet.text(32, sheet.y+25, name, size=13)
            x = 180; row_height = 0
            for size_ref in item['sizes']:
                size = tokens.num(size_ref)
                sheet.rect(x, sheet.y, size, size, fill='none', stroke='#CCD5DA', sw=.5)
                draw_icon(sheet, tokens, item, state, size, x, sheet.y)
                sheet.text(x, sheet.y+size+22, str(size), size=11)
                x += max(size+60, 100); row_height = max(row_height, size+48)
            sheet.y += row_height+12
        for name, reason in item.get('omitted_states', {}).items():
            sheet.y = sheet.paragraph(32, sheet.y, name + ' omitted: ' + reason, 1056, size=12)
        sheet.text(32, sheet.y, f'Grid {tokens.num(item["grid"]):g} · Stroke {tokens.num(item["stroke"]):g} · {tokens.resolve(item["cap"])}/{tokens.resolve(item["join"])}', size=12)
        sheet.y += 32
        draw_icon(sheet, tokens, item, item['states']['default'], tokens.num(item['sizes'][0]), 32, sheet.y)
        sheet.text(80, sheet.y+18, item['accessible_label'], size=14)
        sheet.y += max(48, tokens.num(item['sizes'][0])+20)


def draw_tile(sheet, tokens, spec, root):
    sheet.section('Identity in combination — same tokens and anatomy as the sheets')
    draw_type(sheet, tokens, {**spec, 'typography':spec['typography'][:3]})
    x = 32
    for item in spec['colors']:
        if x > 970:
            x = 32; sheet.y += 56
        sheet.rect(x, sheet.y, 72, 24, fill=tokens.color(item['token']), sw=0)
        sheet.text(x, sheet.y+40, tokens.color(item['token']), size=10); x += 88
    sheet.y += 70
    draw_components(sheet, tokens, spec)
    draw_icons(sheet, tokens, spec)
    sheet.section('Imagery / material')
    imagery = spec['imagery']
    if imagery['mode'] == 'image':
        path = local_file(root, imagery['file']); mime = 'image/png' if path.suffix.lower() == '.png' else 'image/jpeg'
        data = base64.b64encode(path.read_bytes()).decode()
        sheet.parts.append(f'<image x="32" y="{sheet.y}" width="480" height="280" preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{data}"/>')
        sheet.y += 310; sheet.y = sheet.paragraph(32, sheet.y, imagery['caption'], 1056)
    else:
        sheet.y = sheet.paragraph(32, sheet.y, 'Deliberate image absence: '+imagery['reason'], 1056)
    draw_geometry(sheet, tokens, spec)
    sheet.section('Motion cue — conceptual state diagram, not timing proof')
    sheet.y = sheet.paragraph(32, sheet.y, spec['motion_cue'], 1056)


def validate_svg(path):
    try:
        root = ET.parse(path).getroot()
        if root.tag != '{http://www.w3.org/2000/svg}svg':
            raise ValueError('root must be SVG with namespace')
        width, height = (float(root.attrib[key].removesuffix('px')) for key in ('width','height'))
        if not (64 <= width <= 8192 and 64 <= height <= 100000):
            raise ValueError('dimensions outside reasonable spec-sheet bounds')
        if not any(el.tag.endswith('}text') and ''.join(el.itertext()).strip() for el in root.iter()):
            raise ValueError('SVG has no readable text')
        if not any(el.tag.rsplit('}',1)[-1] in ('rect','path','circle','image','line','polygon') for el in root.iter()):
            raise ValueError('SVG has no visual geometry')
        for el in root.iter():
            if el.tag.rsplit('}',1)[-1] in ('script','foreignObject'):
                raise ValueError('Specimen SVG cannot contain executable/foreign content')
            for key, value in el.attrib.items():
                if key.lower().startswith('on') or ('href' in key and not value.startswith(('#','data:image/png;base64,','data:image/jpeg;base64,'))):
                    raise ValueError('Specimen SVG cannot use remote or executable references')
        return {'width':width,'height':height}
    except (ET.ParseError, OSError, KeyError, TypeError, ValueError) as exc:
        raise ValueError(f'Invalid SVG {path}: {exc}') from exc


def render(standard):
    standard = Path(standard).resolve()
    tokens = Tokens(read_json(standard/'TOKENS.json')); spec = read_json(standard/'SPECIMENS.json')
    validate_config(tokens, spec, standard)
    functions = (draw_colors, draw_type, draw_geometry, draw_layout, draw_components, draw_icons)
    outputs = {}
    # Build all SVGs before writing any, so content overflow fails without a partial render.
    for name, draw in zip(SHEETS, (*functions, None)):
        sheet = Sheet(name.replace('-', ' ').title(), spec['title'] + ' · Generated specification; product styles resolve TOKENS.json')
        if draw:
            draw(sheet, tokens, spec)
        else:
            draw_tile(sheet, tokens, spec, standard)
        outputs[name+'.svg'] = sheet.finish(name)
    evidence = standard/'evidence'; evidence.mkdir(exist_ok=True)
    manifest = {'schema_version':1, 'inputs':{name:digest(standard/name) for name in ('TOKENS.json','SPECIMENS.json')},'files':{},'contrast':[]}
    if spec['imagery']['mode'] == 'image':
        path = local_file(standard, spec['imagery']['file'])
        manifest['inputs'][spec['imagery']['file']] = digest(path)
    for name, content in outputs.items():
        path = evidence/name; path.write_text(content, encoding='utf-8'); validate_svg(path)
        manifest['files'][name] = digest(path)
    for item in spec['colors']:
        ratio = contrast(tokens.color(item['token']), tokens.color(item['pair']))
        threshold = item.get('min_contrast',4.5)
        manifest['contrast'].append({'token':item['token'],'pair':item['pair'],'ratio':round(ratio,4),'minimum':threshold,'pass':ratio >= threshold})
    (evidence/'render-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--standard', required=True, type=Path)
    args = parser.parse_args()
    try:
        manifest = render(args.standard)
    except ValueError as exc:
        parser.exit(1, str(exc)+'\n')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
