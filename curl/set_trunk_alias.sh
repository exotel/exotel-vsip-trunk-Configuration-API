#!/usr/bin/env bash

# ============================================================================
# SET TRUNK ALIAS (CALLER ID)
# Sets the phone number displayed to called parties on outbound calls
# ============================================================================

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Required variables
: "${API_KEY:?Error: API_KEY is required}"
: "${API_TOKEN:?Error: API_TOKEN is required}"
: "${ACCOUNT_SID:?Error: ACCOUNT_SID is required}"
: "${TRUNK_SID:?Error: TRUNK_SID is required}"
: "${CALLER_ID:?Error: CALLER_ID is required (E.164 format, e.g., +919876543210)}"

# Optional: defaults
SUBDOMAIN="${SUBDOMAIN:-api.in.exotel.com}"

echo "Setting caller ID alias: ${CALLER_ID}"

curl -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/settings" \
  -H "Content-Type: application/json" \
  -d "{
    \"settings\": [
      {
        \"name\": \"trunk_external_alias\",
        \"value\": \"${CALLER_ID}\"
      }
    ]
  }"

echo ""
