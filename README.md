# Exotel SIP Trunking APIs

Connect your communication system to the telephone network.

---

## Three Use Cases

| Use Case | Direction | Mode | Description |
|----------|-----------|------|-------------|
| **Outbound / Termination** | Your System → PSTN | `pstn` | Make calls to phone numbers |
| **Inbound / Origination** | PSTN → Your System | - | Receive calls from phone numbers |
| **StreamKit** | Your System → Voice AI Bot | `flow` | Connect contact center to WebSocket-based bots |

---

## Quick Start: Outbound / Termination

Make calls from your PBX to the telephone network.

**Requirement:** Static public IP (FQDN not supported)

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

Save the `trunk_sid` from response.

### Step 2: Map Phone Number

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "pstn"
  }'
```

### Step 3: Whitelist IP

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "<your_server_ip>",
    "mask": 32
  }'
```

### Step 4: Get Credentials

```bash
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/credentials"
```

### Step 5: Configure PBX

| Setting | Value |
|---------|-------|
| SIP Server | `<your_sid>.pstn.exotel.com` |
| Port | 5060 (TCP) or 5061 (TLS) |
| Username | `<trunk_sid>` |
| Password | From Step 4 |

---

## Quick Start: Inbound / Origination

Receive calls from the telephone network to your system.

**Requirement:** Static IP or FQDN

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

### Step 2: Map Phone Number

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+911800123456"
  }'
```

### Step 3: Add Destination URI

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {"destination": "<your_server_ip>:5061;transport=tls"}
    ]
  }'
```

---

## Quick Start: StreamKit

Connect your contact center to WebSocket-based Voice AI bots.

StreamKit is a cloud-native SIP-to-WebSocket connector that enables real-time audio streaming between enterprise contact centers and Voice AI platforms.

**Use Cases:**
- AI-powered IVR
- Voice bot integration
- Real-time speech analytics
- Agent assist with AI

### Step 1: Create Trunk

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "streamkit_trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "<your_sid>.pstn.exotel.com"
  }'
```

### Step 2: Map Phone Number with Flow Mode

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

The `mode: "flow"` routes calls to your Voice AI bot instead of PSTN.

### Step 3: Whitelist IP

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "<your_server_ip>",
    "mask": 32
  }'
```

### Step 4: Get Credentials

```bash
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/credentials"
```

---

## Update Phone Number Mode

Switch between PSTN and Flow mode for an existing phone number mapping.

### Change to Flow Mode (StreamKit)

```bash
curl -X PUT "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers/<phone_number_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

### Change to PSTN Mode (Standard Termination)

```bash
curl -X PUT "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers/<phone_number_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "pstn"
  }'
```

---

## API Summary

| API | Method | Endpoint |
|-----|--------|----------|
| Create Trunk | POST | `/v2/accounts/<your_sid>/trunks` |
| Map Phone Number | POST | `/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers` |
| Update Phone Number | PUT | `/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers/<id>` |
| Whitelist IP | POST | `/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips` |
| Add Destination URI | POST | `/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris` |
| Get Credentials | GET | `/v2/accounts/<your_sid>/trunks/<trunk_sid>/credentials` |
| Get Phone Numbers | GET | `/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers` |
| Get Whitelisted IPs | GET | `/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips` |
| Get Destination URIs | GET | `/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris` |
| Set Trunk Alias | POST | `/v2/accounts/<your_sid>/trunks/<trunk_sid>/settings` |
| Delete Trunk | DELETE | `/v2/accounts/<your_sid>/trunks?trunk_sid=<trunk_sid>` |

---

## Authentication

| Parameter | Value |
|-----------|-------|
| Method | HTTP Basic Auth |
| Username | Your API Key |
| Password | Your API Token |

**Base URL:**
- India: `https://api.in.exotel.com`
- Singapore: `https://api.exotel.com`

**Rate Limit:** 200 calls per minute

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Wrong credentials | Check API Key and Token |
| 403 Forbidden | IP not whitelisted | Add IP via Whitelist API |
| 404 Not Found | Invalid trunk_sid or number | Verify IDs |
| No inbound calls | Missing destination URI | Add destination URI |

---

## Documentation

- [Detailed API Reference](docs/API_REFERENCE.md)
- [SIP Trunking Guide](docs/SIP_TRUNKING_GUIDE.md)
- [Postman Collection](postman/Exotel_SIP_Trunking_APIs.json)

---

## Support

- Documentation: https://developer.exotel.com
- StreamKit: https://exotel.com/products/streamkit-cloud-connector/
- Email: support@exotel.com

---

**Note:** FQDN/DNS routing is supported only for Inbound/Origination. Outbound/Termination and StreamKit require static IP whitelisting.
