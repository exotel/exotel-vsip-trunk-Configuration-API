import os
import json
import urllib.request
import urllib.parse
import sys

# Build base URL from environment variables
def get_base_url():
    auth_key = os.environ.get('EXO_AUTH_KEY')
    auth_token = os.environ.get('EXO_AUTH_TOKEN')
    domain = os.environ.get('EXO_SUBSCRIBIX_DOMAIN')
    account_sid = os.environ.get('EXO_ACCOUNT_SID')
    
    if not all([auth_key, auth_token, domain, account_sid]):
        print("Error: Missing required environment variables (EXO_AUTH_KEY, EXO_AUTH_TOKEN, EXO_SUBSCRIBIX_DOMAIN, EXO_ACCOUNT_SID)")
        sys.exit(1)
    
    return f"https://{auth_key}:{auth_token}@{domain}/v2/accounts/{account_sid}"

BASE = get_base_url()

def _request(method, path, data=None, query=None):
    url = BASE + path
    if query:
        q = {k: v for k, v in query.items() if v is not None and str(v) != ''}
        if q:
            url += '?' + urllib.parse.urlencode(q)
    body = None
    headers = {}
    if data is not None:
        body = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode('utf-8')
            print(raw)
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(e.read().decode('utf-8'))
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def post(path, payload):
    return _request('POST', path, data=payload)

def get(path, query=None):
    return _request('GET', path, query=query)

def put(path, payload):
    return _request('PUT', path, data=payload)

def delete(path, query=None):
    return _request('DELETE', path, query=query)
