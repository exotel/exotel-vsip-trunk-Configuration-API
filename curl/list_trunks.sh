#!/usr/bin/env bash
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi
[ -z "$EXO_AUTH_KEY" ] && echo "Error: missing .env" && exit 1
args=()
[ -n "$PAGE_SIZE" ] && args+=("page_size=${PAGE_SIZE}")
[ -n "$PAGE_OFFSET" ] && args+=("offset=${PAGE_OFFSET}")
[ -n "$TRUNK_SID" ] && args+=("trunk_sid=${TRUNK_SID}")
QS=$(IFS='&'; echo "${args[*]}")
URL="https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_API_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}/trunks"
[ -n "$QS" ] && URL="${URL}?${QS}"
curl -sS "$URL"
