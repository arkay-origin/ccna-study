import json, re, importlib, sys, os
sys.path.insert(0, os.path.dirname(__file__))
MODS = ['c1_foundations', 'c2_addressing', 'c3_switching', 'c4_routing', 'c5_security', 'c6_ops']
secs = []
for m in MODS:
    try: secs += importlib.import_module(m).S
    except ModuleNotFoundError as e:
        if e.name == m: print('skip', m); continue
        raise

# validate
errs = []
for s in secs:
    n = len(s['qs'])
    for p in s['lesson']['parts']:
        for b in p['b']:
            for i in b.get('check', []):
                if i >= n: errs.append(f"{s['name']}: check {i} out of range ({n})")
    used = {i for p in s['lesson']['parts'] for b in p['b'] for i in b.get('check', [])}
    missing = set(range(n)) - used
    if missing: errs.append(f"{s['name']}: questions not in any check: {sorted(missing)}")
    for q in s['qs']:
        mc = q['mc']
        if not mc.get('order') and len(mc['o']) != len(set(mc['o'])): errs.append(f"dup option: {q['q']}")
print('\n'.join(errs) or 'checks ok')

DATA = [{'name': s['name'], 'intro': [], 'refs': [], 'notes': [], 'qs': s['qs']} for s in secs]
LESSONS = {s['name']: s['lesson'] for s in secs}
SHORT = {s['name']: s['short'] for s in secs}
groups = []
for s in secs:
    if not groups or groups[-1][0] != s['group']: groups.append([s['group'], []])
    groups[-1][1].append(s['name'])

try:
    from cheat import CHEAT
except ModuleNotFoundError: CHEAT = []
try:
    from exam import EXAM, DOMS
except ModuleNotFoundError: EXAM, DOMS = [], []

h = open(os.path.join(os.path.dirname(__file__), 'shell.html')).read()
J = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')

def sub(old, new, count=1):
    global h
    c = h.count(old)
    if c != count: raise SystemExit(f'expected {count} of {old[:60]!r}, found {c}')
    h = h.replace(old, new)

sub('const DATA = __DATA__;', 'const DATA = ' + J(DATA) + ';')
h = re.sub(r'const SHORT = \{.*?\};\n', lambda m: 'const SHORT = ' + J(SHORT) + ';\n', h, count=1)
h = re.sub(r'const GROUPS=\[\[.*?\]\]\];\n', lambda m: 'const GROUPS=' + J(groups) + ';\n', h, count=1, flags=re.S)
sub("const EXAM=__EXAM__,DOMS=['Routing','Campus','WAN','Network Services','Automation'],MOCKMIN=90;",
    'const EXAM=' + J(EXAM) + ',DOMS=' + J(DOMS) + ',MOCKMIN=60;')
sub('__CHEAT__', J(CHEAT))
sub('__LESSONS__', J(LESSONS))

# ---- wording / identity ----
title = 'CCNA 200-301 v2.0 Study Course'
sub('ENSLD 300-420 Study Guide', title, h.count('ENSLD 300-420 Study Guide'))
sub('ENSLD Study', 'CCNA Study', h.count('ENSLD Study'))
sub('<h1>Network <span>/</span> Design</h1>', '<h1>CCNA <span>/</span> 200-301</h1>')
sub('Cisco ENSLD 300-420 · Designing Cisco Enterprise Networks', 'Cisco CCNA 200-301 v2.0 · Implementing and Administering Cisco Solutions')
sub("const KEY='ndfc-v1';", "const KEY='ccna-v1';")
sub("const TKEY='ndfc-test-v1';", "const TKEY='ccna-test-v1';")
sub("app:'ensld-study'", "app:'ccna-study'")
sub("d.app!=='ensld-study'", "d.app!=='ccna-study'")
sub("'ensld-progress-'", "'ccna-progress-'")
sub("The instructor's 50-question practice exam, weighted like the real one (Routing 13, Campus 12, WAN 10, Network Services 10, Automation 5).",
    "50 exam-style scenario questions, weighted like the v2.0 blueprint (" + ', '.join(f'{d} {sum(1 for e in EXAM if e["dom"]==d)}' for d in DOMS) + ").")
sub("Key terms, design trade-offs and exam tips from the course's ENSLD 300-420 cheat sheet. Tap a topic to open it.",
    "Commands, numbers, comparisons and exam tips for CCNA 200-301 v2.0. Tap a topic to open it.")
sub('Checked against the Cert Guide', 'Exam topics covered', 2)
sub('<p class="tsub">Each point below was checked against the ENSLD 300-420 Official Cert Guide (PDF page numbers).</p>',
    '<p class="tsub">This lesson maps to these Cisco CCNA 200-301 v2.0 exam topics. Check Cisco\'s published topic list before you book the exam.</p>')
sub('</style><style>body{margin:0}', '.q,.gq h3 span,.mq,.lu li,.ltbl td,.hit span{white-space:pre-wrap}.ltbl td,.gq h3 span,.ans li,.q,.mq,.lp,.lu li,.why,.opt,.hit span{overflow-wrap:anywhere;min-width:0}</style><style>body{margin:0}')
open(os.path.join(os.path.dirname(__file__), '..', 'index.html'), 'w').write(h)
print('sections', len(DATA), 'questions', sum(len(s['qs']) for s in DATA), 'exam', len(EXAM), 'cheat', len(CHEAT), 'bytes', len(h))
