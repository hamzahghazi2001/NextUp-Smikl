import os
import hashlib
import requests
from dotenv import load_dotenv

# Force .env values to replace any stale Windows/PowerShell variables
load_dotenv(override=True)

client_id = os.getenv("SIMKL_CLIENT_ID", "").strip()
access_token = os.getenv("SIMKL_ACCESS_TOKEN", "").strip()

if not client_id:
    raise SystemExit("Missing SIMKL_CLIENT_ID")

if not access_token:
    raise SystemExit("Missing SIMKL_ACCESS_TOKEN")


# Safe fingerprint so we can tell which token is actually being loaded
token_fingerprint = hashlib.sha256(
    access_token.encode()
).hexdigest()[:12]

print("client_id length:", len(client_id))
print("access token length:", len(access_token))
print("token fingerprint:", token_fingerprint)
print()


url = "https://api.simkl.com/sync/all-items/shows"

params = {
    "client_id": client_id,
    "app-name": "nextup",
    "app-version": "0.1",
    "next_watch_info": "yes",
}

headers = {
    "User-Agent": "nextup-dev/0.1",
    "Authorization": f"Bearer {access_token}",
}

response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=15,
)

print("status:", response.status_code)
print("url:", response.url)
print("content-type:", response.headers.get("Content-Type"))
print()

try:
    print(response.json())
except ValueError:
    print(response.text[:1000])