#!/usr/bin/env bash

# ============================================================================
# ADD DESTINATION URI
# Configures where incoming calls are routed (your PBX/server)
# Required for: Inbound/Origination calls
# ============================================================================
# IMPORTANT:
# - For IP addresses: You MUST whitelist the IP first!
# - For FQDNs (e.g., sip.company.com): No whitelisting required
# ============================================================================

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Required variables
: "${API_KEY:?Error: API_KEY is required}"
: "${API_TOKEN:?Error: API_TOKEN is required}"
: "${ACCOUNT_SID:?Error: ACCOUNT_SID is required}"
: "${TRUNK_SID:?Error: TRUNK_SID is required}"
: "${DESTINATION:?Error: DESTINATION is required (IP or FQDN)}"

# Optional: defaults
SUBDOMAIN="${SUBDOMAIN:-api.in.exotel.com}"
PORT="${PORT:-5061}"
TRANSPORT="${TRANSPORT:-tls}"  # tls (recommended) or tcp

echo "Adding destination: ${DESTINATION}:${PORT};transport=${TRANSPORT}"

curl -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d "{
    \"destinations\": [
      {
        \"destination\": \"${DESTINATION}:${PORT};transport=${TRANSPORT}\"
      }
    ]
  }"

echo ""
