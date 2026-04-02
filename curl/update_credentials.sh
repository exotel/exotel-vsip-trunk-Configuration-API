#!/usr/bin/env bash
# PUT /credentials/{id} — body uses friendly_name by default; set SIP_CRED_USERNAME / SIP_CRED_PASSWORD to rotate.
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi
[ -z "$TRUNK_SID" ] || [ -z "$CREDENTIAL_ID" ] && echo "Error: TRUNK_SID and CREDENTIAL_ID required" && exit 1
FN="${SIP_CRED_FRIENDLY_NAME:-updated_label}"
BODY="{\"friendly_name\":\"${FN}\"}"
curl -sS -X PUT "https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_API_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials/${CREDENTIAL_ID}" \
  -H "Content-Type: application/json" -d "$BODY"
