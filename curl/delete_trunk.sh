#!/usr/bin/env bash

# ============================================================================
# DELETE TRUNK
# ⚠️ PERMANENTLY deletes the trunk and ALL its configurations
# This action CANNOT be undone!
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

echo "⚠️  WARNING: This will PERMANENTLY delete trunk: ${TRUNK_SID}"
echo "    All phone numbers, whitelisted IPs, and destination URIs will be removed!"
read -p "Are you sure? Type 'yes' to confirm: " confirm

if [[ "$confirm" == "yes" ]]; then
  curl -X DELETE "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks?trunk_sid=${TRUNK_SID}"
  echo ""
else
  echo "Cancelled."
fi
