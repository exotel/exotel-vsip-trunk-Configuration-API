#!/usr/bin/env bash
# DELETE uses query ?id= (not path)
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi
[ -z "$TRUNK_SID" ] || [ -z "$CREDENTIAL_ID" ] && echo "Error: TRUNK_SID and CREDENTIAL_ID required" && exit 1
curl -sS -X DELETE "https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_API_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials?id=${CREDENTIAL_ID}"
