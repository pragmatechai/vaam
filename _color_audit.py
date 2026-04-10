import re, os, json

# Logo palette (canonical colors, lowercase)
emerald = {'#ecfdf5','#d1fae5','#a7f3d0','#6ee7b7','#34d399','#10b981','#059669','#047857','#065f46','#064e3b'}
gold = {'#fffbeb','#fef3c7','#fef9c3','#fde68a','#fcd34d','#fbbf24','#f59e0b','#d97706','#b45309','#92400e','#78350f'}
slate = {'#f8fafc','#f1f5f9','#e2e8f0','#cbd5e1','#94a3b8','#64748b','#475569','#334155','#1e293b','#0f172a','#020617'}
palette = emerald | gold | slate
common_hex = {'#000000','#000','#ffffff','#fff'}

hex_re = re.compile(r'#([0-9a-fA-F]{3,8})\b')
rgb_re = re.compile(r'rgba?\s*\([^)]+\)', re.IGNORECASE)
var_re = re.compile(r'--[a-zA-Z0-9_-]+')
gradient_re = re.compile(r'(?:linear-gradient|radial-gradient|conic-gradient)\s*\([^;}{]{5,200}\)', re.IGNORECASE)
color_kw_list = ['red','green','blue','yellow','orange','purple','white','black','gray','grey',
    'gold','silver','emerald','amber','teal','cyan','magenta','pink','brown','navy',
    'olive','maroon','lime','aqua','fuchsia','indigo','violet','coral','crimson',
    'khaki','plum','salmon','sienna','tan','tomato','turquoise','wheat']
color_kw_re = re.compile(r'\b(' + '|'.join(color_kw_list) + r')\b', re.IGNORECASE)
tw_re = re.compile(
    r'\b(?:text|bg|border|ring|shadow|from|to|via|fill|stroke|accent|outline|decoration|divide|placeholder)'
    r'-(?:emerald|green|amber|yellow|gold|slate|gray|red|blue|orange|purple|pink|teal|cyan|indigo|violet|lime|rose|fuchsia|sky|stone|zinc|neutral|white|black)'
    r'(?:-\d+)?(?:/\d+)?\b'
)

# Collect files
files = []
# Root HTML
for f in ['index.html','about.html','contact.html','services.html','products.html',
           'product-detail.html','projects.html','news.html','news-detail.html','melumat.html']:
    if os.path.exists(f):
        files.append(f)

# Templates
for root, dirs, fnames in os.walk('templates'):
    for f in fnames:
        if f.endswith(('.html','.css','.js')):
            files.append(os.path.join(root, f))

# JS
for p in ['js/app.js', 'static/js/app.js']:
    if os.path.exists(p):
        files.append(p)
for d in ['staticjs']:
    if os.path.isdir(d):
        for root, dirs, fnames in os.walk(d):
            for f in fnames:
                files.append(os.path.join(root, f))

# CSS
for d in ['static/css', 'staticcss']:
    if os.path.isdir(d):
        for root, dirs, fnames in os.walk(d):
            for f in fnames:
                files.append(os.path.join(root, f))

# Python
for p in ['core/views.py', 'core/context_processors.py', 'vaam_project/settings.py']:
    if os.path.exists(p):
        files.append(p)

files = list(dict.fromkeys(files))

results = {}
for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        continue

    hexes = set()
    for m in hex_re.finditer(content):
        h = '#' + m.group(1).lower()
        hexes.add(h)

    rgbs = set(m.group(0) for m in rgb_re.finditer(content))
    css_vars = set(m.group(0) for m in var_re.finditer(content))
    color_var_keys = ['color','bg','text','border','fill','stroke','shadow','gradient',
        'primary','accent','dark','emerald','gold','amber','slate','green','brand',
        'surface','muted','ring','overlay','hover','focus']
    color_vars = set(v for v in css_vars if any(k in v.lower() for k in color_var_keys))
    gradients = set()
    for m in gradient_re.finditer(content):
        g = m.group(0)
        if len(g) > 150:
            g = g[:150] + '...'
        gradients.add(g)
    keywords = set(m.group(0).lower() for m in color_kw_re.finditer(content))
    tw_classes = set(m.group(0) for m in tw_re.finditer(content))

    if hexes or rgbs or color_vars or gradients or tw_classes:
        on_palette = sorted(hexes & palette)
        off_palette = sorted(hexes - palette - common_hex)
        common_found = sorted(hexes & common_hex)
        results[filepath] = {
            'on_palette': on_palette,
            'off_palette': off_palette,
            'common': common_found,
            'rgb': sorted(rgbs),
            'vars': sorted(color_vars),
            'gradients': sorted(gradients),
            'tailwind': sorted(tw_classes),
            'keywords': sorted(keywords),
        }

for fp, d in sorted(results.items()):
    print(f"\n{'='*60}")
    print(f"FILE: {fp}")
    print(f"{'='*60}")
    if d['on_palette']:
        print(f"  ON-PALETTE hex ({len(d['on_palette'])}): {', '.join(d['on_palette'])}")
    if d['off_palette']:
        print(f"  *** OFF-PALETTE hex ({len(d['off_palette'])}): {', '.join(d['off_palette'])}")
    if d['common']:
        print(f"  Common hex: {', '.join(d['common'])}")
    if d['rgb']:
        print(f"  RGB/RGBA ({len(d['rgb'])}): {', '.join(d['rgb'])}")
    if d['vars']:
        print(f"  CSS color vars ({len(d['vars'])}): {', '.join(d['vars'])}")
    if d['gradients']:
        print(f"  Gradients ({len(d['gradients'])}):")
        for g in d['gradients']:
            print(f"    {g}")
    if d['tailwind']:
        print(f"  Tailwind ({len(d['tailwind'])}): {', '.join(d['tailwind'])}")
    if d['keywords']:
        print(f"  Color keywords: {', '.join(d['keywords'])}")
    if not any([d['on_palette'], d['off_palette'], d['common'], d['rgb'], d['vars'], d['gradients'], d['tailwind']]):
        print("  (no color values found)")

print(f"\n\n{'='*60}")
print("GLOBAL SUMMARY")
print(f"{'='*60}")
all_off = set()
all_rgb = set()
all_tw = set()
all_grad = set()
all_vars = set()
off_files = {}
for fp, d in results.items():
    for c in d['off_palette']:
        all_off.add(c)
        off_files.setdefault(c, []).append(fp)
    all_rgb |= set(d['rgb'])
    all_tw |= set(d['tailwind'])
    all_grad |= set(d['gradients'])
    all_vars |= set(d['vars'])

print(f"\nOFF-PALETTE colors ({len(all_off)}):")
for c in sorted(all_off):
    print(f"  {c} -> found in: {', '.join(off_files[c])}")

print(f"\nAll RGB/RGBA values ({len(all_rgb)}):")
for r in sorted(all_rgb):
    print(f"  {r}")

print(f"\nAll Tailwind color classes ({len(all_tw)}):")
for t in sorted(all_tw):
    print(f"  {t}")

print(f"\nAll CSS color variables ({len(all_vars)}):")
for v in sorted(all_vars):
    print(f"  {v}")

print(f"\nAll gradients ({len(all_grad)}):")
for g in sorted(all_grad):
    print(f"  {g}")

print(f"\nTotal files scanned: {len(files)}")
print(f"Files with color values: {len(results)}")
