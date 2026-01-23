#!/usr/bin/env bash

# ============================================================================
# UPDATE PHONE NUMBER MODE
# Switch between PSTN and Flow (StreamKit) mode
# ============================================================================
# MODE OPTIONS:
#   pstn - Routes calls to telephone network (PSTN)
#   flow - Routes calls to Voice AI bot (StreamKit)
# ============================================================================
# IMPORTANT: The PHONE_NUMBER_ID is the numeric ID returned when you mapped
# the phone number (e.g., 41523), NOT the phone number itself!
# ============================================================================

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Required variables
: "${API_KEY:?Error: API_KEY is required}"
: "${API_TOKEN:?Error: API_TOKEN is required}"
: "${ACCOUNT_SID:?Error: ACCOUNT_SID is required}"
: "${TRUNK_SID:?Error: TRUNK_SID is required}"
: "${PHONE_NUMBER_ID:?Error: PHONE_NUMBER_ID is required (numeric ID from map response, e.g., 41523)}"
: "${PHONE_NUMBER:?Error: PHONE_NUMBER is required (E.164 format)}"
: "${MODE:?Error: MODE is required (pstn or flow)}"

# Optional: defaults
SUBDOMAIN="${SUBDOMAIN:-api.in.exotel.com}"

echo "Updating phone number ${PHONE_NUMBER} to mode: ${MODE}"

curl -X PUT "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/phone-numbers/${PHONE_NUMBER_ID}" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone_number\": \"${PHONE_NUMBER}\",
    \"mode\": \"${MODE}\"
  }"

echo ""
