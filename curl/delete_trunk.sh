#!/usr/bin/env bash

# Delete Trunk API
# ⚠️ PERMANENTLY deletes the trunk and ALL configurations

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Validate required variables
: "${your_api_key:?Error: your_api_key is required}"
: "${your_api_token:?Error: your_api_token is required}"
: "${subdomain:?Error: subdomain is required}"
: "${your_sid:?Error: your_sid is required}"
: "${trunk_sid:?Error: trunk_sid is required}"

echo "⚠️  WARNING: This will permanently delete trunk: ${trunk_sid}"
read -p "Are you sure? (y/N): " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
  curl -X DELETE "https://${your_api_key}:${your_api_token}@${subdomain}/v2/accounts/${your_sid}/trunks?trunk_sid=${trunk_sid}" \
    -H "Content-Type: application/json"
else
  echo "Cancelled."
fi
 