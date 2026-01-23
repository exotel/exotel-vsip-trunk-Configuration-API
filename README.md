# Exotel SIP Trunking APIs

Connect your PBX or Contact Center to the telephone network.

---

## Quick Setup

### Step 1: Create Trunk (Required for all use cases)

```bash
curl -X POST "https://api.in.exotel.com/v2/accounts/<account_sid>/trunks" \
  -u "<api_key>:<api_token>" \
  -H "Content-Type: application/json" \
  -d '{"trunk_name": "my_trunk", "nso_code": "ANY-ANY", "domain_name": "<account_sid>.pstn.exotel.com"}'
```

Save `trunk_sid` from response.

---

### Step 2: Choose Your Use Case

| Use Case | What it does | Next Step |
|----------|--------------|-----------|
| **Outbound** | Make calls to phone numbers | → Map Number + Whitelist IP |
| **Inbound** | Receive calls from phone numbers | → Map Number + Add Destination |
| **StreamKit** | Connect to Voice AI bots | → Map Number (flow mode) + Whitelist IP |

---

## Outbound (Your System → PSTN)

```bash
# Map phone number
curl -X POST ".../trunks/<trunk_sid>/phone-numbers" \
  -d '{"phone_number": "<your_exophone>", "mode": "pstn"}'

# Whitelist your server IP
curl -X POST ".../trunks/<trunk_sid>/whitelisted-ips" \
  -d '{"ip": "<your_server_ip>", "mask": 32}'

# Get SIP credentials for your PBX
curl -X GET ".../trunks/<trunk_sid>/credentials"
```

---

## Inbound (PSTN → Your System)

```bash
# Map phone number
curl -X POST ".../trunks/<trunk_sid>/phone-numbers" \
  -d '{"phone_number": "<your_exophone>"}'

# Add destination (where calls go)
curl -X POST ".../trunks/<trunk_sid>/destination-uris" \
  -d '{"destinations": [{"destination": "<your_server>:<port>;transport=tls"}]}'
```

---

## StreamKit (Your System → Voice AI)

```bash
# Map phone number with flow mode
curl -X POST ".../trunks/<trunk_sid>/phone-numbers" \
  -d '{"phone_number": "<your_exophone>", "mode": "flow"}'

# Whitelist your server IP
curl -X POST ".../trunks/<trunk_sid>/whitelisted-ips" \
  -d '{"ip": "<your_server_ip>", "mask": 32}'

# Get SIP credentials
curl -X GET ".../trunks/<trunk_sid>/credentials"
```

---

## Settings & Management

```bash
# Change mode (pstn ↔ flow)
curl -X PUT ".../trunks/<trunk_sid>/phone-numbers/<id>" \
  -d '{"phone_number": "<number>", "mode": "flow"}'

# Set caller ID alias
curl -X POST ".../trunks/<trunk_sid>/settings" \
  -d '{"settings": [{"name": "trunk_external_alias", "value": "<number>"}]}'

# View configurations
curl -X GET ".../trunks/<trunk_sid>/phone-numbers"
curl -X GET ".../trunks/<trunk_sid>/whitelisted-ips"
curl -X GET ".../trunks/<trunk_sid>/destination-uris"

# Delete trunk
curl -X DELETE ".../trunks?trunk_sid=<trunk_sid>"
```

---

## Authentication

```
Base URL: https://api.in.exotel.com/v2/accounts/<account_sid>
Auth: HTTP Basic (api_key:api_token)
Rate Limit: 200 requests/minute
```

---

## Resources

| Resource | Description |
|----------|-------------|
| [API Reference](docs/API_REFERENCE.md) | Full request/response details |
| [SIP Guide](docs/SIP_TRUNKING_GUIDE.md) | Concepts & troubleshooting |
| [Postman](postman/Exotel_SIP_Trunking_APIs.json) | Import & test APIs |

---

## Support

https://developer.exotel.com | support@exotel.com
