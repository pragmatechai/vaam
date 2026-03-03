"""Download remaining project images with rate-limit-safe delays."""
import urllib.request, time, os, sys

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120'
BASE = '/home/vaam/app/media/'
BUDAK = 'https://upload.wikimedia.org/wikipedia/commons/3/35/Budakeszitrafo.JPG'
HV    = 'https://upload.wikimedia.org/wikipedia/commons/c/c1/High-voltage_transformer.jpg'
PJD   = 'https://upload.wikimedia.org/wikipedia/commons/3/3d/PJD_Genset_700kva.jpg'
MON   = 'https://upload.wikimedia.org/wikipedia/commons/b/bf/Montreal_power_backup.jpg'

todo = [
    ('projects/gallery/gen-uz-2.jpg',    PJD),
    ('projects/gallery/gen-uz-3.jpg',    MON),
    ('projects/tr-az-2500-main.jpg',     BUDAK),
    ('projects/gallery/tr-az-2500-1.jpg',HV),
    ('projects/gallery/tr-az-2500-2.jpg',BUDAK),
    ('projects/tr-az-1600-main.jpg',     HV),
    ('projects/gallery/tr-az-1600-1.jpg',BUDAK),
    ('projects/gallery/tr-az-1600-2.jpg',HV),
    ('projects/tr-ru-main.jpg',          BUDAK),
    ('projects/gallery/tr-ru-1.jpg',     HV),
    ('projects/gallery/tr-ru-2.jpg',     BUDAK),
]

for rel, url in todo:
    dest = BASE + rel
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f'  [skip] {rel}')
        continue
    time.sleep(5)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, 'wb') as f:
            f.write(r.read())
        print(f'  [ok]   {rel}')
    except Exception as e:
        print(f'  [err]  {rel}: {e}')

import subprocess
subprocess.run(['chown', '-R', 'vaam:www-data', '/home/vaam/app/media/projects'], check=False)
subprocess.run(['find', '/home/vaam/app/media/projects', '-type', 'f', '-exec', 'chmod', '644', '{}', ';'], check=False)
subprocess.run(['find', '/home/vaam/app/media/projects', '-type', 'd', '-exec', 'chmod', '755', '{}', ';'], check=False)
print('Done.')
