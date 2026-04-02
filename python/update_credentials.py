#!/usr/bin/env python3
"""Update credential by id (path). Optional user_name, password, friendly_name in body."""
from _client import put
import os

trunk = os.environ.get("TRUNK_SID")
cid = os.environ.get("CREDENTIAL_ID")
if not trunk or not cid:
    print("Error: TRUNK_SID and CREDENTIAL_ID required")
    exit(1)

body = {}
if os.getenv("SIP_CRED_FRIENDLY_NAME"):
    body["friendly_name"] = os.getenv("SIP_CRED_FRIENDLY_NAME")
if os.getenv("SIP_CRED_USERNAME"):
    body["user_name"] = os.getenv("SIP_CRED_USERNAME")
if os.getenv("SIP_CRED_PASSWORD"):
    body["password"] = os.getenv("SIP_CRED_PASSWORD")
if not body:
    body["friendly_name"] = os.getenv("SIP_CRED_FRIENDLY_NAME", "updated_label")

print("Updating credential...")
put(f"/trunks/{trunk}/credentials/{cid}", body)
