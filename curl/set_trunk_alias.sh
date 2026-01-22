#!/usr/bin/env bash

# Set Trunk Alias API
# Sets an external Caller ID alias for the trunk

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Validate required variables
: "${your_api_key:?Error: your_api_key is required}"
: "${your_api_token:?Error: your_api_token is required}"
: "${subdomain:?Error: subdomain is required}"
: "${your_sid:?Error: your_sid is required}"
: "${trunk_sid:?Error: trunk_sid is required}"
: "${phone_number:?Error: phone_number is required}"

curl -X POST "https://${your_api_key}:${your_api_token}@${subdomain}/v2/accounts/${your_sid}/trunks/${trunk_sid}/settings" \
  -H "Content-Type: application/json" \
  -d "{
    \"settings\": [
      { \"name\": \"trunk_external_alias\", \"value\": \"${phone_number}\" }
    ]
  }"
