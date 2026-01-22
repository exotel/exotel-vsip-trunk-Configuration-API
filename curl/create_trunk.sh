#!/usr/bin/env bash

# Create Trunk API
# Creates a virtual connection between your system and Exotel's PSTN gateway

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Validate required variables
: "${your_api_key:?Error: your_api_key is required}"
: "${your_api_token:?Error: your_api_token is required}"
: "${subdomain:?Error: subdomain is required (e.g., api.in.exotel.com)}"
: "${your_sid:?Error: your_sid is required}"

curl -X POST "https://${your_api_key}:${your_api_token}@${subdomain}/v2/accounts/${your_sid}/trunks" \
  -H "Content-Type: application/json" \
  -d "{
    \"trunk_name\": \"${trunk_name:-my_trunk}\",
    \"nso_code\": \"${nso_code:-ANY-ANY}\",
    \"domain_name\": \"${your_sid}.pstn.exotel.com\"
  }"
