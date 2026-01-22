# Exotel Voice Trunking APIs

Connect your communication system to the telephone network using Exotel's Voice Trunking service.

---

# What is SIP Trunking?

## Overview

SIP (Session Initiation Protocol) Trunking is a method of delivering voice and other communication services over the internet. It replaces traditional telephone lines (PRI/ISDN) with a virtual connection that carries voice traffic as data packets.

A **SIP Trunk** is a virtual phone line that connects your Private Branch Exchange (PBX), Session Border Controller (SBC), or any SIP-enabled communication system to the Public Switched Telephone Network (PSTN) through Exotel's gateway.

## How It Works

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         SIP TRUNKING ARCHITECTURE                          │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  YOUR SYSTEM    │       │     EXOTEL      │       │      PSTN       │
│                 │       │                 │       │                 │
│  - PBX          │       │  - SIP Gateway  │       │  - Mobile       │
│  - Contact      │  SIP  │  - Media Server │ SS7/  │  - Landline     │
│    Center       │<----->│  - Routing      │ PSTN  │  - International│
│  - SBC          │       │  - Recording    │<----->│                 │
│  - Obot/IVR     │       │  - Analytics    │       │                 │
│                 │       │                 │       │                 │
└─────────────────┘       └─────────────────┘       └─────────────────┘
     Your Network              Exotel Cloud           Telephone Network
```

## Benefits

| Benefit | Description |
|---------|-------------|
| Cost Reduction | Eliminate expensive PRI lines and hardware |
| Scalability | Add or remove channels instantly via API |
| Flexibility | Connect any SIP-compatible system |
| Geographic Freedom | Use phone numbers from any supported region |
| Unified Communications | Combine voice with your digital workflows |

---

# Call Direction

## Terminology

| Term | Also Known As | Direction | Description |
|------|---------------|-----------|-------------|
| Outbound | Termination | Your System to PSTN | Calls you make to external phone numbers |
| Inbound | Origination | PSTN to Your System | Calls you receive from external phone numbers |

## Outbound / Termination

Your system initiates a call to a phone number on the PSTN.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    OUTBOUND / TERMINATION FLOW                          │
└─────────────────────────────────────────────────────────────────────────┘

     YOUR SYSTEM                    EXOTEL                      PSTN
         │                            │                           │
         │  1. SIP INVITE             │                           │
         │  (from whitelisted IP)     │                           │
         │--------------------------->│                           │
         │                            │  2. Route to PSTN         │
         │                            │-------------------------->│
         │                            │                           │
         │                            │  3. PSTN connects call    │
         │                            │<------------------------->│
         │  4. Call established       │                           │
         │<-------------------------->│                           │
         │                            │                           │
```

**Connectivity Requirement:** Static public IP address (FQDN not supported)

**Setup Steps:**
1. Create a trunk
2. Map your caller ID (ExoPhone/DID)
3. Whitelist your static public IP

**Use Cases:**
- Outbound sales and support calls
- Click-to-call from CRM/applications
- Automated dialer campaigns
- Bot-initiated calls
- Notifications and reminders

---

## Inbound / Origination

External callers dial your phone number, and the call is routed to your system.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INBOUND / ORIGINATION FLOW                           │
└─────────────────────────────────────────────────────────────────────────┘

     PSTN                           EXOTEL                    YOUR SYSTEM
       │                              │                            │
       │  1. Customer dials           │                            │
       │  your ExoPhone number        │                            │
       │----------------------------->│                            │
       │                              │  2. SIP INVITE             │
       │                              │  (to your IP or FQDN)      │
       │                              │--------------------------->│
       │                              │                            │
       │                              │  3. Your system answers    │
       │                              │<---------------------------|
       │  4. Call established         │                            │
       │<---------------------------->│<-------------------------->│
       │                              │                            │
```

**Connectivity Options:** Static IP address OR FQDN (DNS-based routing)

**Setup Steps:**
1. Create a trunk
2. Map the customer-facing phone number (ExoPhone/DID)
3. Add destination URI (your server's IP or FQDN)

**Use Cases:**
- Inbound customer support lines
- IVR and call routing
- Contact center queues
- SIP-to-bot integrations
- Toll-free number handling

---

# Quick Start

## Prerequisites

| Requirement | Description | Where to Get |
|-------------|-------------|--------------|
| Exotel Account | Active Exotel account | [Sign up](https://exotel.com/signup) |
| API Credentials | API Key and API Token | [API Settings](https://my.exotel.com/apisettings/site#api-credentials) |
| Account SID | Your unique account identifier | [API Settings](https://my.exotel.com/apisettings/site#api-credentials) |
| ExoPhone | Virtual phone number (DID) | [Number Manager](https://my.exotel.com/numbers) |
| SIP Server | Your PBX/SBC with static IP or FQDN | Your infrastructure |

---

## Outbound / Termination Setup

### Step 1: Create Trunk

### Step 2: Map Phone Number

### Step 3: Whitelist IP

### Step 4: Get Credentials and Configure PBX

| PBX Setting | Value |
|-------------|-------|
| SIP Server | `<your_sid>.pstn.exotel.com` |
| Port | 5060 (TCP) or 5061 (TLS) |
| Username | Value of `trunk_sid` from Create Trunk response |
| Password | Value from Get Credentials API |
| Caller ID | Your mapped phone number |

---

## Inbound / Origination Setup

### Step 1: Create Trunk

### Step 2: Map Phone Number

### Step 3: Add Destination URI

---

# API Reference

## Authentication

All API requests require HTTP Basic Authentication.

| Parameter | Description |
|-----------|-------------|
| Username | Your API Key |
| Password | Your API Token |

**Base URL Format:**
```
https://<your_api_key>:<your_api_token>@<subdomain>/v2/accounts/<your_sid>/
```

**Subdomain by Region:**

| Region | Subdomain |
|--------|-----------|
| India (Mumbai) | api.in.exotel.com |
| Singapore | api.exotel.com |

---

## Create Trunk

Creates a new SIP trunk that serves as the virtual connection between your system and Exotel's PSTN gateway.

### HTTP Request

```
POST /v2/accounts/<your_sid>/trunks
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trunk_name | String | Yes | Unique identifier for the trunk. Maximum 16 characters. Only alphanumeric characters and underscores allowed. |
| nso_code | String | Yes | Network Service Operator code. Use `ANY-ANY` for standard routing. |
| domain_name | String | Yes | SIP domain for the trunk. Format: `<your_sid>.pstn.exotel.com` |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "my_trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "<your_sid>.pstn.exotel.com"
  }'
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response.status | String | `success` or `failure` |
| response.code | Integer | Response code |
| response.data.trunk_sid | String | Unique identifier for the created trunk. Use this in all subsequent API calls. |
| response.data.trunk_name | String | Name of the trunk |
| response.data.domain_name | String | SIP domain assigned to the trunk |
| response.data.nso_code | String | Network Service Operator code |
| response.data.date_created | String | Timestamp of creation in ISO 8601 format |
| response.data.date_updated | String | Timestamp of last update in ISO 8601 format |

### Example Response

```json
{
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "method": "POST",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": {
      "trunk_sid": "trind1a2b3c4d5e6f7890abcdef",
      "trunk_name": "my_trunk",
      "domain_name": "mycompany.pstn.exotel.com",
      "nso_code": "ANY-ANY",
      "date_created": "2025-01-22T10:30:00Z",
      "date_updated": "2025-01-22T10:30:00Z"
    }
  }
}
```

---

## Map Phone Number

Associates a phone number (ExoPhone/DID) with your trunk. For outbound calls, this becomes your Caller ID. For inbound calls, this is the number customers dial to reach you.

### HTTP Request

```
POST /v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| phone_number | String | Yes | Phone number in E.164 format. Must include country code with + prefix. Example: `+919876543210` |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210"
  }'
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response.status | String | `success` or `failure` |
| response.code | Integer | Response code |
| response.data.id | String | Unique identifier for the phone number mapping |
| response.data.phone_number | String | The mapped phone number |
| response.data.trunk_sid | String | Associated trunk identifier |
| response.data.date_created | String | Timestamp of creation in ISO 8601 format |

### Example Response

```json
{
  "request_id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
  "method": "POST",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": {
      "id": "pn_abc123def456",
      "phone_number": "+919876543210",
      "trunk_sid": "trind1a2b3c4d5e6f7890abcdef",
      "date_created": "2025-01-22T10:35:00Z"
    }
  }
}
```

---

## Whitelist IP Address

Registers your server's public IP address for authentication. Required for Outbound / Termination calls. Exotel validates incoming SIP requests against this whitelist.

### HTTP Request

```
POST /v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ip | String | Yes | IPv4 address of your SIP server. Must be a public, static IP address. |
| mask | Integer | Yes | Subnet mask in CIDR notation (16-32). Use 32 for a single IP address. |

**Subnet Mask Reference:**

| Mask | IPs Covered | Use Case |
|------|-------------|----------|
| 32 | 1 | Single server |
| 30 | 4 | Small cluster |
| 28 | 16 | Medium deployment |
| 24 | 256 | Large deployment |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "203.0.113.50",
    "mask": 32
  }'
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response.status | String | `success` or `failure` |
| response.code | Integer | Response code |
| response.data.id | String | Unique identifier for the whitelist entry |
| response.data.ip | String | Whitelisted IP address |
| response.data.mask | Integer | Subnet mask |
| response.data.trunk_sid | String | Associated trunk identifier |
| response.data.date_created | String | Timestamp of creation in ISO 8601 format |

### Example Response

```json
{
  "request_id": "c3d4e5f6-a7b8-9012-cdef-345678901234",
  "method": "POST",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": {
      "id": "wl_xyz789abc012",
      "ip": "203.0.113.50",
      "mask": 32,
      "trunk_sid": "trind1a2b3c4d5e6f7890abcdef",
      "date_created": "2025-01-22T10:40:00Z"
    }
  }
}
```

---

## Add Destination URI

Configures where Exotel should route incoming calls. Required for Inbound / Origination calls. You can specify either an IP address or FQDN.

### HTTP Request

```
POST /v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| destinations | Array | Yes | Array of destination objects |
| destinations[].destination | String | Yes | SIP URI in format: `<host>:<port>;transport=<protocol>` |

**Destination Format:**

| Component | Description | Example |
|-----------|-------------|---------|
| host | IP address or FQDN | `203.0.113.50` or `sip.company.com` |
| port | SIP port number | `5060` (TCP) or `5061` (TLS) |
| transport | Protocol | `tcp` or `tls` (recommended) |

### Example Request (Using IP)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {
        "destination": "203.0.113.50:5061;transport=tls"
      }
    ]
  }'
```

### Example Request (Using FQDN)

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {
        "destination": "sip.mycompany.com:5061;transport=tls"
      }
    ]
  }'
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response | Array | Array of response objects for each destination |
| response[].status | String | `success` or `failure` |
| response[].code | Integer | Response code |
| response[].data.id | String | Unique identifier for the destination |
| response[].data.destination | String | Full SIP URI |
| response[].data.trunk_sid | String | Associated trunk identifier |
| response[].data.date_created | String | Timestamp of creation in ISO 8601 format |

### Example Response

```json
{
  "request_id": "d4e5f6a7-b8c9-0123-def0-456789012345",
  "method": "POST",
  "http_code": 200,
  "response": [
    {
      "status": "success",
      "code": 200,
      "data": {
        "id": "du_mno345pqr678",
        "destination": "sip:203.0.113.50:5061;transport=tls",
        "trunk_sid": "trind1a2b3c4d5e6f7890abcdef",
        "date_created": "2025-01-22T10:45:00Z"
      }
    }
  ]
}
```

---

## Get Destination URIs

Retrieves all destination URIs configured for a trunk.

### HTTP Request

```
GET /v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/destination-uris" \
  -H "Content-Type: application/json"
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response.status | String | `success` or `failure` |
| response.code | Integer | Response code |
| response.data | Array | Array of destination URI objects |
| response.data[].id | String | Unique identifier for the destination |
| response.data[].destination | String | Full SIP URI |
| response.data[].trunk_sid | String | Associated trunk identifier |
| response.data[].date_created | String | Timestamp of creation |

### Example Response

```json
{
  "request_id": "e5f6a7b8-c9d0-1234-ef01-567890123456",
  "method": "GET",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": [
      {
        "id": "du_mno345pqr678",
        "destination": "sip:203.0.113.50:5061;transport=tls",
        "trunk_sid": "trind1a2b3c4d5e6f7890abcdef",
        "date_created": "2025-01-22T10:45:00Z"
      }
    ]
  }
}
```

---

## Get Whitelisted IPs

Retrieves all whitelisted IP addresses for a trunk.

### HTTP Request

```
GET /v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/whitelisted-ips" \
  -H "Content-Type: application/json"
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response.status | String | `success` or `failure` |
| response.code | Integer | Response code |
| response.data | Array | Array of whitelisted IP objects |
| response.data[].id | String | Unique identifier for the whitelist entry |
| response.data[].ip | String | Whitelisted IP address |
| response.data[].mask | Integer | Subnet mask |
| response.data[].trunk_sid | String | Associated trunk identifier |
| response.data[].date_created | String | Timestamp of creation |

### Example Response

```json
{
  "request_id": "f6a7b8c9-d0e1-2345-f012-678901234567",
  "method": "GET",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": [
      {
        "id": "wl_xyz789abc012",
        "ip": "203.0.113.50",
        "mask": 32,
        "trunk_sid": "trind1a2b3c4d5e6f7890abcdef",
        "date_created": "2025-01-22T10:40:00Z"
      }
    ]
  }
}
```

---

## Get Credentials

Retrieves SIP authentication credentials for the trunk. Use these credentials to configure your PBX or SBC.

### HTTP Request

```
GET /v2/accounts/<your_sid>/trunks/<trunk_sid>/credentials
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/credentials" \
  -H "Content-Type: application/json"
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response.status | String | `success` or `failure` |
| response.code | Integer | Response code |
| response.data.username | String | SIP authentication username (same as trunk_sid) |
| response.data.password | String | SIP authentication password |

### Example Response

```json
{
  "request_id": "a7b8c9d0-e1f2-3456-0123-789012345678",
  "method": "GET",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": {
      "username": "trind1a2b3c4d5e6f7890abcdef",
      "password": "Xy9#mK2$pL5nQ8"
    }
  }
}
```

---

## Get Phone Numbers

Retrieves all phone numbers mapped to a trunk.

### HTTP Request

```
GET /v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers
```

### Example Request

```bash
curl -X GET "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/phone-numbers" \
  -H "Content-Type: application/json"
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response.status | String | `success` or `failure` |
| response.code | Integer | Response code |
| response.data | Array | Array of phone number objects |
| response.data[].id | String | Unique identifier for the mapping |
| response.data[].phone_number | String | Mapped phone number |
| response.data[].trunk_sid | String | Associated trunk identifier |
| response.data[].date_created | String | Timestamp of creation |

### Example Response

```json
{
  "request_id": "b8c9d0e1-f2a3-4567-1234-890123456789",
  "method": "GET",
  "http_code": 200,
  "response": {
    "status": "success",
    "code": 200,
    "data": [
      {
        "id": "pn_abc123def456",
        "phone_number": "+919876543210",
        "trunk_sid": "trind1a2b3c4d5e6f7890abcdef",
        "date_created": "2025-01-22T10:35:00Z"
      }
    ]
  }
}
```

---

## Set Trunk Alias

Configures an external caller ID alias for the trunk. This allows you to display a specific phone number as the caller ID for outbound calls.

### HTTP Request

```
POST /v2/accounts/<your_sid>/trunks/<trunk_sid>/settings
```

### Request Headers

| Header | Value |
|--------|-------|
| Content-Type | application/json |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| settings | Array | Yes | Array of setting objects |
| settings[].name | String | Yes | Setting name. Use `trunk_external_alias` |
| settings[].value | String | Yes | Phone number in E.164 format |

### Example Request

```bash
curl -X POST "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks/<trunk_sid>/settings" \
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

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response | Array | Array of response objects |
| response[].status | String | `success` or `failure` |
| response[].code | Integer | Response code |
| response[].data.name | String | Setting name |
| response[].data.value | String | Setting value |
| response[].data.trunk_sid | String | Associated trunk identifier |
| response[].data.date_created | String | Timestamp of creation |

### Example Response

```json
{
  "request_id": "c9d0e1f2-a3b4-5678-2345-901234567890",
  "method": "POST",
  "http_code": 200,
  "response": [
    {
      "status": "success",
      "code": 200,
      "data": {
        "name": "trunk_external_alias",
        "value": "+919876543210",
        "trunk_sid": "trind1a2b3c4d5e6f7890abcdef",
        "date_created": "2025-01-22T10:50:00Z"
      }
    }
  ]
}
```

---

## Delete Trunk

Permanently deletes a trunk and all its associated configurations including phone number mappings, whitelisted IPs, and destination URIs. This action cannot be undone.

### HTTP Request

```
DELETE /v2/accounts/<your_sid>/trunks?trunk_sid=<trunk_sid>
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| trunk_sid | String | Yes | Unique identifier of the trunk to delete |

### Example Request

```bash
curl -X DELETE "https://<your_api_key>:<your_api_token>@api.in.exotel.com/v2/accounts/<your_sid>/trunks?trunk_sid=trind1a2b3c4d5e6f7890abcdef" \
  -H "Content-Type: application/json"
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| request_id | String | Unique identifier for the API request |
| method | String | HTTP method used |
| http_code | Integer | HTTP status code |
| response.status | String | `success` or `failure` |
| response.code | Integer | Response code |
| response.data | null | No data returned on successful deletion |

### Example Response

```json
{
  "request_id": "d0e1f2a3-b4c5-6789-3456-012345678901",
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

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request completed successfully |
| 400 | Bad Request | Invalid request parameters or malformed request body |
| 401 | Unauthorized | Invalid or missing API credentials |
| 403 | Forbidden | Access denied to the requested resource |
| 404 | Not Found | Requested resource does not exist |
| 409 | Conflict | Resource already exists (duplicate) |
| 422 | Unprocessable Entity | Request validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error, contact support |

---

# Error Codes

| Error Code | HTTP Status | Message | Description |
|------------|-------------|---------|-------------|
| 1000 | 400 | Invalid request | Missing or invalid required field in request |
| 1001 | 400 | Invalid parameter | Parameter value is not valid |
| 1002 | 409 | Resource exists | Trunk or phone number already exists |
| 1003 | 404 | Resource not found | Specified trunk_sid does not exist |
| 1010 | 401 | Authorization failed | Invalid API key or token |
| 1011 | 403 | Access denied | No permission to access this resource |
| 1020 | 422 | Validation error | Request validation failed |
| 1030 | 429 | Rate limit exceeded | Too many requests, retry later |

### Error Response Format

```json
{
  "request_id": "error-request-id-12345",
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

# SIP Response Codes

## Success Codes

| Code | Message | Description |
|------|---------|-------------|
| 100 | Trying | Request received, processing |
| 180 | Ringing | Called party is being alerted |
| 183 | Session Progress | Call progress information (early media) |
| 200 | OK | Request successful, call connected |

## Client Error Codes (4xx)

| Code | Message | Cause | Resolution |
|------|---------|-------|------------|
| 400 | Bad Request | Malformed SIP message | Check SIP headers and message format |
| 401 | Unauthorized | Invalid SIP credentials | Verify username and password from Get Credentials API |
| 403 | Forbidden | IP not whitelisted | Add your IP using Whitelist IP API |
| 404 | Not Found | Invalid destination number | Verify phone number format (E.164) |
| 408 | Request Timeout | Network timeout | Check network connectivity and firewall |
| 480 | Temporarily Unavailable | Destination offline or busy | Retry later |
| 486 | Busy Here | Called party is busy | User is on another call |
| 487 | Request Terminated | Call cancelled | Caller hung up before answer |
| 488 | Not Acceptable | Codec mismatch | Check supported codecs configuration |

## Server Error Codes (5xx)

| Code | Message | Cause | Resolution |
|------|---------|-------|------------|
| 500 | Server Internal Error | Exotel server issue | Contact support |
| 502 | Bad Gateway | Upstream server error | Check destination server status |
| 503 | Service Unavailable | Server overloaded or maintenance | Retry with exponential backoff |
| 504 | Gateway Timeout | Destination not responding | Verify destination server is running |

---

# Troubleshooting

| Issue | Likely Cause | Resolution |
|-------|--------------|------------|
| 401 on SIP registration | Wrong credentials | Fetch credentials using Get Credentials API |
| 403 on outbound calls | IP not whitelisted | Add IP using Whitelist IP API |
| 404 on outbound calls | Invalid phone number | Use E.164 format with country code |
| No inbound calls received | Missing destination URI | Add destination using Add Destination URI API |
| One-way audio | Firewall blocking RTP | Open UDP ports 10000-20000 |
| TLS handshake failed | Certificate issue | Verify certificate validity and chain |
| Registration timeout | Network or firewall issue | Check ports 5060/5061 connectivity |

---

# Postman Collection

Import `postman/Exotel_Voice_Trunking_APIs.json` into Postman.

**Setup:**
1. Go to Authorization tab and select Basic Auth
2. Enter API Key as Username and API Token as Password
3. Replace `<subdomain>`, `<your_sid>`, `<trunk_sid>` in the URL
4. Fill request body parameters
5. Click Send

---

# Support

- Documentation: https://developer.exotel.com
- Email: support@exotel.com

---

# Important Note

FQDN/DNS routing is supported only for Inbound / Origination (PSTN to SIP).
Outbound / Termination (SIP to PSTN) requires static IP whitelisting.
