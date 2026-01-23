#!/usr/bin/env bash

# Update Phone Number Mode
# Use this to switch between PSTN and Flow mode

# Source environment variables
if [ -f "../.env" ]; then
    source ../.env
elif [ -f ".env" ]; then
    source .env
fi

# Check required environment variables
if [ -z "$EXO_AUTH_KEY" ] || [ -z "$EXO_AUTH_TOKEN" ] || [ -z "$EXO_SUBSCRIBIX_DOMAIN" ] || [ -z "$EXO_ACCOUNT_SID" ]; then
    echo "Error: Missing required environment variables. Please check your .env file."
    exit 1
fi

if [ -z "$TRUNK_SID" ]; then
    echo "Error: TRUNK_SID is required."
    exit 1
fi

if [ -z "$PHONE_NUMBER_ID" ]; then
    echo "Error: PHONE_NUMBER_ID is required."
    exit 1
fi

if [ -z "$PHONE_NUMBER" ]; then
    echo "Error: PHONE_NUMBER is required."
    exit 1
fi

# Default mode is pstn, can be overridden with MODE=flow
MODE=${MODE:-pstn}

curl --location --request PUT "https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_SUBSCRIBIX_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}/trunks/${TRUNK_SID}/phone-numbers/${PHONE_NUMBER_ID}" \
  --header 'Content-Type: application/json' \
  --data-raw "{
  \"phone_number\": \"${PHONE_NUMBER}\",
  \"mode\": \"${MODE}\"
}"
