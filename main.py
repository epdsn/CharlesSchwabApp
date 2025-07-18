import base64
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

appKey = os.getenv('SCHWAB_APP_KEY')
appSecret = os.getenv('SCHWAB_APP_SECRET')
redirect_uri = os.getenv('SCHWAB_REDIRECT_URI')

auhthUrl = f'https://api.schwabapi.com/v1/oauth/authorize?client_id={appKey}&redirect_uri={redirect_uri}&state=12345'
print(f"Click to authenticate: {auhthUrl}")

returnedLink = input("Paste the redirect URL here and press Enter: ")

code = f"{returnedLink[returnedLink.index('code=')+5:returnedLink.index('%40')]}@"

headers = {
    'Authorization': f'Basic {base64.b64encode(bytes(f"{appKey}:{appSecret}", "utf-8")).decode("utf-8")}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}

response = requests.post('https://api.schwabapi.com/v1/oauth/token', headers=headers, data=data)

print(f"Token response status: {response.status_code}")
print(f"Token response: {response.text}")

tokenDictionary = response.json()

accessToken = tokenDictionary['access_token']
refreshToken = tokenDictionary['refresh_token']

base_url = "https://api.schwabapi.com/trader/v1/"

response = requests.get(
    f"{base_url}accounts/accountNumbers",
    headers={'Authorization': f'Bearer {accessToken}'}
)

print(f"Account API response status: {response.status_code}")
print(f"Account API response text: {response.text}")
if response.status_code == 200:
    print(response.json()) 