import requests

lines = open('.env.canva').readlines()
token = [l.split('=',1)[1].strip() for l in lines if l.startswith('CANVA_API_KEY=')][0]
h = {'Authorization': f'Bearer {token}'}

ids = ['DAHDvlsbcXg','DAHDvg5c3cM','DAHDvvdsB9s','DAHDvgaEX2w','DAHDvlxkBnY']
names = ['Primary Logo','Horizontal','Favicon','Dark Version','Business Card']

for i, did in enumerate(ids):
    r = requests.get(f'https://api.canva.com/rest/v1/designs/{did}', headers=h)
    print(f'{names[i]}: status={r.status_code}')
    if r.status_code == 200:
        d = r.json().get('design', {})
        title = d.get('title', 'N/A')
        url = d.get('urls', {}).get('edit_url', 'N/A')
        print(f'  Title: {title}')
        print(f'  URL: {url[:150]}')
    else:
        print(f'  Error: {r.text[:200]}')
    print()
