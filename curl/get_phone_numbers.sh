#!/usr/bin/env bash

# Get Phone Numbers API
# Retrieves all phone numbers mapped to a trunk

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Validate required variables
: "${your_api_key:?Error: your_api_key is required}"
: "${your_api_token:?Error: your_api_token is required}"
: "${subdomain:?Error: subdomain is required}"
: "${your_sid:?Error: your_sid is required}"
: "${trunk_sid:?Error: trunk_sid is required}"

curl -X GET "https://${your_api_key}:${your_api_token}@${subdomain}/v2/accounts/${your_sid}/trunks/${trunk_sid}/phone-numbers" \
  -H "Content-Type: application/json"
