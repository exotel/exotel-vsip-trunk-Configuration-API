#!/usr/bin/env python3
"""Delete credential — query param id= (not path). Requires TRUNK_SID, CREDENTIAL_ID."""
from _client import delete
import os

trunk = os.environ.get("TRUNK_SID")
cid = os.environ.get("CREDENTIAL_ID")
if not trunk or not cid:
    print("Error: TRUNK_SID and CREDENTIAL_ID required")
    exit(1)

print("Deleting credential...")
delete(f"/trunks/{trunk}/credentials", query={"id": cid})
