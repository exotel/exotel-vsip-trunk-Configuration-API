#!/usr/bin/env python3
"""List vSIP trunks (manage / view). Optional: PAGE_SIZE, PAGE_OFFSET, TRUNK_SID filter via query."""
from _client import get
import os

q = {}
if os.getenv("PAGE_SIZE"):
    q["page_size"] = os.getenv("PAGE_SIZE")
if os.getenv("PAGE_OFFSET"):
    q["offset"] = os.getenv("PAGE_OFFSET")
if os.getenv("TRUNK_SID"):
    q["trunk_sid"] = os.getenv("TRUNK_SID")

print("Listing trunks...")
get("/trunks", query=q or None)
