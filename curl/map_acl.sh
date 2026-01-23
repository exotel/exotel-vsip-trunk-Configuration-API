#!/usr/bin/env bash

# ============================================================================
# MAP ACL TO TRUNK (Whitelist IP)
# Registers your server's public IP for authentication
# Required for: Outbound/Termination calls
# Note: Must whitelist IP BEFORE adding it as destination URI
# ============================================================================

# Load environment variables
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi

# Required variables
: "${API_KEY:?Error: API_KEY is required}"
: "${API_TOKEN:?Error: API_TOKEN is required}"
: "${ACCOUNT_SID:?Error: ACCOUNT_SID is required}"
: "${TRUNK_SID:?Error: TRUNK_SID is required}"
: "${SERVER_IP:?Error: SERVER_IP is required (your public IP address)}"

# Optional: defaults
SUBDOMAIN="${SUBDOMAIN:-api.in.exotel.com}"
MASK="${MASK:-32}"  # 32 = single IP, 24 = /24 subnet

echo "Mapping ACL (Whitelisting IP): ${SERVER_IP}/${MASK}"

curl -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d "{
    \"ip\": \"${SERVER_IP}\",
    \"mask\": ${MASK}
  }"

echo ""
