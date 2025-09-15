#!/usr/bin/env python3

from _client import get
import os

# Get phone numbers for a trunk (same endpoint as destination-uris)
trunk_sid = os.getenv('TRUNK_SID')
if not trunk_sid:
    print("Error: TRUNK_SID environment variable is required")
    exit(1)

print(f"Getting phone numbers for trunk {trunk_sid}...")
result = get(f'/trunks/{trunk_sid}/destination-uris')
print("Phone numbers retrieved successfully!") 