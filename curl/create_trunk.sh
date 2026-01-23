#!/usr/bin/env bash

# ============================================================================
# CREATE TRUNK
# Creates a new SIP trunk - Required first step for all use cases
# ============================================================================

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Required variables
: "${API_KEY:?Error: API_KEY is required}"
: "${API_TOKEN:?Error: API_TOKEN is required}"
: "${ACCOUNT_SID:?Error: ACCOUNT_SID is required}"

# Optional: defaults
SUBDOMAIN="${SUBDOMAIN:-api.in.exotel.com}"
TRUNK_NAME="${TRUNK_NAME:-my_trunk}"

echo "Creating trunk: ${TRUNK_NAME}"

curl -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks" \
  -H "Content-Type: application/json" \
  -d "{
    \"trunk_name\": \"${TRUNK_NAME}\",
    \"nso_code\": \"ANY-ANY\",
    \"domain_name\": \"${ACCOUNT_SID}.pstn.exotel.com\"
  }"

echo ""
echo "✓ Save the trunk_sid from the response for subsequent API calls"
