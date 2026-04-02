#!/usr/bin/env bash
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi
[ -z "$TRUNK_SID" ] && echo "Error: TRUNK_SID required" && exit 1
args=()
[ -n "$PAGE_SIZE" ] && args+=("page_size=${PAGE_SIZE}")
[ -n "$PAGE_OFFSET" ] && args+=("offset=${PAGE_OFFSET}")
[ -n "$CREDENTIAL_ID" ] && args+=("id=${CREDENTIAL_ID}")
QS=$(IFS='&'; echo "${args[*]}")
URL="https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_API_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials"
[ -n "$QS" ] && URL="${URL}?${QS}"
curl -sS "$URL"
