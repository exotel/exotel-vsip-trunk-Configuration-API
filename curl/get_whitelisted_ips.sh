#!/usr/bin/env bash

# ============================================================================
# GET WHITELISTED IPs
# Lists all whitelisted IP addresses for the trunk
# ============================================================================

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Required variables
: "${API_KEY:?Error: API_KEY is required}"
: "${API_TOKEN:?Error: API_TOKEN is required}"
: "${ACCOUNT_SID:?Error: ACCOUNT_SID is required}"
: "${TRUNK_SID:?Error: TRUNK_SID is required}"

# Optional: defaults
SUBDOMAIN="${SUBDOMAIN:-api.in.exotel.com}"

curl -X GET "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips"

echo ""
