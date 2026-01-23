# Exotel SIP Trunking APIs - API Reference

Complete API documentation with request/response examples.

---

## Sample Data Used in Examples

| Parameter | Example Value | Description |
|-----------|---------------|-------------|
| Account SID | `exoteltest` | Your Exotel account identifier |
| API Key | `exoteltest` | Your API key (usually same as SID) |
| API Token | `a1b2c3d4e5f6g7h8i9j0` | Your API token |
| Trunk SID | `trmum1a2b3c4d5e6f7890123456` | Trunk identifier (returned on creation) |
| Server IP | `203.0.113.50` | Your PBX/SBC public IP |
| Server Port | `5061` | SIP TLS port |
| Phone Number | `+919876543210` | E.164 format phone number |

---

## Authentication

All API requests require HTTP Basic Authentication.

```
Authorization: Basic base64(api_key:api_token)
```

**Base URL:**
- India: `https://api.in.exotel.com`
- Singapore: `https://api.exotel.com`

**Rate Limit:** 200 calls per minute

---

# API Endpoints

## 1. Create Trunk

Creates a new SIP trunk for voice connectivity.

**Endpoint:**
```
POST /v2/accounts/{account_sid}/trunks
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trunk_name | String | Yes | Unique name (max 16 chars, alphanumeric + underscore) |
| nso_code | String | Yes | Network service operator code. Use `ANY-ANY` |
| domain_name | String | Yes | SIP domain. Format: `{account_sid}.pstn.exotel.com` |

### Example Request

```bash
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "outbound_trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "exoteltest.pstn.exotel.com"
  }'
```

### Success Response (200 OK)

```json
{
  "request_id": "10a67da360d446378d5c2b66407b7f18",
  "method": "POST",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "trunk_name": "outbound_trunk",
      "date_created": "2026-01-23T09:24:59Z",
      "date_updated": "2026-01-23T09:24:59Z",
      "trunk_sid": "trmum1f708622631150902801a1n",
      "status": "active",
      "domain_name": "exoteltest.pstn.exotel.com",
      "auth_type": "IP-WHITELIST",
      "registration_enabled": "disabled",
      "edge_preference": "auto",
      "nso_code": "ANY-ANY",
      "secure_trunking": "disabled",
      "destination_uris": "/v2/accounts/exoteltest/trunks/trmum1f708622631150902801a1n/destination-uris",
      "whitelisted_ips": "/v2/accounts/exoteltest/trunks/trmum1f708622631150902801a1n/whitelisted-ips",
      "credentials": "/v2/accounts/exoteltest/trunks/trmum1f708622631150902801a1n/credentials",
      "phone_numbers": "/v2/accounts/exoteltest/trunks/trmum1f708622631150902801a1n/phone-numbers"
    }
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| trunk_sid | String | Unique trunk identifier |
| trunk_name | String | Name of the trunk |
| domain_name | String | SIP domain for the trunk |
| status | String | Trunk status (`active`, `inactive`) |
| auth_type | String | Authentication type (`IP-WHITELIST`) |
| registration_enabled | String | Registration status (`enabled`, `disabled`) |
| edge_preference | String | Edge server preference (`auto`) |
| nso_code | String | Network service operator code |
| secure_trunking | String | Secure trunking status (`enabled`, `disabled`) |
| destination_uris | String | API path to destination URIs |
| whitelisted_ips | String | API path to whitelisted IPs |
| credentials | String | API path to credentials |
| phone_numbers | String | API path to phone numbers |
| date_created | String | ISO 8601 timestamp |
| date_updated | String | ISO 8601 timestamp |

### Error Response (400 Bad Request)

```json
{
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "method": "POST",
  "http_code": 400,
  "response": {
    "status": "failure",
    "code": 400,
    "error_data": {
      "code": 1000,
      "message": "Invalid request",
      "description": "trunk_name must be alphanumeric with underscores only, max 16 characters"
    }
  }
}
```

### Error Response (409 Conflict)

```json
{
  "request_id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
  "method": "POST",
  "http_code": 409,
  "response": {
    "status": "failure",
    "code": 409,
    "error_data": {
      "code": 1002,
      "message": "Resource exists",
      "description": "Trunk with name 'outbound_trunk' already exists"
    }
  }
}
```

---

## 2. Map Phone Number

Associates a phone number with a trunk. Use `mode` to control routing.

**Endpoint:**
```
POST /v2/accounts/{account_sid}/trunks/{trunk_sid}/phone-numbers
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| phone_number | String | Yes | Phone number in E.164 format (with + prefix) |
| mode | String | No | `pstn` (default) for PSTN routing, `flow` for StreamKit/Voice AI |

### Example Request (PSTN Mode - Outbound/Termination)

```bash
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "pstn"
  }'
```

### Example Request (Flow Mode - StreamKit)

```bash
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

### Success Response (200 OK)

```json
{
  "request_id": "13ab9319cf574486ba299c364f82cade",
  "method": "POST",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "id": "41512",
      "phone_number": "+919876543210",
      "trunk_sid": "trmum1a2b3c4d5e6f7890123456",
      "date_created": "2026-01-23T10:26:54Z",
      "date_updated": "2026-01-23T10:26:54Z",
      "mode": null
    }
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique phone number mapping identifier |
| phone_number | String | Phone number in E.164 format |
| trunk_sid | String | Associated trunk identifier |
| mode | String | Routing mode (`pstn`, `flow`, or `null` if not specified) |
| date_created | String | ISO 8601 timestamp |
| date_updated | String | ISO 8601 timestamp |

### Error Response (404 Not Found)

```json
{
  "request_id": "d4e5f6a7-b8c9-0123-def4-567890123456",
  "method": "POST",
  "http_code": 404,
  "response": {
    "status": "failure",
    "code": 404,
    "error_data": {
      "code": 1003,
      "message": "Resource not found",
      "description": "Trunk 'trmum1a2b3c4d5e6f7890123456' does not exist"
    }
  }
}
```

### Error Response (400 Bad Request - Invalid Phone)

```json
{
  "request_id": "e5f6a7b8-c9d0-1234-ef56-789012345678",
  "method": "POST",
  "http_code": 400,
  "response": {
    "status": "failure",
    "code": 400,
    "error_data": {
      "code": 1001,
      "message": "Invalid parameter",
      "description": "phone_number must be in E.164 format (e.g., +919876543210)"
    }
  }
}
```

### Error Response (409 - Duplicate Phone Number)

```json
{
  "request_id": "524f5159c04b44508f846cba89aeb87e",
  "method": "POST",
  "http_code": 200,
  "response": {
    "code": 409,
    "error_data": {
      "code": 1008,
      "message": "Duplicate resource",
      "description": "Unable to create DidTrunkMapping with TrunkSid trmum15f77c83605998cdb9d1a1n"
    },
    "status": "failure",
    "data": null
  }
}
```

> **Note:** This error occurs when the phone number is already mapped to this trunk.

---

## 3. Update Phone Number Mode

Switch an existing phone number between PSTN and Flow mode.

**Endpoint:**
```
PUT /v2/accounts/{account_sid}/trunks/{trunk_sid}/phone-numbers/{phone_number_id}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| phone_number | String | Yes | Phone number in E.164 format |
| mode | String | Yes | `pstn` for PSTN routing, `flow` for StreamKit |

### Example Request (Switch to Flow Mode)

```bash
curl -X PUT "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/phone-numbers/pn_9876543210_001" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

### Example Request (Switch to PSTN Mode)

```bash
curl -X PUT "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/phone-numbers/pn_9876543210_001" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "pstn"
  }'
```

### Success Response (200 OK)

```json
{
  "request_id": "f6a7b8c9-d0e1-2345-f678-901234567890",
  "method": "PUT",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "id": "41512",
      "phone_number": "+919876543210",
      "trunk_sid": "trmum1a2b3c4d5e6f7890123456",
      "date_created": "2026-01-23T10:26:54Z",
      "date_updated": "2026-01-23T10:30:00Z",
      "mode": "flow"
    }
  }
}
```

---

## 4. Whitelist IP Address

Register your server's IP for authentication. Required for Outbound/Termination and StreamKit.

**Endpoint:**
```
POST /v2/accounts/{account_sid}/trunks/{trunk_sid}/whitelisted-ips
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ip | String | Yes | Public IPv4 address of your server |
| mask | Integer | Yes | Subnet mask (32 = single IP, 24 = /24 subnet) |

### Example Request

```bash
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "203.0.113.50",
    "mask": 32
  }'
```

### Success Response (200 OK)

```json
{
  "request_id": "3daaed4cd05d443f854e07e60dd4c008",
  "method": "POST",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "id": "1153",
      "mask": 32,
      "trunk_sid": "trmum1a2b3c4d5e6f7890123456",
      "ip": "203.0.113.50",
      "friendly_name": null,
      "date_created": "2026-01-23T11:37:36Z",
      "date_updated": "2026-01-23T11:37:36Z"
    }
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique whitelisted IP identifier |
| ip | String | Whitelisted IPv4 address |
| mask | Integer | Subnet mask (32 = single IP) |
| trunk_sid | String | Associated trunk identifier |
| friendly_name | String | Optional friendly name (`null` if not set) |
| date_created | String | ISO 8601 timestamp |
| date_updated | String | ISO 8601 timestamp |

### Error Response (400 Bad Request - Invalid IP)

```json
{
  "request_id": "b8c9d0e1-f2a3-4567-8901-bcdef2345678",
  "method": "POST",
  "http_code": 400,
  "response": {
    "status": "failure",
    "code": 400,
    "error_data": {
      "code": 1001,
      "message": "Invalid parameter",
      "description": "ip must be a valid IPv4 address"
    }
  }
}
```

### Error Response (409 - Duplicate IP)

```json
{
  "request_id": "901c1fb5f9c244fea99fdf498665f229",
  "method": "POST",
  "http_code": 200,
  "response": {
    "code": 409,
    "error_data": {
      "code": 1008,
      "message": "Duplicate resource",
      "description": "Unable to Whitelist-ip with ip 44.248.146.10"
    },
    "status": "failure",
    "data": null
  }
}
```

> **Note:** The `http_code` may be 200 but check `response.code` for the actual status.

---

## 5. Add Destination URI

Configure where incoming calls are routed. Required for Inbound/Origination.

**Endpoint:**
```
POST /v2/accounts/{account_sid}/trunks/{trunk_sid}/destination-uris
```

> ⚠️ **IMPORTANT:** You must use your **actual server's public IP address** or a valid FQDN. The API validates that the destination is reachable. Example IPs like `203.0.113.50` (documentation IPs) will fail validation.

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| destinations | Array | Yes | Array of destination objects |
| destinations[].destination | String | Yes | Format: `ip:port;transport=tls` or `ip:port;transport=tcp`. Must be a **real, routable IP** or valid FQDN |

### Example Request (TLS - Recommended)

```bash
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {"destination": "203.0.113.50:5061;transport=tls"}
    ]
  }'
```

### Example Request (TCP)

```bash
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {"destination": "203.0.113.50:5060;transport=tcp"}
    ]
  }'
```

### Example Request (FQDN)

```bash
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {"destination": "sip.mycompany.com:5061;transport=tls"}
    ]
  }'
```

### Success Response (200 OK)

```json
{
  "request_id": "63999f0a98a24a0aa58ab5b74aec9f0a",
  "method": "POST",
  "http_code": 200,
  "metadata": {
    "total": 1,
    "success": 1
  },
  "response": [
    {
      "code": 200,
      "error_data": null,
      "status": "success",
      "data": {
        "id": "2543",
        "destination": "sip:44.248.146.11:5061;transport=tls",
        "date_created": "2026-01-23T13:38:32Z",
        "date_updated": "2026-01-23T13:38:32Z",
        "type": "public",
        "priority": 0,
        "weight": 1,
        "trunk_sid": "trmum1a2b3c4d5e6f7890123456"
      }
    }
  ]
}
```

### Error Response (400/207 - Invalid Destination)

This error occurs when the destination IP is not valid or reachable:

```json
{
  "request_id": "f4909884342e4532a4ccf30d617519af",
  "method": "POST",
  "http_code": 207,
  "metadata": {
    "failed": 1,
    "total": 1,
    "success": 0
  },
  "response": [
    {
      "code": 400,
      "error_data": {
        "code": 1002,
        "message": "Invalid parameter",
        "description": "Destination is not a valid Ip or Fqdn"
      },
      "status": "failure",
      "data": null
    }
  ]
}
```

**Common causes:**
- Using documentation/example IPs like `203.0.113.50` (RFC 5737 reserved)
- Using private IPs that aren't publicly routable
- FQDN doesn't resolve to a valid IP
- IP address format is incorrect

**Solution:** Use your actual server's public IP address or a valid FQDN.

### Error Response (207 - Destination Not Whitelisted)

This error occurs when you try to add a destination URI for an IP that hasn't been whitelisted first:

```json
{
  "request_id": "c06dc46304aa406ea7daca83785bc7a9",
  "method": "POST",
  "http_code": 207,
  "metadata": {
    "failed": 1,
    "total": 1,
    "success": 0
  },
  "response": [
    {
      "code": 400,
      "error_data": {
        "code": 1002,
        "message": "Invalid parameter",
        "description": "Destination not whitelisted"
      },
      "status": "failure",
      "data": null
    }
  ]
}
```

**Solution:** For IP-based destinations, you must whitelist the IP address first using the Whitelist IP API before adding it as a destination URI. FQDNs do not require whitelisting.

---

## 6. Get Credentials

Retrieve SIP authentication credentials for PBX configuration.

**Endpoint:**
```
GET /v2/accounts/{account_sid}/trunks/{trunk_sid}/credentials
```

### Example Request

```bash
curl -X GET "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/credentials"
```

### Success Response (200 OK)

```json
{
  "request_id": "d0e1f2a3-b4c5-6789-0123-def456789012",
  "method": "GET",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "username": "trmum1a2b3c4d5e6f7890123456",
      "password": "Xk9mP2nQ4rS6tU8v"
    }
  }
}
```

### Empty Response (No Credentials)

If no credentials have been configured, the response will be an empty array:

```json
{
  "request_id": "4b15de3688c64a6184ca3777d5cfa046",
  "method": "GET",
  "http_code": 200,
  "response": []
}
```

**Use these credentials in your PBX:**

| PBX Setting | Value |
|-------------|-------|
| SIP Server | `exoteltest.pstn.exotel.com` |
| Port | `5060` (TCP) or `5061` (TLS) |
| Username | `trmum1a2b3c4d5e6f7890123456` |
| Password | `Xk9mP2nQ4rS6tU8v` |

---

## 7. Get Phone Numbers

List all phone numbers mapped to a trunk.

**Endpoint:**
```
GET /v2/accounts/{account_sid}/trunks/{trunk_sid}/phone-numbers
```

### Example Request

```bash
curl -X GET "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/phone-numbers"
```

### Success Response (200 OK)

```json
{
  "request_id": "785471d288054cbf8c677b75e0b5f2f8",
  "method": "GET",
  "http_code": 200,
  "metadata": {
    "page_size": 50,
    "first_page_uri": "/v2/accounts/ameyo5m/trunks/trmum1a2b3c4d5e6f7890123456/phone-numbers?offset=0&page_size=50",
    "prev_page_uri": null,
    "next_page_uri": null
  },
  "response": [
    {
      "code": 200,
      "error_data": null,
      "status": "success",
      "data": {
        "id": "41523",
        "phone_number": "+918040264208",
        "trunk_sid": "trmum1a2b3c4d5e6f7890123456",
        "date_created": "2026-01-23T13:28:11Z",
        "date_updated": "2026-01-23T13:41:59Z",
        "mode": "flow"
      }
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| metadata.page_size | Integer | Number of items per page (default 50) |
| metadata.first_page_uri | String | URI to first page of results |
| metadata.prev_page_uri | String | URI to previous page (null if on first page) |
| metadata.next_page_uri | String | URI to next page (null if on last page) |

---

## 8. Get Whitelisted IPs

List all whitelisted IPs for a trunk.

**Endpoint:**
```
GET /v2/accounts/{account_sid}/trunks/{trunk_sid}/whitelisted-ips
```

### Example Request

```bash
curl -X GET "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/whitelisted-ips"
```

### Success Response (200 OK)

```json
{
  "request_id": "91dc982ca79846479c6f9678c788cfc1",
  "method": "GET",
  "http_code": 200,
  "metadata": {
    "page_size": 50,
    "first_page_uri": "/v2/accounts/ameyo5m/trunks/trmum1a2b3c4d5e6f7890123456/whitelisted-ips?offset=0&page_size=50",
    "prev_page_uri": null,
    "next_page_uri": null
  },
  "response": [
    {
      "code": 200,
      "error_data": null,
      "status": "success",
      "data": {
        "id": "1154",
        "mask": 32,
        "trunk_sid": "trmum1a2b3c4d5e6f7890123456",
        "ip": "44.248.146.11",
        "friendly_name": null,
        "date_created": "2026-01-23T13:30:04Z",
        "date_updated": "2026-01-23T13:30:04Z"
      }
    }
  ]
}
```

---

## 9. Get Destination URIs

List all destination URIs for inbound routing.

**Endpoint:**
```
GET /v2/accounts/{account_sid}/trunks/{trunk_sid}/destination-uris
```

### Example Request

```bash
curl -X GET "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/destination-uris"
```

### Success Response (200 OK)

```json
{
  "request_id": "bfc1544ab0ab4df3ae49173ccc744331",
  "method": "GET",
  "http_code": 200,
  "metadata": {
    "page_size": 50,
    "first_page_uri": "/v2/accounts/ameyo5m/trunks/trmum1a2b3c4d5e6f7890123456/destination-uris?offset=0&page_size=50",
    "prev_page_uri": null,
    "next_page_uri": null
  },
  "response": [
    {
      "code": 200,
      "error_data": null,
      "status": "success",
      "data": {
        "id": "2544",
        "destination": "sip:sip.mycompany.com:5061;transport=tls",
        "date_created": "2026-01-23T13:39:06Z",
        "date_updated": "2026-01-23T13:39:06Z",
        "type": "public",
        "priority": 0,
        "weight": 1,
        "trunk_sid": "trmum1a2b3c4d5e6f7890123456"
      }
    },
    {
      "code": 200,
      "error_data": null,
      "status": "success",
      "data": {
        "id": "2543",
        "destination": "sip:44.248.146.11:5061;transport=tls",
        "date_created": "2026-01-23T13:38:32Z",
        "date_updated": "2026-01-23T13:38:32Z",
        "type": "public",
        "priority": 0,
        "weight": 1,
        "trunk_sid": "trmum1a2b3c4d5e6f7890123456"
      }
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | String | Unique destination URI identifier |
| destination | String | SIP URI with transport |
| type | String | Destination type (`public`) |
| priority | Integer | Priority for routing (lower = higher priority) |
| weight | Integer | Weight for load balancing |
| trunk_sid | String | Associated trunk identifier |

---

## 10. Set Trunk Alias

Set an external caller ID for outbound calls.

**Endpoint:**
```
POST /v2/accounts/{account_sid}/trunks/{trunk_sid}/settings
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| settings | Array | Yes | Array of setting objects |
| settings[].name | String | Yes | Setting name. Use `trunk_external_alias` |
| settings[].value | String | Yes | Phone number in E.164 format |

### Example Request

```bash
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "settings": [
      {"name": "trunk_external_alias", "value": "+919876543210"}
    ]
  }'
```

### Success Response (200 OK)

```json
{
  "request_id": "8ce98845365f43fd97c2f46df38438c6",
  "method": "POST",
  "http_code": 200,
  "metadata": {
    "total": 1,
    "success": 1
  },
  "response": [
    {
      "code": 200,
      "error_data": null,
      "status": "success",
      "data": {
        "name": "trunk_external_alias",
        "value": "+919876543210",
        "trunk_sid": "trmum1a2b3c4d5e6f7890123456",
        "date_created": "2026-01-23T13:34:50Z",
        "date_updated": "2026-01-23T13:34:50Z"
      }
    }
  ]
}
```

---

## 11. Delete Trunk

Permanently delete a trunk and all configurations. This cannot be undone.

**Endpoint:**
```
DELETE /v2/accounts/{account_sid}/trunks?trunk_sid={trunk_sid}
```

### Example Request

```bash
curl -X DELETE "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks?trunk_sid=trmum1a2b3c4d5e6f7890123456"
```

### Success Response (200 OK)

```json
{
  "request_id": "f708818c79f547b3aee31c4a480367a5",
  "method": "DELETE",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "trunk_name": "my_trunk1234",
      "date_created": "2026-01-23T13:25:39Z",
      "date_updated": "2026-01-23T13:25:39Z",
      "trunk_sid": "trmum15f77c83605998cdb9d1a1n",
      "status": "active",
      "domain_name": "ameyo5m.pstn.exotel.com",
      "auth_type": "IP-WHITELIST",
      "registration_enabled": "disabled",
      "edge_preference": "auto",
      "nso_code": "ANY-ANY",
      "secure_trunking": "disabled"
    }
  }
}
```

> **Note:** The delete response returns the full trunk data of the deleted trunk.

---

# HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 207 | Multi-Status | Partial success (check individual responses) |
| 400 | Bad Request | Invalid parameters or malformed request |
| 401 | Unauthorized | Invalid or missing credentials |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Resource already exists (duplicate) |
| 415 | Unsupported Media Type | Wrong Content-Type (use application/json) |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded (200/min) |
| 500 | Internal Server Error | Server error |

---

# Error Codes

| Code | HTTP | Message | Description | Resolution |
|------|------|---------|-------------|------------|
| 1000 | 404 | Not Found | Resource not found or invalid body | Check URL and request body |
| 1001 | 400 | Invalid parameter / Mandatory Parameter missing | Parameter missing or invalid | Verify all required parameters |
| 1002 | 400 | Invalid parameter | Destination not valid or not whitelisted | Use valid IP/FQDN, whitelist IP first |
| 1007 | 400 | Invalid request body | JSON parsing failed | Check JSON syntax |
| 1008 | 409 | Duplicate resource | IP or phone number already exists | Use different IP/number or delete existing |
| 1011 | 415 | Unsupported content type | Wrong Content-Type header | Use `Content-Type: application/json` |
| 1010 | 401 | Authorization failed | Invalid API key or token | Check credentials |
| 1020 | 422 | Validation error | Request validation failed | Check all parameters |
| 1030 | 429 | Rate limit exceeded | Too many requests | Wait and retry |

---

# End-to-End Example: Outbound Setup

Complete setup for making outbound calls:

```bash
# Step 1: Create Trunk
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks" \
  -H "Content-Type: application/json" \
  -d '{"trunk_name": "outbound_trunk", "nso_code": "ANY-ANY", "domain_name": "exoteltest.pstn.exotel.com"}'
# Response: trunk_sid = "trmum1a2b3c4d5e6f7890123456"

# Step 2: Map Phone Number
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+919876543210", "mode": "pstn"}'

# Step 3: Whitelist IP
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "203.0.113.50", "mask": 32}'

# Step 4: Get Credentials
curl -X GET "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum1a2b3c4d5e6f7890123456/credentials"
# Response: username="trmum1a2b3c4d5e6f7890123456", password="Xk9mP2nQ4rS6tU8v"
```

---

# End-to-End Example: Inbound Setup

Complete setup for receiving inbound calls:

```bash
# Step 1: Create Trunk
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks" \
  -H "Content-Type: application/json" \
  -d '{"trunk_name": "inbound_trunk", "nso_code": "ANY-ANY", "domain_name": "exoteltest.pstn.exotel.com"}'
# Response: trunk_sid = "trmum2b3c4d5e6f7890123457"

# Step 2: Map Phone Number
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum2b3c4d5e6f7890123457/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+911800123456"}'

# Step 3: Add Destination URI
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum2b3c4d5e6f7890123457/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{"destinations": [{"destination": "203.0.113.50:5061;transport=tls"}]}'
```

---

# End-to-End Example: StreamKit Setup

Complete setup for Voice AI bot integration:

```bash
# Step 1: Create Trunk
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks" \
  -H "Content-Type: application/json" \
  -d '{"trunk_name": "streamkit_trunk", "nso_code": "ANY-ANY", "domain_name": "exoteltest.pstn.exotel.com"}'
# Response: trunk_sid = "trmum3c4d5e6f7890123458"

# Step 2: Map Phone Number with Flow Mode
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum3c4d5e6f7890123458/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+919876543210", "mode": "flow"}'

# Step 3: Whitelist IP
curl -X POST "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum3c4d5e6f7890123458/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "203.0.113.50", "mask": 32}'

# Step 4: Get Credentials
curl -X GET "https://exoteltest:a1b2c3d4e5f6g7h8i9j0@api.in.exotel.com/v2/accounts/exoteltest/trunks/trmum3c4d5e6f7890123458/credentials"
```

---

# Validation Rules

| Field | Rule | Example Valid | Example Invalid |
|-------|------|---------------|-----------------|
| trunk_name | Alphanumeric + underscore, max 16 chars | `my_trunk_01` | `my-trunk!` |
| phone_number | E.164 format with + prefix | `+919876543210` | `9876543210` |
| ip | Valid IPv4 address | `203.0.113.50` | `256.1.2.3` |
| mask | Integer 1-32 | `32` | `33` |
| mode | `pstn` or `flow` | `pstn` | `PSTN` |
| transport | `tcp` or `tls` | `tls` | `udp` |
