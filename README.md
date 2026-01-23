# Exotel SIP Trunking APIs

Connect your PBX or Contact Center to the telephone network.

---

## Quick Start

### 1. Get Your Credentials

From Exotel Dashboard → API Credentials:
- **API Key** (username)
- **API Token** (password)
- **Account SID**

### 2. Choose Your Use Case

| Use Case | Description | Steps |
|----------|-------------|-------|
| **PSTN (Standard)** | Make & receive calls via telephone network | Create Trunk → Map DID → Whitelist IP → Add Destination |
| **StreamKit (Voice AI)** | Connect to Voice AI bots | Create Trunk → Map DID (mode: flow) → Whitelist IP |

---

## PSTN Setup (Outbound + Inbound)

### Step 1: Create Trunk

```bash
curl -X POST "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "my_trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "ACCOUNT_SID.pstn.exotel.com"
  }'
```

**Save `trunk_sid` from response!**

### Step 2: Map Phone Number

```bash
curl -X POST "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks/TRUNK_SID/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210"
  }'
```

**Save `id` from response** (needed for Update Mode API).

### Step 3: Whitelist IP (for Outbound/Termination)

```bash
curl -X POST "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks/TRUNK_SID/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "YOUR_SERVER_IP",
    "mask": 32
  }'
```

### Step 4: Add Destination URI (for Inbound/Origination)

> **Important:** If using an IP address, whitelist it first (Step 3). FQDNs don't need whitelisting.

```bash
curl -X POST "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks/TRUNK_SID/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {
        "destination": "YOUR_SERVER_IP:5061;transport=tls"
      }
    ]
  }'
```

---

## StreamKit Setup (Voice AI)

For connecting your Contact Center to Voice AI bots.

### Step 1: Create Trunk

Same as PSTN Step 1.

### Step 2: Map Phone Number (Flow Mode)

```bash
curl -X POST "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks/TRUNK_SID/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

> **Note:** `mode: flow` routes calls to Voice AI bot instead of PSTN.

### Step 3: Whitelist IP

Same as PSTN Step 3.

---

## Manage & View

### Update Phone Number Mode (pstn ↔ flow)

```bash
curl -X PUT "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks/TRUNK_SID/phone-numbers/PHONE_NUMBER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

> **Note:** `PHONE_NUMBER_ID` is the numeric ID (e.g., `41523`) from Map Phone Number response, NOT the phone number!

### Set Caller ID (for Outbound)

```bash
curl -X POST "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks/TRUNK_SID/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "settings": [
      {
        "name": "trunk_external_alias",
        "value": "+919876543210"
      }
    ]
  }'
```

### View Configurations

```bash
# Get phone numbers
curl -X GET "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks/TRUNK_SID/phone-numbers"

# Get whitelisted IPs
curl -X GET "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks/TRUNK_SID/whitelisted-ips"

# Get destination URIs
curl -X GET "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks/TRUNK_SID/destination-uris"
```

### Delete Trunk

```bash
curl -X DELETE "https://API_KEY:API_TOKEN@api.in.exotel.com/v2/accounts/ACCOUNT_SID/trunks?trunk_sid=TRUNK_SID"
```

---

## Authentication

| Setting | Value |
|---------|-------|
| Base URL | `https://api.in.exotel.com` |
| Auth | HTTP Basic (`API_KEY:API_TOKEN`) |
| Content-Type | `application/json` |
| Rate Limit | 200 requests/minute |

---

## Mode Options

| Mode | Description |
|------|-------------|
| `pstn` | Routes calls to telephone network (default) |
| `flow` | Routes calls to Voice AI bot (StreamKit) |

---

## Resources

| Resource | Description |
|----------|-------------|
| [API Reference](docs/API_REFERENCE.md) | Full request/response details with examples |
| [SIP Guide](docs/SIP_TRUNKING_GUIDE.md) | Concepts, troubleshooting, PBX config |
| [Postman Collection](postman/Exotel_SIP_Trunking_APIs.json) | Import & test APIs |
| [curl Scripts](curl/) | Ready-to-use bash scripts |

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| HTTP 415 | Wrong content type | Use `Content-Type: application/json` |
| "Destination not whitelisted" | IP not whitelisted | Whitelist IP before adding as destination |
| Duplicate resource (1008) | Already exists | Use different name/IP or delete existing |

---

## Support

- Documentation: https://developer.exotel.com
- Email: support@exotel.com
