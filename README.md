# Exotel vSIP Trunk Configuration API

Configure SIP Trunks for PSTN connectivity with Exotel.

---

## What is a SIP Trunk?

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Your System   │◄───────►│     Exotel      │◄───────►│      PSTN       │
│  (PBX/Contact   │   SIP   │   SIP Trunk     │         │  (Phone Network)│
│    Center)      │  Trunk  │    Gateway      │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

A SIP Trunk connects your communication system to the Public Switched Telephone Network (PSTN) over the internet.

---

## Two Use Cases

| Use Case | Direction | Setup Flow |
|----------|-----------|------------|
| **Termination** | Your System → PSTN | Create Trunk → Map Phone Number → Whitelist IP |
| **Origination** | PSTN → Your System | Create Trunk → Map Phone Number → Add Destination URI |

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│      TERMINATION            │     │      ORIGINATION            │
│    (Outbound Calls)         │     │    (Inbound Calls)          │
├─────────────────────────────┤     ├─────────────────────────────┤
│  1. Create Trunk            │     │  1. Create Trunk            │
│  2. Map Phone Number        │     │  2. Map Phone Number        │
│     (Your Caller ID)        │     │     (Customer Dials)        │
│  3. Whitelist IP            │     │  3. Add Destination URI     │
│     (Your Server IP)        │     │     (Your Server Address)   │
└─────────────────────────────┘     └─────────────────────────────┘
```

---

# Quick Start Guide

## End-to-End Setup: Your First Successful Call

### Prerequisites

Before you begin, ensure you have:

| Requirement | Where to Get |
|-------------|--------------|
| Exotel Account | [Sign up](https://exotel.com/signup) |
| API Key & Token | [API Settings](https://my.exotel.com/apisettings/site#api-credentials) |
| Account SID | [API Settings](https://my.exotel.com/apisettings/site#api-credentials) |
| ExoPhone (Virtual Number) | [Number Manager](https://my.exotel.com/numbers) |
| Your SIP Server IP | Your infrastructure |

---

## Quickstart: Termination (Make Outbound Calls)

**Goal:** Make a call from your PBX to a mobile/landline number.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    TERMINATION SETUP (5 minutes)                         │
└──────────────────────────────────────────────────────────────────────────┘

  STEP 1                STEP 2                 STEP 3              STEP 4
┌─────────┐          ┌──────────┐          ┌───────────┐       ┌──────────┐
│ Create  │  ──────► │ Map Phone│  ──────► │ Whitelist │ ────► │ Make     │
│ Trunk   │          │ Number   │          │ IP        │       │ Test Call│
└─────────┘          └──────────┘          └───────────┘       └──────────┘
     │                    │                      │                   │
     ▼                    ▼                      ▼                   ▼
 Get trunk_sid      Set Caller ID         Your PBX IP         Validate!
```

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

✅ **Save the `trunk_sid` from response** — you'll need it for all subsequent calls.

### Step 2: Map Phone Number (Your Caller ID)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919XXXXXXXXX"
  }'
```

### Step 3: Whitelist Your Server IP

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "<your_pbx_public_ip>",
    "mask": 32
  }'
```

### Step 4: Configure Your PBX

Use these SIP settings in your PBX:

| Setting | Value |
|---------|-------|
| **SIP Server** | `<your_sid>.pstn.exotel.com` |
| **Port** | `5060` (TCP) or `5061` (TLS) |
| **Username** | `<trunk_sid>` |
| **Password** | Get from [Get Credentials API](#get-credentials) |
| **Caller ID** | Your mapped phone number |

### Step 5: Make a Test Call

From your PBX, dial any valid phone number. The call should connect!

---

## Quickstart: Origination (Receive Inbound Calls)

**Goal:** Receive calls on your published number and route to your system.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    ORIGINATION SETUP (5 minutes)                         │
└──────────────────────────────────────────────────────────────────────────┘

  STEP 1                STEP 2                 STEP 3              STEP 4
┌─────────┐          ┌──────────┐          ┌───────────┐       ┌──────────┐
│ Create  │  ──────► │ Map Phone│  ──────► │ Add Dest  │ ────► │ Test     │
│ Trunk   │          │ Number   │          │ URI       │       │ Inbound  │
└─────────┘          └──────────┘          └───────────┘       └──────────┘
     │                    │                      │                   │
     ▼                    ▼                      ▼                   ▼
 Get trunk_sid      Customer dials         Your server IP      Call yourself!
```

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

### Step 2: Map Phone Number (Customer-Facing Number)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+911800XXXXXXX"
  }'
```

### Step 3: Add Destination URI (Where Calls Go)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "<your_server_ip>:5061;transport=tls" }
    ]
  }'
```

### Step 4: Test Inbound Call

Call your mapped phone number from any phone. The call should route to your server!

---

# First Successful Call Validation

## Checklist Before Making Your First Call

### For Termination (Outbound)

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | ✅ Trunk created | `trunk_sid` received in response |
| 2 | ✅ Phone number mapped | [Get Phone Numbers API](#get-phone-numbers) returns your number |
| 3 | ✅ IP whitelisted | [Get Whitelisted IPs API](#get-whitelisted-ips) returns your IP |
| 4 | ✅ SIP credentials obtained | [Get Credentials API](#get-credentials) returns username/password |
| 5 | ✅ PBX configured | SIP registration successful |
| 6 | ✅ Firewall allows outbound | Port 5060/5061 open to Exotel |

### For Origination (Inbound)

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | ✅ Trunk created | `trunk_sid` received in response |
| 2 | ✅ Phone number mapped | [Get Phone Numbers API](#get-phone-numbers) returns your number |
| 3 | ✅ Destination URI added | [Get Destination URIs API](#get-destination-uris) returns your server |
| 4 | ✅ Server listening | Your SIP server accepting connections on 5060/5061 |
| 5 | ✅ Firewall allows inbound | Port 5060/5061 open from Exotel IPs |
| 6 | ✅ TLS certificate valid | If using TLS, certificate is trusted |

---

## Validation Script

Run these commands to verify your setup:

```bash
# 1. Verify trunk exists
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/credentials"

# 2. Verify phone number mapped
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers"

# 3. Verify IP whitelisted (for Termination)
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips"

# 4. Verify destination URI (for Origination)
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris"
```

**Expected:** All APIs return `"status": "success"` with your configured data.

---

# SIP Response Codes & Troubleshooting

## SIP Response Code Mapping

### Successful Calls

| SIP Code | Meaning | Description |
|----------|---------|-------------|
| 100 | Trying | Call is being routed |
| 180 | Ringing | Destination phone is ringing |
| 183 | Session Progress | Early media (ringback tone) |
| 200 | OK | Call connected successfully |

### Client Errors (4xx)

| SIP Code | Meaning | Cause | Solution |
|----------|---------|-------|----------|
| 400 | Bad Request | Malformed SIP message | Check SIP headers format |
| 401 | Unauthorized | Invalid credentials | Verify username/password from Get Credentials API |
| 403 | Forbidden | IP not whitelisted | Add your IP using Whitelist IP API |
| 404 | Not Found | Invalid destination number | Verify phone number format (E.164) |
| 408 | Request Timeout | Network timeout | Check network connectivity |
| 480 | Temporarily Unavailable | Destination busy/offline | Retry later |
| 486 | Busy Here | Destination is busy | User is on another call |
| 487 | Request Terminated | Call cancelled | Caller hung up before answer |
| 488 | Not Acceptable | Codec mismatch | Check supported codecs |

### Server Errors (5xx)

| SIP Code | Meaning | Cause | Solution |
|----------|---------|-------|----------|
| 500 | Server Internal Error | Exotel server issue | Contact support |
| 502 | Bad Gateway | Upstream error | Check destination server |
| 503 | Service Unavailable | Server overloaded | Retry with backoff |
| 504 | Gateway Timeout | Destination not responding | Check destination server |

### Global Errors (6xx)

| SIP Code | Meaning | Cause | Solution |
|----------|---------|-------|----------|
| 600 | Busy Everywhere | All destinations busy | All lines occupied |
| 603 | Decline | Call rejected | Destination rejected call |
| 604 | Does Not Exist | Number doesn't exist | Verify destination number |
| 606 | Not Acceptable | Call requirements not met | Check call parameters |

---

## Troubleshooting Guide

### Problem: 401 Unauthorized

```
┌─────────────────────────────────────────────────────────────────┐
│ SYMPTOM: SIP registration fails with 401                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECK 1: Are credentials correct?                               │
│                                                                 │
│ curl -X GET ".../trunks/<trunk_sid>/credentials"                │
│                                                                 │
│ → Verify username = trunk_sid                                   │
│ → Verify password matches                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECK 2: Is authentication method correct?                      │
│                                                                 │
│ → Use Digest Authentication (not Basic)                         │
│ → Realm: pstn.exotel.com                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Problem: 403 Forbidden

```
┌─────────────────────────────────────────────────────────────────┐
│ SYMPTOM: Calls rejected with 403                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECK 1: Is your IP whitelisted?                                │
│                                                                 │
│ curl -X GET ".../trunks/<trunk_sid>/whitelisted-ips"            │
│                                                                 │
│ → Verify your public IP is in the list                          │
│ → If NAT, whitelist your external/public IP                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECK 2: Is phone number mapped?                                │
│                                                                 │
│ curl -X GET ".../trunks/<trunk_sid>/phone-numbers"              │
│                                                                 │
│ → Verify your caller ID is mapped                               │
└─────────────────────────────────────────────────────────────────┘
```

### Problem: No Inbound Calls Received

```
┌─────────────────────────────────────────────────────────────────┐
│ SYMPTOM: Calls to your number don't reach your server           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECK 1: Is destination URI configured?                         │
│                                                                 │
│ curl -X GET ".../trunks/<trunk_sid>/destination-uris"           │
│                                                                 │
│ → Verify your server IP:port is listed                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECK 2: Is your server reachable?                              │
│                                                                 │
│ → Firewall allows inbound on 5060/5061                          │
│ → Server is listening on correct port                           │
│ → Test: nc -zv <your_ip> 5061                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECK 3: TLS certificate valid? (if using TLS)                  │
│                                                                 │
│ → Certificate not expired                                       │
│ → Certificate chain complete                                    │
│ → Common Name matches server                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Problem: Call Connects but No Audio

```
┌─────────────────────────────────────────────────────────────────┐
│ SYMPTOM: Call shows connected but one/both sides have no audio  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECK 1: NAT/Firewall issue                                     │
│                                                                 │
│ → RTP ports open (typically 10000-20000 UDP)                    │
│ → STUN/TURN configured if behind NAT                            │
│ → SIP ALG disabled on router                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHECK 2: Codec mismatch                                         │
│                                                                 │
│ Supported codecs:                                               │
│ → G.711 μ-law (PCMU)                                            │
│ → G.711 A-law (PCMA)                                            │
│ → G.729                                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Common Issues Quick Reference

| Issue | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| 401 on registration | Wrong credentials | Re-fetch from Get Credentials API |
| 403 on outbound call | IP not whitelisted | Add IP via Whitelist IP API |
| 404 on outbound call | Invalid number format | Use E.164 format (+919XXXXXXXXX) |
| No inbound calls | Missing destination URI | Add via Add Destination URI API |
| One-way audio | Firewall blocking RTP | Open UDP 10000-20000 |
| TLS handshake failed | Certificate issue | Check cert validity and chain |
| Registration timeout | Network/firewall | Check port 5060/5061 connectivity |

---

## Exotel SIP Server IPs (Whitelist in Your Firewall)

For **inbound calls**, allow these Exotel IPs in your firewall:

| Region | IP Addresses |
|--------|--------------|
| India (Mumbai) | Contact support for current IPs |
| Singapore | Contact support for current IPs |

---

# API Reference

---

## Authentication

Replace `<your_api_key>` and `<your_api_token>` with the API key and token created by you.

- Replace `<your_sid>` with your "Account SID"
- Replace `<subdomain>` with the region of your account
  - `<subdomain>` of Singapore cluster is `@api.exotel.com`
  - `<subdomain>` of Mumbai cluster is `@api.in.exotel.com`

`<your_api_key>`, `<your_api_token>` and `<your_sid>` are available in the **API Settings** page of your [Exotel Dashboard](https://my.exotel.com/apisettings/site#api-credentials)

---

## Create Trunk

Creates a virtual connection between your system and Exotel's PSTN gateway.

An HTTP POST request is made to:

```
POST
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks
```

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| trunk_name | Mandatory | String; Unique name (max 16 chars, alphanumeric + underscore) |
| nso_code | Mandatory | String; Network Service Operator code. Use `ANY-ANY` |
| domain_name | Mandatory | String; Format: `<your_sid>.pstn.exotel.com` |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "my_trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "<your_sid>.pstn.exotel.com"
  }'
```

### Example Response

```json
{
  "request_id": "a1b2c3d4e5f6",
  "method": "POST",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": {
      "trunk_sid": "<trunk_sid>",
      "trunk_name": "my_trunk",
      "domain_name": "<your_sid>.pstn.exotel.com",
      "nso_code": "ANY-ANY",
      "date_created": "2025-01-22T10:00:00Z"
    }
  }
}
```

---

## Map Phone Number

Associates a phone number (DID/ExoPhone) with your trunk.

```
POST
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers
```

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| phone_number | Mandatory | String; E.164 format (e.g., `+919XXXXXXXXX`) |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+919XXXXXXXXX"}'
```

---

## Whitelist IP Address

Registers your server's IP for secure authentication. **Required for Termination.**

```
POST
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips
```

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| ip | Mandatory | String; Your server's public IPv4 address |
| mask | Mandatory | Integer; Subnet mask (32 for single IP) |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "<your_server_ip>", "mask": 32}'
```

---

## Add Destination URI

Tells Exotel where to send incoming calls. **Required for Origination.**

```
POST
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris
```

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| destinations | Mandatory | Array of destination objects |
| destinations[].destination | Mandatory | String; Format: `<ip>:<port>;transport=<tls\|tcp>` |

### Example Request (TLS - Recommended)

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{"destinations": [{"destination": "<your_server_ip>:5061;transport=tls"}]}'
```

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
{
  "response": {
    "status": "success",
    "data": {
      "username": "<trunk_sid>",
      "password": "<sip_password>"
    }
  }
}
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

⚠️ **Permanently deletes** the trunk and all configurations.

```bash
curl -X DELETE "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks?trunk_sid=<trunk_sid>"
```

---

# HTTP Status Codes

| HTTP Code | Status | Description |
|-----------|--------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Invalid credentials |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

---

# Error Codes

| Error Code | HTTP | Message | Description |
|------------|------|---------|-------------|
| 1000 | 400 | Invalid request | Missing/invalid field |
| 1002 | 409 | Resource exists | Already exists |
| 1003 | 404 | Not found | Trunk doesn't exist |
| 1010 | 401 | Auth failed | Invalid API key/token |

---

# Postman Collection

Import `postman/Exotel_vSIP_API_Collection.json` into Postman.

**Setup:**
1. Go to **Authorization** tab → **Basic Auth**
2. Enter **API Key** as Username, **API Token** as Password
3. Replace `<subdomain>`, `<your_sid>`, `<trunk_sid>` in URL
4. Fill **Body** parameters
5. Click **Send**

---

# Support

- Documentation: https://developer.exotel.com
- Email: support@exotel.com
