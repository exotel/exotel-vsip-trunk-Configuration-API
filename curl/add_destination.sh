#!/usr/bin/env bash

# Add Destination URI API
# Tells Exotel where to send incoming calls
# Default: TLS on port 5061 (recommended)

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Validate required variables
: "${your_api_key:?Error: your_api_key is required}"
: "${your_api_token:?Error: your_api_token is required}"
: "${subdomain:?Error: subdomain is required}"
: "${your_sid:?Error: your_sid is required}"
: "${trunk_sid:?Error: trunk_sid is required}"
: "${your_server_ip:?Error: your_server_ip is required}"

# Defaults: TLS on port 5061
transport="${transport:-tls}"
dest_port="${dest_port:-5061}"

curl -X POST "https://${your_api_key}:${your_api_token}@${subdomain}/v2/accounts/${your_sid}/trunks/${trunk_sid}/destination-uris" \
  -H "Content-Type: application/json" \
  -d "{
    \"destinations\": [
      { \"destination\": \"${your_server_ip}:${dest_port};transport=${transport}\" }
    ]
  }"
