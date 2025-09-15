#!/usr/bin/env python3

from _client import delete
import os

# Delete a trunk
trunk_sid = os.getenv('TRUNK_SID')
if not trunk_sid:
    print("Error: TRUNK_SID environment variable is required")
    exit(1)

print(f"Deleting trunk {trunk_sid}...")
result = delete(f'/trunks?trunk_sid={trunk_sid}')
print("Trunk deleted successfully!") 