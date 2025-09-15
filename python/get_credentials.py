#!/usr/bin/env python3

from _client import get
import os

# Get credentials for a trunk
trunk_sid = os.getenv('TRUNK_SID')
if not trunk_sid:
    print("Error: TRUNK_SID environment variable is required")
    exit(1)

print(f"Getting credentials for trunk {trunk_sid}...")
result = get(f'/trunks/{trunk_sid}/credentials')
print("Credentials retrieved successfully!") 