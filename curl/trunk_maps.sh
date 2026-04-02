#!/usr/bin/env bash
# Trunk map by exophone (set EXOPHONE or DID_NUMBER)
if [ -f "../.env" ]; then source ../.env; elif [ -f ".env" ]; then source .env; fi
EX="${EXOPHONE:-$DID_NUMBER}"
[ -z "$EX" ] && echo "Error: set EXOPHONE or DID_NUMBER" && exit 1
QS="exophone=${EX}"
[ -n "$TRUNK_SID" ] && QS="${QS}&trunk_sid=${TRUNK_SID}"
curl -sS "https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_SUBSCRIBIX_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}/trunk-maps?${QS}"
