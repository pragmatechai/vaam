"""
Canva Token Refresh Script
Usage: python refresh_canva_token.py YOUR_CLIENT_SECRET
"""
import requests, base64, urllib.parse, sys, os

if len(sys.argv) < 2:
    print("Usage: python refresh_canva_token.py YOUR_CLIENT_SECRET")
    sys.exit(1)

client_id = 'OC-AZzhAjgsUwy2'
client_secret = sys.argv[1]

with open('.env.canva', 'r') as f:
    lines = f.read().strip().split('\n')

refresh_token = ''
for line in lines:
    if line.startswith('CANVA_REFRESH_TOKEN='):
        refresh_token = line.split('=', 1)[1]

credentials = f'{urllib.parse.quote(client_id)}:{urllib.parse.quote(client_secret)}'
basic_auth = base64.b64encode(credentials.encode()).decode()

response = requests.post(
    'https://api.canva.com/rest/v1/oauth/token',
    data=urllib.parse.urlencode({
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }),
    headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {basic_auth}',
    },
)

if response.status_code == 200:
    data = response.json()
    new_access = data.get('access_token', '')
    new_refresh = data.get('refresh_token', refresh_token)
    with open('.env.canva', 'w') as f:
        f.write(f'CANVA_APP_ID={client_id}\n')
        f.write(f'CANVA_API_KEY={new_access}\n')
        f.write(f'CANVA_REFRESH_TOKEN={new_refresh}\n')
    print(f'SUCCESS! Token refreshed.')
else:
    print(f'ERROR: {response.status_code} - {response.text}')
