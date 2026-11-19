"""Helpers for writing CCNA course content compactly."""
import html

def Q(q, a, wrong, why, card=None, note='', ca=None):
    """Multiple-choice question. a = correct answer(s); wrong = distractors."""
    a = a if isinstance(a, list) else [a]
    d = {'q': q, 'a': a, 'why': why, 'note': note, 'dup': False,
         'mc': {'o': a + wrong, 'c': list(range(len(a)))}}
    if card: d['card'] = card
    if ca: d['ca'] = ca
    return d

def ORD(q, steps, why, card=None):
    """Put-in-order question; steps given in the right order."""
    d = {'q': q, 'a': [f'{i+1}. {s}' for i, s in enumerate(steps)], 'why': why, 'note': '', 'dup': False,
         'mc': {'order': True}}
    if card: d['card'] = card
    return d

# lesson blocks
P = lambda t: {'p': t}
UL = lambda *xs: {'ul': list(xs)}
TB = lambda *rows: {'tbl': [list(r) for r in rows]}
TIP = lambda t: {'tip': t}
CK = lambda *ix: {'check': list(ix)}
DIA = lambda svg: {'dia': svg}

def lesson(mins, intro, parts, topics):
    return {'mins': mins, 'intro': intro,
            'parts': [{'h': h, 'b': b} for h, b in parts],
            'verified': [[t, f'Topic {n}'] for n, t in topics], 'course': []}

def sec(name, short, group, intro_txt, les, qs):
    return {'name': name, 'short': short, 'group': group, 'lesson': les, 'qs': qs}

# ---------- tiny SVG diagram DSL ----------
E = lambda t: html.escape(str(t), quote=True)
MARK = ('<defs><marker id="ar" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0 0L8 4L0 8z" class="d-arh"/></marker></defs>')

def svg(w, h, label, *parts):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{E(label)}">{MARK}{"".join(parts)}</svg>'

def txt(x, y, t, cls='d-t', anchor='middle'):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{E(t)}</text>'

def ln(x1, y1, x2, y2, cls='d-ln', arrow=False, both=False):
    m = ''
    if arrow: m += ' marker-end="url(#ar)"'
    if both: m += ' marker-start="url(#ar)"'
    return f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{m}/>'

def box(x, y, w, h, cls='d-box'):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>'

def router(x, y, label=None, below=True):
    s = (f'<circle class="d-rt" cx="{x}" cy="{y}" r="11"/>'
         f'<path class="d-x" d="M{x-6} {y-3}h12M{x-6} {y+3}h12"/>')
    if label: s += txt(x, y + 24 if below else y - 16, label)
    return s

def switch(x, y, label=None, below=True):
    s = (f'<rect class="d-rt" x="{x-15}" y="{y-9}" width="30" height="18" rx="3"/>'
         f'<path class="d-x" d="M{x-9} {y-3}h18M{x-9} {y+3}h18"/>')
    if label: s += txt(x, y + 22 if below else y - 14, label)
    return s

def host(x, y, label=None, below=True, w=None):
    w = w or max(34, 7 * len(label or '') + 10)
    s = f'<rect class="d-rt" x="{x-w/2}" y="{y-9}" width="{w}" height="18" rx="3"/>'
    if label: s += txt(x, y + 4, label, 'd-s')
    return s

def cloud(x, y, rx, ry, label=None):
    s = f'<ellipse class="d-cloud" cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>'
    if label: s += txt(x, y + 4, label, 'd-s')
    return s

def num(x, y, n):
    return f'<circle class="d-rt" cx="{x}" cy="{y}" r="8"/>' + txt(x, y + 3.5, n, 'd-s')

CODE = lambda *lines: {'code': '\n'.join(lines)}
NOTE = lambda label, t: {'note': t, 'nl': label}
