#!/usr/bin/env python3
"""List or fetch SIP credentials for a trunk. Optional CREDENTIAL_ID for single row."""
from _client import get
import os

trunk = os.environ.get("TRUNK_SID")
if not trunk:
    print("Error: TRUNK_SID required")
    exit(1)

q = {}
if os.getenv("PAGE_SIZE"):
    q["page_size"] = os.getenv("PAGE_SIZE")
if os.getenv("PAGE_OFFSET"):
    q["offset"] = os.getenv("PAGE_OFFSET")
if os.getenv("CREDENTIAL_ID"):
    q["id"] = os.getenv("CREDENTIAL_ID")

print("Listing credentials...")
get(f"/trunks/{trunk}/credentials", query=q or None)
