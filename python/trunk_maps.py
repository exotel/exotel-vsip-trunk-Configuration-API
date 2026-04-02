#!/usr/bin/env python3
"""Trunk map lookup: which trunk is tied to a virtual number (exophone). Requires DID_NUMBER or EXOPHONE."""
from _client import get
import os

ex = os.getenv("EXOPHONE") or os.getenv("DID_NUMBER")
if not ex:
    print("Error: set EXOPHONE or DID_NUMBER")
    exit(1)

q = {"exophone": ex}
if os.getenv("TRUNK_SID"):
    q["trunk_sid"] = os.getenv("TRUNK_SID")

print("Trunk map lookup...")
get("/trunk-maps", query=q)
