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

## Authentication

Replace `<your_api_key>` and `<your_api_token>` with the API key and token created by you.

- Replace `<your_sid>` with your "Account SID"
- Replace `<subdomain>` with the region of your account
  - `<subdomain>` of Singapore cluster is `@api.exotel.com`
  - `<subdomain>` of Mumbai cluster is `@api.in.exotel.com`

`<your_api_key>`, `<your_api_token>` and `<your_sid>` are available in the **API Settings** page of your [Exotel Dashboard](https://my.exotel.com/apisettings/site#api-credentials)

---

# API Reference

---

## Create Trunk

Creates a virtual connection between your system and Exotel's PSTN gateway.

An HTTP POST request is made to:

```
POST
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks
```

### Request Parameters

The following are the POST parameters sent in the body of the request:

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| trunk_name | Mandatory | String; Unique name for the trunk (max 16 characters, alphanumeric and underscore only) |
| nso_code | Mandatory | String; Network Service Operator code. Use `ANY-ANY` |
| domain_name | Mandatory | String; Domain for the trunk. Format: `<your_sid>.pstn.exotel.com` |

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

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| request_id | String; Unique identifier of the request |
| method | String; HTTP method used |
| http_code | Integer; HTTP status code |
| status | String; `success` or `failure` |
| trunk_sid | String; Unique identifier of the trunk. Use this in subsequent API calls |
| trunk_name | String; Name of the trunk |
| domain_name | String; SIP domain for the trunk |
| nso_code | String; Network Service Operator code |
| date_created | String; Timestamp in format `YYYY-MM-DDTHH:mm:ssZ` |
| date_updated | String; Timestamp of last update |

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
      "date_created": "2025-01-22T10:00:00Z",
      "date_updated": "2025-01-22T10:00:00Z"
    }
  }
}
```

---

## Map Phone Number

Associates a phone number (DID/ExoPhone) with your trunk.

- **For Termination:** This becomes your outbound Caller ID
- **For Origination:** This is the number customers dial to reach you

An HTTP POST request is made to:

```
POST
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers
```

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| phone_number | Mandatory | String; Phone number in [E.164 format](https://en.wikipedia.org/wiki/E.164). Example: `+919XXXXXXXXX` |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919XXXXXXXXX"
  }'
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| id | String; Unique identifier of the phone number mapping |
| phone_number | String; The mapped phone number |
| trunk_sid | String; Associated trunk identifier |
| date_created | String; Timestamp in format `YYYY-MM-DDTHH:mm:ssZ` |

### Example Response

```json
{
  "request_id": "b2c3d4e5f6g7",
  "method": "POST",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": {
      "id": "<phone_number_id>",
      "phone_number": "+919XXXXXXXXX",
      "trunk_sid": "<trunk_sid>",
      "date_created": "2025-01-22T10:05:00Z"
    }
  }
}
```

---

## Whitelist IP Address

Registers your server's IP address for secure authentication. **Required for Termination.**

An HTTP POST request is made to:

```
POST
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips
```

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| ip | Mandatory | String; IPv4 address of your server |
| mask | Mandatory | Integer; Subnet mask (16-32). Use `32` for single IP address |

**Mask Reference:**

| Mask | IPs Covered | Use Case |
|------|-------------|----------|
| 32 | 1 | Single server |
| 28 | 16 | Small cluster |
| 24 | 256 | Large deployment |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "<your_server_ip>",
    "mask": 32
  }'
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| id | String; Unique identifier of the whitelist entry |
| ip | String; Whitelisted IP address |
| mask | Integer; Subnet mask |
| trunk_sid | String; Associated trunk identifier |
| date_created | String; Timestamp in format `YYYY-MM-DDTHH:mm:ssZ` |

### Example Response

```json
{
  "request_id": "c3d4e5f6g7h8",
  "method": "POST",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": {
      "id": "<whitelist_id>",
      "ip": "<your_server_ip>",
      "mask": 32,
      "trunk_sid": "<trunk_sid>",
      "date_created": "2025-01-22T10:10:00Z"
    }
  }
}
```

---

## Add Destination URI

Tells Exotel where to send incoming calls — your server's SIP address. **Required for Origination.**

An HTTP POST request is made to:

```
POST
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris
```

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| destinations | Mandatory | Array; Array of destination objects |
| destinations[].destination | Mandatory | String; SIP destination. Format: `<ip>:<port>;transport=<protocol>` |

**Transport Options:**

| Transport | Port | Security | Recommendation |
|-----------|------|----------|----------------|
| tls | 5061 | Encrypted | ✅ Recommended for production |
| tcp | 5060 | Unencrypted | Legacy systems only |

### Example Request (TLS - Recommended)

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "<your_server_ip>:5061;transport=tls" }
    ]
  }'
```

### Example Request (TCP)

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "<your_server_ip>:5060;transport=tcp" }
    ]
  }'
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| id | String; Unique identifier of the destination |
| destination | String; Full SIP URI |
| trunk_sid | String; Associated trunk identifier |
| date_created | String; Timestamp in format `YYYY-MM-DDTHH:mm:ssZ` |

### Example Response

```json
{
  "request_id": "d4e5f6g7h8i9",
  "method": "POST",
  "http_code": 200,
  "response": [
    {
      "status": "success",
      "code": 200,
      "data": {
        "id": "<destination_id>",
        "destination": "sip:<your_server_ip>:5061;transport=tls",
        "trunk_sid": "<trunk_sid>",
        "date_created": "2025-01-22T10:15:00Z"
      }
    }
  ]
}
```

---

## Get Destination URIs

Retrieves all destination URIs configured for a trunk.

An HTTP GET request is made to:

```
GET
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json"
```

### Example Response

```json
{
  "request_id": "e5f6g7h8i9j0",
  "method": "GET",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": [
      {
        "id": "<destination_id>",
        "destination": "sip:<your_server_ip>:5061;transport=tls",
        "trunk_sid": "<trunk_sid>",
        "date_created": "2025-01-22T10:15:00Z"
      }
    ]
  }
}
```

---

## Get Whitelisted IPs

Retrieves all whitelisted IPs for a trunk.

An HTTP GET request is made to:

```
GET
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json"
```

### Example Response

```json
{
  "request_id": "f6g7h8i9j0k1",
  "method": "GET",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": [
      {
        "id": "<whitelist_id>",
        "ip": "<your_server_ip>",
        "mask": 32,
        "trunk_sid": "<trunk_sid>",
        "date_created": "2025-01-22T10:10:00Z"
      }
    ]
  }
}
```

---

## Get Credentials

Retrieves SIP authentication credentials for the trunk.

An HTTP GET request is made to:

```
GET
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/credentials
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/credentials" \
  -H "Content-Type: application/json"
```

### Response Parameters

| Parameter Name | Type & Value |
|----------------|--------------|
| username | String; SIP authentication username (same as trunk_sid) |
| password | String; SIP authentication password |

### Example Response

```json
{
  "request_id": "g7h8i9j0k1l2",
  "method": "GET",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": {
      "username": "<trunk_sid>",
      "password": "<sip_password>"
    }
  }
}
```

---

## Get Phone Numbers

Retrieves all phone numbers mapped to a trunk.

An HTTP GET request is made to:

```
GET
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json"
```

### Example Response

```json
{
  "request_id": "h8i9j0k1l2m3",
  "method": "GET",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": [
      {
        "id": "<phone_number_id>",
        "phone_number": "+919XXXXXXXXX",
        "trunk_sid": "<trunk_sid>",
        "date_created": "2025-01-22T10:05:00Z"
      }
    ]
  }
}
```

---

## Set Trunk Alias

Sets an external Caller ID alias for the trunk.

An HTTP POST request is made to:

```
POST
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/settings
```

### Request Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| settings | Mandatory | Array; Array of setting objects |
| settings[].name | Mandatory | String; Setting name. Use `trunk_external_alias` |
| settings[].value | Mandatory | String; Phone number for Caller ID in E.164 format |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks/<trunk_sid>/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "settings": [
      { "name": "trunk_external_alias", "value": "+919XXXXXXXXX" }
    ]
  }'
```

### Example Response

```json
{
  "request_id": "i9j0k1l2m3n4",
  "method": "POST",
  "http_code": 200,
  "response": [
    {
      "status": "success",
      "code": 200,
      "data": {
        "name": "trunk_external_alias",
        "value": "+919XXXXXXXXX",
        "trunk_sid": "<trunk_sid>",
        "date_created": "2025-01-22T10:20:00Z"
      }
    }
  ]
}
```

---

## Delete Trunk

⚠️ **Permanently deletes** the trunk and all its configurations. This action cannot be undone.

An HTTP DELETE request is made to:

```
DELETE
https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks?trunk_sid=<trunk_sid>
```

### Query Parameters

| Parameter Name | Mandatory/Optional | Value |
|----------------|-------------------|-------|
| trunk_sid | Mandatory | String; Trunk identifier to delete |

### Example Request

```bash
curl -X DELETE "https://<your_api_key>:<your_api_token><subdomain>/v2/accounts/<your_sid>/trunks?trunk_sid=<trunk_sid>" \
  -H "Content-Type: application/json"
```

### Example Response

```json
{
  "request_id": "j0k1l2m3n4o5",
  "method": "DELETE",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": null
  }
}
```

---

# HTTP Status Codes

| HTTP Code | Status | Description |
|-----------|--------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Invalid API credentials |
| 403 | Forbidden | Access denied to resource |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

---

# Error Codes

| Error Code | HTTP Status | Message | Description |
|------------|-------------|---------|-------------|
| 1000 | 400 | Invalid request | Missing or invalid required field |
| 1001 | 400 | Invalid parameter | Parameter value is invalid |
| 1002 | 409 | Resource exists | Trunk or phone number already exists |
| 1003 | 404 | Resource not found | Trunk SID does not exist |
| 1010 | 401 | Authorization failed | Invalid API key or token |
| 1011 | 403 | Access denied | No permission for this resource |
| 1020 | 422 | Validation error | Request validation failed |
| 1030 | 429 | Rate limit exceeded | Too many requests |

---

# Error Response Format

```json
{
  "request_id": "xyz123",
  "method": "POST",
  "http_code": 400,
  "response": {
    "status": "failure",
    "code": 400,
    "error_data": {
      "code": 1000,
      "message": "Invalid request",
      "description": "Missing required field: trunk_name"
    }
  }
}
```

---

# Postman Collection

Import `postman/Exotel_vSIP_API_Collection.json` into Postman.

**Setup:**
1. Import the collection
2. Go to **Authorization** tab → Select **Basic Auth**
3. Enter your **API Key** as Username
4. Enter your **API Token** as Password
5. In the URL, replace:
   - `<subdomain>` → `api.in.exotel.com` (India) or `api.exotel.com` (Singapore)
   - `<your_sid>` → Your Account SID
   - `<trunk_sid>` → Trunk SID (from Create Trunk response)
6. Fill parameters in **Body** tab (form-data)
7. Click **Send**

---

# Support

- Documentation: https://developer.exotel.com
- Email: support@exotel.com
