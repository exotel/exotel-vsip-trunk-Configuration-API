# Exotel SIP Trunking APIs - API Reference

SIP Trunking APIs enable you to connect your PBX, Contact Center, or Voice AI system to the telephone network (PSTN) via Exotel's infrastructure.

---

## Authentication

All API requests require HTTP Basic Authentication using your API credentials.

### Getting Your Credentials

1. Login to your Exotel Dashboard
2. Navigate to **API Credentials** section
3. Copy the following details:
   - **API Key** (username)
   - **API Token** (password)
   - **Account SID**

### Making Authenticated Requests

An HTTP request is made with Basic Authentication:

```
Authorization: Basic base64(<your_api_key>:<your_api_token>)
```

Or include credentials in the URL:

```
https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/...
```

Replace the following placeholders:
- `<your_api_key>` and `<your_api_token>` with the API key and token from your dashboard
- `<your_sid>` with your Account SID
- `<subdomain>` with the region of your account:
  - **Singapore cluster**: `api.exotel.com`
  - **Mumbai cluster**: `api.in.exotel.com`

### Rate Limits

| Limit Type | Value |
|------------|-------|
| Requests per minute | 200 |
| Concurrent connections | 50 |

---

# GETTING STARTED (PSTN Setup)

This section covers the APIs required to set up SIP Trunking for standard PSTN (telephone network) connectivity.

**Setup Flow:**
1. Create Trunk → 2. Map Phone Number → 3. Map ACL (for Outbound) → 4. Map Destination URI (for Inbound)

---

## 1. Create Trunk

Creates a new SIP trunk. This is the first step for all SIP Trunking use cases.

A SIP Trunk acts as a virtual connection between your communication system (PBX/Contact Center) and Exotel's telephony network.

### HTTP Request

```
POST https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

The following parameters are sent as JSON in the body of the request:

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| trunk_name | Mandatory | String; Unique identifier for the trunk. Must be alphanumeric with underscores only, maximum 16 characters. Example: `outbound_trunk`, `my_pbx_trunk` |
| nso_code | Mandatory | String; Network Service Operator code. Use `ANY-ANY` for standard configuration. |
| domain_name | Mandatory | String; SIP domain for the trunk. Format: `<your_sid>.pstn.exotel.com`. Example: `ameyo5m.pstn.exotel.com` |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "outbound_trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "<your_sid>.pstn.exotel.com"
  }'
```

### HTTP Response

On success, the HTTP response status code will be `200 OK`.

The `trunk_sid` is the unique identifier of the trunk - **save this value** as it will be required for all subsequent API calls.

### Example Response

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
      "domain_name": "ameyo5m.pstn.exotel.com",
      "auth_type": "IP-WHITELIST",
      "registration_enabled": "disabled",
      "edge_preference": "auto",
      "nso_code": "ANY-ANY",
      "secure_trunking": "disabled",
      "destination_uris": "/v2/accounts/ameyo5m/trunks/trmum1f708622631150902801a1n/destination-uris",
      "whitelisted_ips": "/v2/accounts/ameyo5m/trunks/trmum1f708622631150902801a1n/whitelisted-ips",
      "credentials": "/v2/accounts/ameyo5m/trunks/trmum1f708622631150902801a1n/credentials",
      "phone_numbers": "/v2/accounts/ameyo5m/trunks/trmum1f708622631150902801a1n/phone-numbers"
    }
  }
}
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| request_id | String; Unique identifier for this API request |
| method | String; HTTP method used (`POST`) |
| http_code | Integer; HTTP status code (`200` for success) |
| trunk_sid | String; **Important** - Unique identifier for the trunk. Save this for subsequent API calls. Example: `trmum1f708622631150902801a1n` |
| trunk_name | String; Name of the trunk as provided in request |
| domain_name | String; SIP domain for the trunk |
| status | String; Current trunk status: `active` - Trunk is ready for use, `inactive` - Trunk is disabled |
| auth_type | String; Authentication type. Currently only `IP-WHITELIST` is supported |
| registration_enabled | String; SIP registration status: `enabled` or `disabled` |
| edge_preference | String; Edge server preference. Default: `auto` |
| nso_code | String; Network Service Operator code |
| secure_trunking | String; TLS status: `enabled` or `disabled` |
| destination_uris | String; API path to manage destination URIs for this trunk |
| whitelisted_ips | String; API path to manage ACLs (whitelisted IPs) for this trunk |
| credentials | String; API path to credentials for this trunk |
| phone_numbers | String; API path to manage phone numbers for this trunk |
| date_created | String; ISO 8601 timestamp when trunk was created |
| date_updated | String; ISO 8601 timestamp when trunk was last updated |

### Error Responses

#### 400 Bad Request - Invalid trunk_name

```json
{
  "request_id": "a1b2c3d4e5f6",
  "method": "POST",
  "http_code": 400,
  "response": {
    "code": 400,
    "error_data": {
      "code": 1002,
      "message": "Invalid parameter",
      "description": "trunk_name must be alphanumeric with underscores only, max 16 characters"
    },
    "status": "failure",
    "data": null
  }
}
```

#### 409 Conflict - Duplicate trunk_name

```json
{
  "request_id": "b2c3d4e5f6a7",
  "method": "POST",
  "http_code": 409,
  "response": {
    "code": 409,
    "error_data": {
      "code": 1008,
      "message": "Duplicate resource",
      "description": "Trunk with name 'outbound_trunk' already exists"
    },
    "status": "failure",
    "data": null
  }
}
```

---

## 2. Map Phone Number to Trunk

Associates a phone number (DID/ExoPhone) with the trunk. This phone number will be used for making and receiving calls through the trunk.

### HTTP Request

```
POST https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| phone_number | Mandatory | String; The phone number to map to the trunk. Must be in E.164 format (with country code). Example: `+919876543210`, `+912247790597` |
| mode | Optional | String; Routing mode for the phone number. Can be: `pstn` (default) - Routes calls to telephone network, `flow` - Routes calls to Voice AI bot (StreamKit). If not specified, defaults to `null` and behaves as `pstn`. |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210"
  }'
```

**For StreamKit (Voice AI) mode:**

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

### HTTP Response

On success, the HTTP response status code will be `200 OK`.

**Important:** Save the `id` from the response - this numeric ID is required for the Update Phone Number Mode API.

### Example Response

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
      "trunk_sid": "trmum1f708622631150902801a1n",
      "date_created": "2026-01-23T10:26:54Z",
      "date_updated": "2026-01-23T10:26:54Z",
      "mode": null
    }
  }
}
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| id | String; **Important** - Numeric identifier for this phone number mapping. Save this value - required for Update Phone Number Mode API. Example: `41512` |
| phone_number | String; The mapped phone number in E.164 format |
| trunk_sid | String; The trunk this phone number is associated with |
| mode | String or null; Routing mode: `pstn` - PSTN routing, `flow` - StreamKit/Voice AI routing, `null` - Default (same as pstn) |
| date_created | String; ISO 8601 timestamp when mapping was created |
| date_updated | String; ISO 8601 timestamp when mapping was last updated |

### Error Responses

#### 404 Not Found - Invalid trunk_sid

```json
{
  "request_id": "e45544e19a7f4d5d956fefe63fe3c6b6",
  "method": "POST",
  "http_code": 404,
  "response": {
    "code": 404,
    "error_data": {
      "code": 1000,
      "message": "Not Found",
      "description": "Not Found"
    },
    "status": "failure",
    "data": null
  }
}
```

#### 409 Conflict - Phone number already mapped

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
      "description": "Unable to create DidTrunkMapping with TrunkSid trmum1f708622631150902801a1n"
    },
    "status": "failure",
    "data": null
  }
}
```

---

## 3. Map ACL to Trunk (Whitelist IP)

Registers your server's public IP address for authentication. This is required for **Outbound/Termination** calls - allowing your system to send calls through the trunk.

ACL (Access Control List) ensures only authorized IP addresses can use your trunk for outbound calling.

### HTTP Request

```
POST https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| ip | Mandatory | String; Your server's public IP address. Must be a valid IPv4 address. Example: `44.248.146.11`, `203.0.113.50` |
| mask | Optional | Integer; Subnet mask in CIDR notation. Default: `32` (single IP). Use `24` for /24 subnet, `16` for /16 subnet. Example: `32`, `24` |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "44.248.146.11",
    "mask": 32
  }'
```

### HTTP Response

On success, the HTTP response status code will be `200 OK`.

### Example Response

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
      "trunk_sid": "trmum1f708622631150902801a1n",
      "ip": "44.248.146.11",
      "friendly_name": null,
      "date_created": "2026-01-23T11:37:36Z",
      "date_updated": "2026-01-23T11:37:36Z"
    }
  }
}
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| id | String; Unique identifier for this ACL entry. Example: `1153` |
| ip | String; The whitelisted IP address |
| mask | Integer; Subnet mask in CIDR notation |
| trunk_sid | String; The trunk this ACL is associated with |
| friendly_name | String or null; Optional friendly name for the IP |
| date_created | String; ISO 8601 timestamp when ACL was created |
| date_updated | String; ISO 8601 timestamp when ACL was last updated |

### Error Responses

#### 409 Conflict - IP already whitelisted

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

---

## 4. Map Destination URI to Trunk

Configures where incoming calls should be routed. This is required for **Inbound/Origination** calls - routing calls from the telephone network to your system.

The destination can be an IP address or FQDN (Fully Qualified Domain Name) of your PBX/SBC.

### Important Notes

- **For IP-based destinations:** You MUST whitelist the IP using the "Map ACL to Trunk" API first
- **For FQDN-based destinations:** No whitelisting required (e.g., `sip.yourcompany.com`)
- The destination format is: `<ip_or_fqdn>:<port>;transport=<protocol>`
- You need to set

### HTTP Request

```
POST https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| destinations | Mandatory | Array; List of destination objects. Each object contains a `destination` field. |
| destinations[].destination | Mandatory | String; SIP URI in format `<ip_or_fqdn>:<port>;transport=<protocol>`. Port is typically `5061` for TLS or `5060` for TCP. Transport can be `tls` (recommended) or `tcp`. Example: `44.248.146.11:5061;transport=tls`, `sip.company.com:5061;transport=tls` |

### Example Request (IP-based destination)

**Note:** Ensure the IP `44.248.146.11` is whitelisted first using Map ACL API.

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {
        "destination": "44.248.146.11:5061;transport=tls"
      }
    ]
  }'
```

### Example Request (FQDN-based destination)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {
        "destination": "sip.yourcompany.com:5061;transport=tls"
      }
    ]
  }'
```

### HTTP Response

On success, the HTTP response status code will be `200 OK` or `207 Multi-Status` (for partial success/failure).

The response includes `metadata` with counts of successful and failed destinations.

### Example Response (Success)

```json
{
  "request_id": "63999f0a98a24a0aa58ab5b74aec9f0a",
  "method": "POST",
  "http_code": 200,
  "metadata": {
    "total": 1,
    "success": 1,
    "failed": 0
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
        "trunk_sid": "trmum1f708622631150902801a1n"
      }
    }
  ]
}
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| metadata.total | Integer; Total number of destinations in request |
| metadata.success | Integer; Number of successfully added destinations |
| metadata.failed | Integer; Number of failed destinations |
| id | String; Unique identifier for this destination URI. Example: `2543` |
| destination | String; The SIP URI (prefixed with `sip:`) |
| type | String; Destination type: `public` |
| priority | Integer; Priority for load balancing. Lower values = higher priority. Default: `0` |
| weight | Integer; Weight for load balancing. Higher values = more traffic. Default: `1` |
| trunk_sid | String; The trunk this destination is associated with |
| date_created | String; ISO 8601 timestamp when destination was created |
| date_updated | String; ISO 8601 timestamp when destination was last updated |

### Error Responses

#### 400 Bad Request - Destination not whitelisted

This error occurs when you try to add an IP-based destination that hasn't been whitelisted.

**Solution:** Use the "Map ACL to Trunk" API to whitelist the IP first.

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

#### 400 Bad Request - Invalid IP or FQDN

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

###for Inbound SIP 
a. Create a Flow using Connect Applet in App Bazaar: https://my.in.exotel.com/apps

b. Use sip:<TrunkID> in the Dial Whom field

c. Map DID to flow through Exophone: https://my.in.exotel.com/numbers

d. Check inbound call flow by dialling Exophone/phonenumber to your system via Exotel SIP trunking


---

# STREAMKIT SETUP (Voice AI)

StreamKit enables you to connect your Contact Center to Voice AI bots. The setup is similar to PSTN, but uses `mode: flow` when mapping phone numbers.

**Setup Flow:**
1. Create Trunk → 2. Map Phone Number (mode: flow) → 3. Map ACL to Trunk

---

## StreamKit: Create Trunk

Same as PSTN setup. Refer to [Create Trunk](#1-create-trunk) above.

---

## StreamKit: Map Phone Number (Flow Mode)

Same endpoint as PSTN, but with `mode: flow` to route calls to Voice AI bot.

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "mode": "flow"
  }'
```

### Example Response

```json
{
  "request_id": "9351dabddc21476e8351d662f1ce31e1",
  "method": "POST",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "id": "41523",
      "phone_number": "+919876543210",
      "trunk_sid": "trmum1f708622631150902801a1n",
      "date_created": "2026-01-23T13:28:11Z",
      "date_updated": "2026-01-23T13:28:11Z",
      "mode": "flow"
    }
  }
}
```

---

## StreamKit: Map ACL to Trunk

Same as PSTN setup. Refer to [Map ACL to Trunk](#3-map-acl-to-trunk-whitelist-ip) above.

Build Flow and Map DID

a. Follow https://docs.exotel.com/exotel-agentstream/streamkit-cloud for end-to-end steps

b. Create flow in AppBazaar with Voicebot applet and passthru applet: https://my.in.exotel.com/apps

c. Procure SIP exophone or contact support

d. Map DID to flow through Exophone: https://my.in.exotel.com/numbers


---

# MANAGE & VIEW

APIs for viewing configurations, updating settings, and managing your trunk.

---

## 5. Get Phone Numbers

Retrieves all phone numbers mapped to a trunk.

### HTTP Request

```
GET https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers"
```

### Example Response

```json
{
  "request_id": "785471d288054cbf8c677b75e0b5f2f8",
  "method": "GET",
  "http_code": 200,
  "metadata": {
    "page_size": 50,
    "first_page_uri": "/v2/accounts/ameyo5m/trunks/trmum1f708622631150902801a1n/phone-numbers?offset=0&page_size=50",
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
        "trunk_sid": "trmum1f708622631150902801a1n",
        "date_created": "2026-01-23T13:28:11Z",
        "date_updated": "2026-01-23T13:41:59Z",
        "mode": "flow"
      }
    }
  ]
}
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| metadata.page_size | Integer; Number of results per page |
| metadata.first_page_uri | String; URI for the first page |
| metadata.prev_page_uri | String or null; URI for previous page (null if on first page) |
| metadata.next_page_uri | String or null; URI for next page (null if on last page) |
| response[] | Array; List of phone number objects |

---

## 6. Get ACLs (Whitelisted IPs)

Retrieves all whitelisted IP addresses for a trunk.

### HTTP Request

```
GET https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips"
```

### Example Response

```json
{
  "request_id": "91dc982ca79846479c6f9678c788cfc1",
  "method": "GET",
  "http_code": 200,
  "metadata": {
    "page_size": 50,
    "first_page_uri": "/v2/accounts/ameyo5m/trunks/trmum1f708622631150902801a1n/whitelisted-ips?offset=0&page_size=50",
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
        "trunk_sid": "trmum1f708622631150902801a1n",
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

## 7. Get Destination URIs

Retrieves all destination URIs configured for a trunk.

### HTTP Request

```
GET https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris"
```

### Example Response

```json
{
  "request_id": "bfc1544ab0ab4df3ae49173ccc744331",
  "method": "GET",
  "http_code": 200,
  "metadata": {
    "page_size": 50,
    "first_page_uri": "/v2/accounts/ameyo5m/trunks/trmum1f708622631150902801a1n/destination-uris?offset=0&page_size=50",
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
        "destination": "sip:sip.company.com:5061;transport=tls",
        "date_created": "2026-01-23T13:39:06Z",
        "date_updated": "2026-01-23T13:39:06Z",
        "type": "public",
        "priority": 0,
        "weight": 1,
        "trunk_sid": "trmum1f708622631150902801a1n"
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
        "trunk_sid": "trmum1f708622631150902801a1n"
      }
    }
  ]
}
```

---

## 8. Update Phone Number Mode

Updates the routing mode for a mapped phone number. Use this to switch between PSTN and StreamKit (Voice AI) modes.

### HTTP Request

```
PUT https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers/<phone_number_id>
```

**Important:** The `<phone_number_id>` is the **numeric ID** returned when you mapped the phone number (e.g., `41523`), NOT the phone number itself.

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| phone_number | Mandatory | String; The phone number in E.164 format. Must match the phone number associated with the ID. Example: `+919876543210` |
| mode | Mandatory | String; The new routing mode. Can be: `pstn` - Route calls to telephone network, `flow` - Route calls to Voice AI bot (StreamKit) |

### Example Request (Switch to Flow mode)

```bash
curl -X PUT "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers/41523" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+918040264208",
    "mode": "flow"
  }'
```

### Example Request (Switch to PSTN mode)

```bash
curl -X PUT "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers/41523" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+918040264208",
    "mode": "pstn"
  }'
```

### Example Response

```json
{
  "request_id": "c719cd56eb5943e789e1bdbd4ce1515a",
  "method": "PUT",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "id": "41523",
      "phone_number": "+918040264208",
      "trunk_sid": "trmum1f708622631150902801a1n",
      "date_created": "2026-01-23T13:28:11Z",
      "date_updated": "2026-01-23T13:41:59Z",
      "mode": "flow"
    }
  }
}
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| id | String; The phone number mapping ID |
| phone_number | String; The phone number in E.164 format |
| trunk_sid | String; The associated trunk |
| mode | String; The updated routing mode (`pstn` or `flow`) |
| date_created | String; ISO 8601 timestamp when mapping was created |
| date_updated | String; ISO 8601 timestamp when mapping was updated (will be updated after this call) |

---

## 9. Set Trunk Alias (Caller ID)

Sets the phone number displayed to called parties on outbound calls. This is useful when you want to display a specific caller ID regardless of which phone number is mapped to the trunk.

### HTTP Request

```
POST https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/settings
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| settings | Mandatory | Array; List of setting objects |
| settings[].name | Mandatory | String; Setting name. Use `trunk_external_alias` for caller ID |
| settings[].value | Mandatory | String; The phone number to display as caller ID. Should be in E.164 format. Example: `+919876543210` |

### Example Request

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

### Example Response

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
        "trunk_sid": "trmum1f708622631150902801a1n",
        "date_created": "2026-01-23T13:34:50Z",
        "date_updated": "2026-01-23T13:34:50Z"
      }
    }
  ]
}
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| metadata.total | Integer; Total number of settings in request |
| metadata.success | Integer; Number of successfully applied settings |
| name | String; Setting name (`trunk_external_alias`) |
| value | String; The caller ID phone number |
| trunk_sid | String; The associated trunk |
| date_created | String; ISO 8601 timestamp when setting was created |
| date_updated | String; ISO 8601 timestamp when setting was last updated |

---

## 10. Delete Trunk

Permanently deletes a trunk and all its associated configurations (phone numbers, ACLs, destination URIs).

**⚠️ Warning:** This action cannot be undone. All associated phone number mappings, whitelisted IPs, and destination URIs will be permanently deleted.

### HTTP Request

```
DELETE https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks?trunk_sid=<trunk_sid>
```

### Example Request

```bash
curl -X DELETE "https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/trunks?trunk_sid=<trunk_sid>"
```

### Example Response

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
      "secure_trunking": "disabled",
      "destination_uris": "/v2/accounts/ameyo5m/trunks/trmum15f77c83605998cdb9d1a1n/destination-uris",
      "whitelisted_ips": "/v2/accounts/ameyo5m/trunks/trmum15f77c83605998cdb9d1a1n/whitelisted-ips",
      "credentials": "/v2/accounts/ameyo5m/trunks/trmum15f77c83605998cdb9d1a1n/credentials",
      "phone_numbers": "/v2/accounts/ameyo5m/trunks/trmum15f77c83605998cdb9d1a1n/phone-numbers"
    }
  }
}
```

### Response Parameters

The response returns the full trunk data that was deleted, allowing you to verify which trunk was removed.

---

# Error Codes Reference

| Error Code | HTTP Status | Message | Description |
|------------|-------------|---------|-------------|
| 1000 | 404 | Not Found | Resource not found (invalid trunk_sid, phone_number_id, etc.) |
| 1001 | 400 | Mandatory Parameter missing | Required parameter not provided |
| 1002 | 400 | Invalid parameter | Parameter value is invalid or malformed |
| 1007 | 400 | Invalid request body | JSON parsing error or malformed request body |
| 1008 | 409 | Duplicate resource | Resource already exists (duplicate trunk name, IP already whitelisted, etc.) |
| 1011 | 415 | Unsupported content type | Wrong Content-Type header. Use `application/json` |

---

# Quick Reference

## API Endpoints Summary

| API | Method | Endpoint |
|-----|--------|----------|
| Create Trunk | POST | `/v2/accounts/{sid}/trunks` |
| Map Phone Number | POST | `/v2/accounts/{sid}/trunks/{trunk_sid}/phone-numbers` |
| Map ACL | POST | `/v2/accounts/{sid}/trunks/{trunk_sid}/whitelisted-ips` |
| Map Destination URI | POST | `/v2/accounts/{sid}/trunks/{trunk_sid}/destination-uris` |
| Get Phone Numbers | GET | `/v2/accounts/{sid}/trunks/{trunk_sid}/phone-numbers` |
| Get ACLs | GET | `/v2/accounts/{sid}/trunks/{trunk_sid}/whitelisted-ips` |
| Get Destination URIs | GET | `/v2/accounts/{sid}/trunks/{trunk_sid}/destination-uris` |
| Update Phone Number Mode | PUT | `/v2/accounts/{sid}/trunks/{trunk_sid}/phone-numbers/{id}` |
| Set Trunk Alias | POST | `/v2/accounts/{sid}/trunks/{trunk_sid}/settings` |
| Delete Trunk | DELETE | `/v2/accounts/{sid}/trunks?trunk_sid={trunk_sid}` |

## Mode Options

| Mode | Description | Use Case |
|------|-------------|----------|
| `pstn` | Routes calls to telephone network | Standard PBX/Contact Center integration |
| `flow` | Routes calls to Voice AI bot | StreamKit/Voice AI integration |

## Common Setup Flows

### PSTN (Outbound + Inbound)
```
Create Trunk → Map Phone Number → Map ACL → Map Destination URI
```

### StreamKit (Voice AI)
```
Create Trunk → Map Phone Number (mode: flow) → Map ACL
```

---

# Support

- Documentation: https://developer.exotel.com
- Email: support@exotel.com
