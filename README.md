# Exotel SIP Trunking APIs

Connect your PBX, Contact Center, or Voice AI system to the telephone network.

---

## Quick Start

### 1. Get Your Credentials

SignUp: https://my.in.exotel.com/auth/register

Complete KYC as per compliance: https://docs.exotel.com/business-phone-system/kyc-verification

Exotel Dashboard → API Credentials:https://my.in.exotel.com/apisettings/site#api-credentials

Purchase Exophone: https://my.in.exotel.com/numbers

- **API Key** (username)
- **API Token** (password)
- **Account SID**

### 2. Choose Your Use Case

| Use Case | Description | Setup Steps |
|----------|-------------|-------------|
| **PSTN (Standard)** | Make & receive calls via telephone network | Create Trunk → Map Phone Number → Map ACL → Map Destination URI |
| **StreamKit (Voice AI)** | Connect to Voice AI bots | Create Trunk → Map Phone Number (mode: flow) → Map ACL |

---

## PSTN Setup (Outbound + Inbound)

### Step 1: Create Trunk

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "my_trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "<your_sid>.pstn.exotel.com"
  }'
```

**Save `trunk_sid` from response!**

### Step 2: Map Phone Number to Trunk

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210"
  }'
```

**Save `id` from response** (needed for Update Mode API).

### Step 3: Map ACL to Trunk (for Outbound/Termination)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "<your_server_ip>",
    "mask": 32
  }'
```

### Step 4: Map Destination URI to Trunk (for Inbound/Origination)

> **Important:** For IP destinations, map ACL first (Step 3). FQDNs don't need ACL mapping.

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {
        "destination": "<your_server_ip>:5061;transport=tls"
      }
    ]
  }'
```
### Step 5: for Inbound SIP 

a. Create a Flow using Connect Applet in App Bazaar: https://my.in.exotel.com/apps

b. Use sip:<TrunkID> in the Dial Whom field

c. Map DID to flow through Exophone: https://my.in.exotel.com/numbers

---

## StreamKit Setup (Voice AI)

For connecting your Contact Center to Voice AI bots.

### Step 1: Create Trunk

Same as PSTN Step 1.

### Step 2: Map Phone Number (Flow Mode)- Procure SIP Exophone from Account or contact support

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

> **Note:** `mode: flow` routes calls to Voice AI bot instead of PSTN.

### Step 3: Map ACL to Trunk

Same as PSTN Step 3.

### Step 4: Build FLow nd Map DID

a. Follow https://docs.exotel.com/exotel-agentstream/streamkit-cloud for end-to-end steps

b. Create flow in AppBazaar with Voicebot applet https://my.in.exotel.com/apps

b. Map DID to flow through Exophone: https://my.in.exotel.com/numbers

---

## Manage & View

### Update Phone Number Mode (pstn ↔ flow)

```bash
curl -X PUT "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers/<phone_number_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

> **Note:** `<phone_number_id>` is the numeric ID (e.g., `41523`) from Map Phone Number response, NOT the phone number!

### Set Trunk Alias (Caller ID for Outbound)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/settings" \
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
curl -X GET "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers"

# Get ACLs (whitelisted IPs)
curl -X GET "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips"

# Get destination URIs
curl -X GET "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris"
```

### Delete Trunk

```bash
curl -X DELETE "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks?trunk_sid=<trunk_sid>"
```

---

## Authentication

| Setting | Value |
|---------|-------|
| Base URL | `https://<subdomain>` |
| Subdomain (India) | `api.in.exotel.com` |
| Subdomain (Singapore) | `api.exotel.com` |
| Auth | HTTP Basic (`<api_key>:<api_token>`) |
| Content-Type | `application/json` |
| Rate Limit | 200 requests/minute |

---

## Mode Options

| Mode | Description |
|------|-------------|
| `pstn` | Routes calls to telephone network (default) |
| `flow` | Routes calls to Voice AI bot (StreamKit) |

Configure the network and firewall on your SIP system side to receive or send an invite from Exotel

Follow Exotel SIP Network and configuration Guide :https://docs.exotel.com/dynamic-sip-trunking
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
| "Destination not whitelisted" | IP not in ACL | Map ACL before mapping as destination |
| Duplicate resource (1008) | Already exists | Use different name/IP or delete existing |

---

## Support

- Documentation: https://developer.exotel.com
- Email: support@exotel.com
