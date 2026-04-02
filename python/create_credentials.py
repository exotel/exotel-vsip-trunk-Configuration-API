#!/usr/bin/env python3
"""Create SIP digest credentials on a trunk — Voice AI / Streamkit-style (dynamic source IPs). Requires TRUNK_SID."""
from _client import post
import os

trunk = os.environ.get("TRUNK_SID")
if not trunk:
    print("Error: TRUNK_SID required")
    exit(1)

body = {
    "user_name": os.getenv("SIP_CRED_USERNAME", "voice_ai_user"),
    "password": os.getenv("SIP_CRED_PASSWORD", ""),
    "friendly_name": os.getenv("SIP_CRED_FRIENDLY_NAME", "streamkit"),
}
if not body["password"]:
    print("Error: set SIP_CRED_PASSWORD")
    exit(1)

print("Creating SIP credentials...")
post(f"/trunks/{trunk}/credentials", body)
