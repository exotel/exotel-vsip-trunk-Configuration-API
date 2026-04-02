#!/usr/bin/env bash
# SIP digest credentials — Voice AI / Streamkit (dynamic IPs). Needs TRUNK_SID, SIP_CRED_PASSWORD.
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi
[ -z "$TRUNK_SID" ] || [ -z "$SIP_CRED_PASSWORD" ] && echo "Error: TRUNK_SID and SIP_CRED_PASSWORD required" && exit 1
UN="${SIP_CRED_USERNAME:-voice_ai_user}"
FN="${SIP_CRED_FRIENDLY_NAME:-streamkit}"
curl -sS -X POST "https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_API_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d "{\"user_name\":\"${UN}\",\"password\":\"${SIP_CRED_PASSWORD}\",\"friendly_name\":\"${FN}\"}"
