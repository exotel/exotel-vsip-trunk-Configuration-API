# 🚨 Exotel vSIP Trunk API - Complete Error Reference Guide

## 📋 Table of Contents

- [Overview](#overview)
- [Error Response Format](#error-response-format)
- [Authentication Errors](#authentication-errors)
- [Validation Errors](#validation-errors)
- [Resource Errors](#resource-errors)
- [Authorization Errors](#authorization-errors)
- [Network Errors](#network-errors)
- [Complete Error Code Reference](#complete-error-code-reference)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Best Practices](#best-practices)

## 🔍 Overview

This document provides a comprehensive reference for all possible errors when working with Exotel vSIP Trunk APIs. All error scenarios have been tested and documented with their exact cause codes, HTTP status codes, and resolution steps.

## 📊 Error Response Format

All Exotel API errors follow this consistent format:

```json
{
  "request_id": "unique_request_identifier",
  "method": "POST",
  "http_code": 400,
  "response": {
    "code": 400,
    "error_data": {
      "code": 1002,
      "message": "Invalid parameter",
      "description": "Maximum allowed length for TrunkName is 16"
    },
    "status": "failure",
    "data": null
  }
}
```

### Response Fields:
- **request_id**: Unique identifier for tracking the request
- **method**: HTTP method used (POST, GET, etc.)
- **http_code**: Standard HTTP response code
- **response.code**: API-specific response code
- **error_data.code**: Exotel-specific error code
- **error_data.message**: Error category
- **error_data.description**: Detailed error description

---

## 🔐 Authentication Errors

### Error Code: **1010** - Authorization Failed
- **HTTP Status**: 401 Unauthorized
- **Message**: "Authorization failed"
- **Description**: "Authorization failed"

#### **Causes:**
1. Invalid `EXO_AUTH_KEY`
2. Invalid `EXO_AUTH_TOKEN`
3. Expired credentials
4. Malformed Authorization header

#### **Example Response:**
```json
{
  "request_id": "c6084ac2e9a44812824b42577f01937b",
  "method": "POST",
  "http_code": 401,
  "response": {
    "code": 401,
    "error_data": {
      "code": 1010,
      "message": "Authorization failed",
      "description": "Authorization failed"
    },
    "status": "failure",
    "data": null
  }
}
```

#### **Resolution:**
1. Verify credentials in Exotel dashboard
2. Check environment variable names:
   ```bash
   echo $EXO_AUTH_KEY
   echo $EXO_AUTH_TOKEN
   ```
3. Ensure no trailing spaces in credentials
4. Test with minimal cURL request:
   ```bash
   curl -u "$EXO_AUTH_KEY:$EXO_AUTH_TOKEN" \
     "https://$EXO_SUBSCRIBIX_DOMAIN/v2/accounts/$EXO_ACCOUNT_SID"
   ```

---

## ❌ Missing Parameter Errors

### Error Code: **1001** - Mandatory Parameter Missing
- **HTTP Status**: 400 Bad Request
- **Message**: "Mandatory Parameter missing"
- **Description**: Varies by missing field

#### **Common Missing Fields:**

**1001.1 - Missing Trunk Name**
```json
{
  "code": 1001,
  "message": "Mandatory Parameter missing",
  "description": "TrunkName is mandatory"
}
```

**1001.2 - Missing IP Address**
```json
{
  "code": 1001,
  "message": "Mandatory Parameter missing", 
  "description": "Ip is mandatory"
}
```

**1001.3 - Missing Phone Number**
```json
{
  "code": 1001,
  "message": "Mandatory Parameter missing",
  "description": "PhoneNumber is mandatory"
}
```

#### **Resolution:**
Always include all required fields:
- **Trunk Creation**: `trunk_name`, `nso_code`, `domain_name`
- **DID Mapping**: `phone_number`
- **IP Whitelisting**: `ip`, `mask`
- **Destination URIs**: `destinations`
- **Trunk Settings**: `settings`

---

## ✅ Validation Errors

### Error Code: **1002** - Invalid Parameter

This error code covers multiple validation scenarios with different descriptions.

#### **1002.1 - Trunk Name Length Validation**
- **HTTP Status**: 400 Bad Request
- **Message**: "Invalid parameter"
- **Description**: "Maximum allowed length for TrunkName is 16"

**Cause**: Trunk name exceeds 16 characters
**Example**: `very_long_trunk_name_that_exceeds_limit` (42 characters)

**Resolution**: Use trunk names ≤ 16 characters
```bash
export TRUNK_NAME="short_name"  # ✅ Valid (10 chars)
export TRUNK_NAME="test_$(date +%H%M%S)"  # ✅ Valid (11 chars)
```

#### **1002.2 - Trunk Name Character Validation**
- **HTTP Status**: 400 Bad Request
- **Message**: "Invalid parameter"
- **Description**: "Allowed characters for TrunkName is alphanumeric and _"

**Cause**: Trunk name contains invalid characters
**Invalid Characters**: `@ # $ % & * ( ) - + = [ ] { } | \ : ; " ' < > , . ? / ~`

**Examples:**
- ❌ `trunk@#$%`
- ❌ `trunk-name`
- ❌ `trunk.name`
- ✅ `trunk_name`
- ✅ `trunk123`
- ✅ `TrunkName_01`

#### **1002.3 - Phone Number Validation**
- **HTTP Status**: 400 Bad Request
- **Message**: "Invalid parameter"
- **Description**: "Invalid PhoneNumber"

**Causes:**
1. Non-E.164 format
2. Invalid characters
3. Missing country code

**Examples:**
- ❌ `080-486-36999` (contains dashes)
- ❌ `invalid-phone` (contains letters)
- ❌ `123456` (too short)
- ✅ `+918048636999` (proper E.164)
- ✅ `+14155552671` (US number)

**Resolution**: Use proper E.164 format
```bash
# India numbers
export DID_NUMBER="+91XXXXXXXXXX"
# US numbers  
export DID_NUMBER="+1XXXXXXXXXX"
```

#### **1002.4 - IP Address Validation**
- **HTTP Status**: 400 Bad Request
- **Message**: "Invalid parameter"
- **Description**: "Invalid ip"

**Causes:**
1. Invalid IP format
2. Non-numeric values
3. Values > 255
4. Empty IP address

**Examples:**
- ❌ `invalid.ip.address`
- ❌ `999.999.999.999`
- ❌ `192.168.1` (incomplete)
- ❌ `` (empty)
- ✅ `192.168.1.1`
- ✅ `140.238.241.32`

#### **1002.5 - Subnet Mask Validation**
- **HTTP Status**: 400 Bad Request
- **Message**: "Invalid parameter"
- **Description**: "mask should be in-between 16 and 32"

**Causes:**
1. Mask value < 16
2. Mask value > 32
3. Negative mask values

**Examples:**
- ❌ `0` (too small)
- ❌ `15` (too small)
- ❌ `99` (too large)
- ❌ `-1` (negative)
- ✅ `16` (minimum)
- ✅ `32` (maximum, single IP)
- ✅ `24` (common subnet)

#### **1002.6 - Domain Name Validation**
- **HTTP Status**: 400 Bad Request
- **Message**: "Invalid parameter"
- **Description**: "Domain name should end with .pstn.exotel.com"

**Examples:**
- ❌ `test.com`
- ❌ `mydomain.org`
- ❌ `server.pstn.exotel.net`
- ✅ `account123.pstn.exotel.com`
- ✅ `{EXO_ACCOUNT_SID}.pstn.exotel.com`

#### **1002.7 - NSO Code Validation**
- **HTTP Status**: 400 Bad Request
- **Message**: "Invalid parameter"
- **Description**: "Nso code is invalid"

**Examples:**
- ❌ `INVALID-CODE`
- ❌ `WRONG_FORMAT`
- ✅ `ANY-ANY` (most common)
- ✅ Valid NSO codes from Exotel documentation

---

## 🚫 Resource Errors

### Error Code: **1000** - Not Found
- **HTTP Status**: 404 Not Found
- **Message**: "Not Found"
- **Description**: "Not Found"

#### **Causes:**
1. Extremely long phone numbers (>30 digits)
2. Empty phone numbers in some contexts
3. Malformed resource identifiers

#### **Example:**
```json
{
  "request_id": "1ed10affef19427dad8bea3d38259e5f",
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

### Error Code: **1008** - Duplicate Resource
- **HTTP Status**: 200 OK (with failure status)
- **Message**: "Duplicate resource"
- **Description**: Varies by resource type

#### **Variations:**

**1008.1 - Duplicate Trunk Name**
```json
{
  "code": 409,
  "error_data": {
    "code": 1008,
    "message": "Duplicate resource",
    "description": "Unable to create trunk with name py_121523"
  },
  "status": "failure"
}
```

**1008.2 - Duplicate DID Mapping**
```json
{
  "code": 409,
  "error_data": {
    "code": 1008,
    "message": "Duplicate resource",
    "description": "Unable to create DidTrunkMapping with TrunkSid trmum1XXXXXXXXXXXXXXX"
  },
  "status": "failure"
}
```

**1008.3 - Duplicate IP Whitelist**
```json
{
  "code": 409,
  "error_data": {
    "code": 1008,
    "message": "Duplicate resource",
    "description": "Unable to Whitelist-ip with ip 192.168.1.1"
  },
  "status": "failure"
}
```

#### **Resolution for Duplicates:**
1. **Trunk Names**: Use unique names with timestamps
   ```bash
   export TRUNK_NAME="trunk_$(date +%Y%m%d_%H%M%S)"
   ```
2. **DID Mapping**: Check if DID is already mapped
3. **IP Whitelist**: Verify IP isn't already whitelisted

---

## 🔒 Authorization Errors

### Error Code: **1003** - Authorization Failed (Invalid Trunk SID)
- **HTTP Status**: 403 Forbidden
- **Message**: "Authorization failed"
- **Description**: "Authorization failed"

#### **Causes:**
1. Invalid trunk SID format
2. Non-existent trunk SID
3. Trunk SID from different account
4. Unauthorized access to trunk resource

#### **Examples:**
- ❌ `invalid_trunk_sid`
- ❌ `trmum1nonexistent123456789`
- ✅ `trmum1XXXXXXXXXXXXXXX`

#### **Security Note:**
This error is returned for both invalid and non-existent trunk SIDs to prevent SID enumeration attacks.

#### **Resolution:**
1. Verify trunk SID from trunk creation response
2. List existing trunks to get valid SIDs
3. Ensure you're using the correct account context

---

## 📝 Request Format Errors

### Error Code: **1007** - Invalid Request Body
- **HTTP Status**: 400 Bad Request
- **Message**: "Invalid request body, failed parsing"
- **Description**: Varies by JSON issue

#### **Common Issues:**

**1007.1 - Malformed JSON**
```json
{
  "code": 1007,
  "message": "Invalid request body,failed parsing ",
  "description": "unexpected EOF"
}
```
**Cause**: Missing closing braces, invalid JSON syntax
**Example**: `{"trunk_name":"test"` (missing `}`)

**1007.2 - Type Mismatch**
```json
{
  "code": 1007,
  "message": "Invalid request body,failed parsing ",
  "description": "json: cannot unmarshal number -1 into Go struct field CreateWhitelistipsRequest.mask of type uint8"
}
```
**Cause**: Wrong data types (e.g., negative numbers where unsigned expected)

#### **Resolution:**
1. Validate JSON syntax before sending
2. Use correct data types for each field
3. Test with JSON validators

### Error Code: **1011** - Unsupported Content Type
- **HTTP Status**: 415 Unsupported Media Type
- **Message**: "unsupported content type"
- **Description**: Content type specified

#### **Example:**
```json
{
  "request_id": "dbd5126aece84ae4896fcaf036dd76d3",
  "method": "POST",
  "http_code": 415,
  "response": {
    "code": 415,
    "error_data": {
      "code": 1011,
      "message": "unsupported content type",
      "description": "text/plain"
    },
    "status": "failure",
    "data": null
  }
}
```

#### **Resolution:**
Always use `Content-Type: application/json` for API requests:
```bash
curl -H "Content-Type: application/json" ...
```

---

## 🌐 Network Errors

### SSL Certificate Errors
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

#### **Resolution for Python:**
```python
import ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

#### **Resolution for System:**
```bash
# macOS
brew install ca-certificates

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ca-certificates
```

---

## 📚 Complete Error Code Reference

| Code | HTTP Status | Message | Description | Category |
|------|-------------|---------|-------------|----------|
| **1000** | 404 | Not Found | Not Found | Resource |
| **1001** | 400 | Mandatory Parameter missing | Required fields missing | Validation |
| **1002** | 400 | Invalid parameter | Length/Character/Format validation | Validation |
| **1003** | 403 | Authorization failed | Invalid trunk SID access | Authorization |
| **1007** | 400 | Invalid request body | JSON parsing/type errors | Request |
| **1008** | 200/409 | Duplicate resource | Resource already exists | Resource |
| **1010** | 401 | Authorization failed | Invalid credentials | Authentication |
| **1011** | 415 | Unsupported content type | Wrong Content-Type header | Request |

## 🔧 Troubleshooting Guide

### **Step 1: Identify Error Category**
```bash
# Check the error_data.code to determine category:
# 1000-1099: Resource errors
# 1000s: Not found, duplicates
# 1003: Authorization (trunk access)
# 1010: Authentication (credentials)
```

### **Step 2: Common Validation Checklist**

#### **Trunk Names:**
- [ ] Length ≤ 16 characters
- [ ] Only alphanumeric + underscore
- [ ] Unique across account
- [ ] Not empty (though allowed)

#### **Phone Numbers:**
- [ ] E.164 format (+CountryCodeNumber)
- [ ] No special characters except +
- [ ] Reasonable length (10-15 digits)
- [ ] Valid country code

#### **IP Addresses:**
- [ ] IPv4 format (x.x.x.x)
- [ ] Each octet 0-255
- [ ] No special characters
- [ ] Not empty

#### **Trunk SIDs:**
- [ ] Format: trmum1[alphanumeric]
- [ ] Obtained from successful trunk creation
- [ ] Belongs to current account
- [ ] Still exists and active

### **Step 3: Debugging Commands**

#### **Test Authentication:**
```bash
curl -u "$EXO_AUTH_KEY:$EXO_AUTH_TOKEN" \
  "https://$EXO_SUBSCRIBIX_DOMAIN/v2/accounts/$EXO_ACCOUNT_SID" \
  -H "Accept: application/json"
```

#### **Validate Environment:**
```bash
echo "Domain: $EXO_SUBSCRIBIX_DOMAIN"
echo "Account: $EXO_ACCOUNT_SID"
echo "Auth Key: ${EXO_AUTH_KEY:0:8}..."
echo "Trunk: $TRUNK_NAME ($(echo $TRUNK_NAME | wc -c) chars)"
```

#### **Test Minimal Trunk Creation:**
```bash
curl -X POST "https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_SUBSCRIBIX_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}/trunks" \
  -H "Content-Type: application/json" \
  -d '{"trunk_name":"test123","nso_code":"ANY-ANY","domain_name":"'${EXO_ACCOUNT_SID}'.pstn.exotel.com"}'
```

---

## ✨ Best Practices

### **1. Error Handling in Code**
```python
def handle_exotel_error(response_data):
    error_code = response_data.get('response', {}).get('error_data', {}).get('code')
    
    if error_code == 1010:
        return "Authentication failed - check credentials"
    elif error_code == 1002:
        return f"Validation error: {response_data['response']['error_data']['description']}"
    elif error_code == 1008:
        return "Resource already exists - use different name"
    elif error_code == 1003:
        return "Invalid trunk SID or access denied"
    elif error_code == 1000:
        return "Resource not found"
    else:
        return f"Unknown error: {error_code}"
```

### **2. Retry Logic for Specific Errors**
```python
def should_retry(error_code):
    # Don't retry validation errors or duplicates
    no_retry_codes = [1002, 1008, 1010, 1003]
    return error_code not in no_retry_codes

def api_request_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except ExotelAPIError as e:
            if not should_retry(e.error_code) or attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### **3. Validation Before API Calls**
```python
import re

def validate_trunk_name(name):
    if len(name) > 16:
        raise ValueError("Trunk name must be ≤ 16 characters")
    if not re.match(r'^[a-zA-Z0-9_]*$', name):
        raise ValueError("Trunk name can only contain alphanumeric and underscore")
    return True

def validate_phone_number(number):
    if not re.match(r'^\+[1-9]\d{1,14}$', number):
        raise ValueError("Phone number must be in E.164 format")
    return True

def validate_ip_address(ip):
    try:
        import ipaddress
        ipaddress.IPv4Address(ip)
        return True
    except:
        raise ValueError("Invalid IPv4 address format")
```

### **4. Unique Resource Naming**
```bash
# Generate unique trunk names
export TRUNK_NAME="trunk_$(date +%Y%m%d_%H%M%S)"
export TRUNK_NAME="trunk_${USER}_$(date +%s)"
export TRUNK_NAME="trunk_$(uuidgen | cut -c1-8)"
```

### **5. Logging and Monitoring**
```python
import logging

def log_api_call(endpoint, payload, response, duration):
    log_data = {
        "endpoint": endpoint,
        "success": response.get("success", False),
        "error_code": response.get("error_code"),
        "duration_ms": duration * 1000,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if log_data["success"]:
        logging.info(f"API_SUCCESS: {json.dumps(log_data)}")
    else:
        logging.error(f"API_ERROR: {json.dumps(log_data)}")
```

---

## 🆘 Support and Resources

### **When to Contact Exotel Support:**
- Error codes not documented here
- Persistent authentication issues after verification
- Unexpected behavior with valid inputs
- Account-specific configuration questions

### **Information to Provide:**
- Request ID from error response
- Full error response JSON
- Timestamp of the error
- Account SID (can be partially redacted)
- Steps to reproduce

### **Useful Resources:**
- [Exotel Developer Documentation](https://developer.exotel.com/)
- [API Status Page](https://status.exotel.com/)
- This Error Reference Guide

---

**📝 Last Updated:** August 18, 2025  
**📊 Total Error Scenarios Tested:** 35+  
**🔍 Error Codes Documented:** 8 main codes with 15+ variations  
**✅ All APIs Tested:** Trunk Creation, DID Mapping, IP Whitelisting, Destination URIs, Trunk Settings  
**🧪 Comprehensive Testing:** Success cases, validation errors, missing fields, malformed requests, authentication, authorization, duplicates, edge cases 