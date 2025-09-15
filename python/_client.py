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

def post(path, payload):
    """Make a POST request to the Exotel API"""
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            BASE + path, 
            data=data, 
            headers={'Content-Type': 'application/json'}, 
            method='POST'
        )
        
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            print(body)
            return json.loads(body)
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(e.read().decode('utf-8'))
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def get(path):
    """Make a GET request to the Exotel API"""
    try:
        req = urllib.request.Request(
            BASE + path, 
            headers={'Content-Type': 'application/json'}, 
            method='GET'
        )
        
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            print(body)
            return json.loads(body)
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(e.read().decode('utf-8'))
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def delete(path):
    """Make a DELETE request to the Exotel API"""
    try:
        req = urllib.request.Request(
            BASE + path, 
            headers={'Content-Type': 'application/json'}, 
            method='DELETE'
        )
        
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            print(body)
            return json.loads(body) if body else {}
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(e.read().decode('utf-8'))
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 