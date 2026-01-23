#!/usr/bin/env bash

# ============================================================================
# MAP PHONE NUMBER (DID) TO TRUNK
# Associates a phone number with the trunk
# MODE: pstn (default) for PSTN calls, flow for StreamKit/Voice AI
# ============================================================================

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Required variables
: "${API_KEY:?Error: API_KEY is required}"
: "${API_TOKEN:?Error: API_TOKEN is required}"
: "${ACCOUNT_SID:?Error: ACCOUNT_SID is required}"
: "${TRUNK_SID:?Error: TRUNK_SID is required - create trunk first}"
: "${PHONE_NUMBER:?Error: PHONE_NUMBER is required (E.164 format, e.g., +919876543210)}"

# Optional: defaults
SUBDOMAIN="${SUBDOMAIN:-api.in.exotel.com}"
MODE="${MODE:-pstn}"  # pstn (default) or flow (for StreamKit)

echo "Mapping phone number: ${PHONE_NUMBER} with mode: ${MODE}"

curl -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/phone-numbers" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone_number\": \"${PHONE_NUMBER}\",
    \"mode\": \"${MODE}\"
  }"

echo ""
echo "✓ Save the 'id' from the response - needed for Update Phone Number API"
