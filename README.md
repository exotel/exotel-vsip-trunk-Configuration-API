# Exotel Voice Trunking APIs

Connect your communication system to the telephone network using Exotel's Voice Trunking service.

---

> ⚠️ **Important:** FQDN/DNS routing is supported **only for Inbound / Origination (PSTN → SIP)**.  
> Outbound / Termination (SIP → PSTN) requires **static IP whitelisting**.

---

# Understanding Call Direction

## Terminology Reference

This documentation uses **both** terminologies so developers from any background can understand:

| Plain English | Telco Term | Direction | Connectivity |
|---------------|------------|-----------|--------------|
| **Outbound** | Termination | Your System → PSTN | Static IP only |
| **Inbound** | Origination | PSTN → Your System | IP or FQDN ✅ |

---

## Outbound / Termination (Your System → PSTN)

**You make calls to the phone network.**

```
┌─────────────────────┐
│ Your PBX / Bot / SBC│
└──────────┬──────────┘
           │  SIP (from static IP)
           ▼
┌─────────────────────┐
│       Exotel        │
└──────────┬──────────┘
           │  PSTN
           ▼
┌─────────────────────┐
│   Customer Phone    │
└─────────────────────┘
```

| Connectivity | Supported |
|--------------|-----------|
| Static public IP | ✅ Yes |
| FQDN / DNS | ❌ No |
| SIP REGISTER | ❌ No |

**Setup Flow:**
1. Create Trunk
2. Map Phone Number (Your Caller ID)
3. Whitelist Your Static IP

**Use Cases:** Sales calls, Click-to-call, Bot campaigns, Dialers

---

## Inbound / Origination (PSTN → Your System)

**You receive calls from the phone network.**

```
┌─────────────────────┐
│   Customer Phone    │
└──────────┬──────────┘
           │  PSTN
           ▼
┌─────────────────────┐
│       Exotel        │
└──────────┬──────────┘
           │  SIP (to IP or FQDN)
           ▼
┌─────────────────────┐
│ Your PBX / Bot / SBC│
└─────────────────────┘
```

| Connectivity | Supported |
|--------------|-----------|
| Static public IP | ✅ Yes |
| FQDN / DNS | ✅ Yes (recommended for cloud/HA) |

**Setup Flow:**
1. Create Trunk
2. Map Phone Number (Customer-Facing)
3. Add Destination URI (IP or FQDN)

**Use Cases:** Support lines, IVR routing, SIP-to-bot, Contact center queues

---

## Quick Decision

```
"Am I making calls TO the PSTN, or receiving calls FROM it?"

        Making calls TO PSTN          Receiving calls FROM PSTN
                 │                              │
                 ▼                              ▼
        OUTBOUND / TERMINATION         INBOUND / ORIGINATION
        Static IP required             IP or FQDN supported
```

---

# Quick Start Guide

## Prerequisites

| Requirement | Where to Get |
|-------------|--------------|
| Exotel Account | [Sign up](https://exotel.com/signup) |
| API Key & Token | [API Settings](https://my.exotel.com/apisettings/site#api-credentials) |
| Account SID | [API Settings](https://my.exotel.com/apisettings/site#api-credentials) |
| ExoPhone (Virtual Number) | [Number Manager](https://my.exotel.com/numbers) |

---

## Outbound / Termination Setup (5 minutes)

> ⚠️ **Requires static public IP** — FQDN/DNS is not supported.

### Step 1: Create Trunk

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "outbound_trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "<your_sid>.pstn.exotel.com"
  }'
```

✅ **Save the `trunk_sid` from response**

### Step 2: Map Phone Number (Caller ID)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+919XXXXXXXXX"}'
```

### Step 3: Whitelist Your Static IP

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "<your_pbx_public_ip>", "mask": 32}'
```

### Step 4: Configure Your PBX

| Setting | Value |
|---------|-------|
| SIP Server | `<your_sid>.pstn.exotel.com` |
| Port | `5060` (TCP) or `5061` (TLS) |
| Username | `<trunk_sid>` |
| Password | Get from [Get Credentials API](#get-credentials) |

### Step 5: Make a Test Call

From your PBX, dial any valid phone number. The call should connect!

---

## Inbound / Origination Setup (5 minutes)

> ✅ **Supports IP or FQDN** — Use FQDN for cloud/HA deployments.

### Step 1: Create Trunk

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "inbound_trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "<your_sid>.pstn.exotel.com"
  }'
```

### Step 2: Map Phone Number (Customer-Facing)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+911800XXXXXXX"}'
```

### Step 3: Add Destination URI

**Using IP:**
```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{"destinations": [{"destination": "<your_server_ip>:5061;transport=tls"}]}'
```

**Using FQDN (recommended for cloud/HA):**
```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{"destinations": [{"destination": "sip.yourcompany.com:5061;transport=tls"}]}'
```

### Step 4: Test Inbound Call

Call your mapped phone number from any phone. The call should route to your server!

---

# Validation Checklist

## For Outbound / Termination

| # | Check | Verify With |
|---|-------|-------------|
| 1 | Trunk created | `trunk_sid` in response |
| 2 | Phone number mapped | [Get Phone Numbers](#get-phone-numbers) |
| 3 | **Static IP whitelisted** | [Get Whitelisted IPs](#get-whitelisted-ips) |
| 4 | SIP credentials obtained | [Get Credentials](#get-credentials) |
| 5 | PBX configured | SIP registration OK |

## For Inbound / Origination

| # | Check | Verify With |
|---|-------|-------------|
| 1 | Trunk created | `trunk_sid` in response |
| 2 | Phone number mapped | [Get Phone Numbers](#get-phone-numbers) |
| 3 | **Destination URI added** | [Get Destination URIs](#get-destination-uris) |
| 4 | Server listening | Port 5060/5061 open |
| 5 | TLS certificate valid | If using TLS |

---

# SIP Response Codes

## Success

| Code | Meaning |
|------|---------|
| 100 | Trying |
| 180 | Ringing |
| 200 | OK (Connected) |

## Common Errors

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Unauthorized | Check credentials via Get Credentials API |
| 403 | Forbidden | Whitelist your IP (Outbound/Termination only) |
| 404 | Not Found | Check phone number format (E.164) |
| 486 | Busy | User on another call |
| 503 | Unavailable | Retry with backoff |

---

# Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| 401 on registration | Wrong credentials | Re-fetch from Get Credentials API |
| 403 on outbound | IP not whitelisted | Add via Whitelist IP API |
| 404 on outbound | Invalid number | Use E.164 format (+919XXXXXXXXX) |
| No inbound calls | Missing destination | Add via Destination URI API |
| One-way audio | Firewall blocking RTP | Open UDP 10000-20000 |
| TLS failed | Certificate issue | Check validity and chain |

---

# API Reference

## Authentication

- Replace `<your_api_key>` and `<your_api_token>` with your credentials
- Replace `<your_sid>` with your Account SID
- Replace `<subdomain>`:
  - India: `@api.in.exotel.com`
  - Singapore: `@api.exotel.com`

Get credentials from [API Settings](https://my.exotel.com/apisettings/site#api-credentials)

---

## Create Trunk

```
POST https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| trunk_name | Yes | Unique name (max 16 chars) |
| nso_code | Yes | Use `ANY-ANY` |
| domain_name | Yes | `<your_sid>.pstn.exotel.com` |

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks" \
  -H "Content-Type: application/json" \
  -d '{"trunk_name": "my_trunk", "nso_code": "ANY-ANY", "domain_name": "<your_sid>.pstn.exotel.com"}'
```

**Response:**
```json
{
  "response": {
    "status": "success",
    "data": {
      "trunk_sid": "<trunk_sid>",
      "trunk_name": "my_trunk"
    }
  }
}
```

---

## Map Phone Number

```
POST https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| phone_number | Yes | E.164 format (+919XXXXXXXXX) |

---

## Whitelist IP Address

**For Outbound / Termination only.**

```
POST https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| ip | Yes | Your static public IP |
| mask | Yes | Subnet mask (32 = single IP) |

---

## Add Destination URI

**For Inbound / Origination only.**

```
POST https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| destinations | Yes | Array of destination objects |
| destinations[].destination | Yes | `<ip_or_fqdn>:<port>;transport=tls` |

---

## Get Destination URIs

```bash
curl -X GET "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris"
```

---

## Get Whitelisted IPs

```bash
curl -X GET "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips"
```

---

## Get Credentials

```bash
curl -X GET "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/credentials"
```

**Response:**
```json
{"response": {"data": {"username": "<trunk_sid>", "password": "<sip_password>"}}}
```

---

## Get Phone Numbers

```bash
curl -X GET "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers"
```

---

## Set Trunk Alias

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/settings" \
  -H "Content-Type: application/json" \
  -d '{"settings": [{"name": "trunk_external_alias", "value": "+919XXXXXXXXX"}]}'
```

---

## Delete Trunk

⚠️ **Permanently deletes** trunk and all configurations.

```bash
curl -X DELETE "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks?trunk_sid=<trunk_sid>"
```

---

# HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Success |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Invalid credentials |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Already exists |
| 500 | Server Error | Contact support |

---

# Postman Collection

Import `postman/Exotel_Voice_Trunking_APIs.json` into Postman.

1. **Authorization** tab → Basic Auth → Enter API Key & Token
2. Replace `<subdomain>`, `<your_sid>`, `<trunk_sid>` in URL
3. Fill **Body** parameters
4. Click **Send**

---

# Support

- Documentation: https://developer.exotel.com
- Email: support@exotel.com
