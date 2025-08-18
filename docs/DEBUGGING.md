# Exotel vSIP API Debugging Guide

This guide provides comprehensive debugging information, error handling, and troubleshooting steps for the Exotel vSIP PSTN Connectivity APIs.

## 📋 Table of Contents

- [Testing Requirements](#testing-requirements)
- [Common Errors](#common-errors)
- [Debugging Tools](#debugging-tools)
- [Error Codes Reference](#error-codes-reference)
- [Troubleshooting Steps](#troubleshooting-steps)
- [Logging and Monitoring](#logging-and-monitoring)
- [Environment Setup](#environment-setup)

## 🧪 Testing Requirements

### Prerequisites for Local Testing

To test these APIs locally, you will need:

#### 1. Exotel Account & Credentials
```bash
# Required environment variables
EXO_AUTH_KEY=your_exotel_api_key
EXO_AUTH_TOKEN=your_exotel_auth_token
EXO_SUBSCRIBIX_DOMAIN=your_subscribix_domain  # e.g., api.exotel.com
EXO_ACCOUNT_SID=your_account_sid
```

#### 2. Test Data
```bash
# Trunk configuration
TRUNK_NAME=test_trunk_001
NSO_CODE=YOUR-NSO-CODE  # Obtain from Exotel support

# DID numbers (must be valid and available)
DID_NUMBER=+1234567890  # Valid DID for testing

# Network configuration
WHITELIST_IP=192.168.1.100    # Your server IP
WHITELIST_MASK=32             # IP mask
TRUNK_DEST_IP=192.168.1.200   # Destination SIP server IP
TRUNK_DEST_PORT=5060          # SIP port

# Optional settings
EXOPHONE=+1234567890          # External phone number
```

#### 3. Network Requirements
- Outbound HTTPS access to Exotel APIs
- Valid SSL certificates for HTTPS requests
- Network connectivity to destination IPs (for SIP traffic)

#### 4. Development Environment
```bash
# Required tools
curl --version      # For cURL tests
python3 --version   # For Python tests
php --version       # For PHP tests
go version          # For Go tests
java --version      # For Java tests
javac --version     # For Java compilation
```

## ❌ Common Errors

### 1. Authentication Errors

#### HTTP 401 - Unauthorized
```json
{
  "error": "Authentication failed",
  "message": "Invalid API key or token"
}
```

**Causes:**
- Invalid `EXO_AUTH_KEY` or `EXO_AUTH_TOKEN`
- Expired credentials
- Incorrect domain in `EXO_SUBSCRIBIX_DOMAIN`

**Solutions:**
- Verify credentials in Exotel dashboard
- Check for typos in environment variables
- Ensure credentials have proper permissions

#### HTTP 403 - Forbidden
```json
{
  "error": "Access denied",
  "message": "Insufficient permissions for this operation"
}
```

**Causes:**
- Account doesn't have vSIP features enabled
- API key lacks required permissions
- Account suspended or limited

### 2. Validation Errors

#### HTTP 400 - Bad Request
```json
{
  "error": "Validation failed",
  "details": {
    "trunk_name": ["This field is required"],
    "nso_code": ["Invalid NSO code format"]
  }
}
```

**Common validation issues:**
- Missing required fields
- Invalid phone number format
- Invalid IP address format
- Invalid NSO code

#### HTTP 422 - Unprocessable Entity
```json
{
  "error": "Resource conflict",
  "message": "Trunk name already exists"
}
```

### 3. Network Errors

#### Connection Timeout
```
Error: Network timeout after 30 seconds
```

**Causes:**
- Network connectivity issues
- Firewall blocking HTTPS traffic
- DNS resolution problems

#### SSL Certificate Errors
```
Error: SSL certificate verification failed
```

**Solutions:**
- Update CA certificates
- Check system clock accuracy
- Verify network proxy settings

### 4. Resource Errors

#### HTTP 404 - Not Found
```json
{
  "error": "Resource not found",
  "message": "Trunk with SID 'TR123' not found"
}
```

#### HTTP 429 - Rate Limited
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Retry after 60 seconds"
}
```

## 🔧 Debugging Tools

### 1. Test Runner
```bash
# Run comprehensive test suite
./tests/test_runner.sh

# Test specific language
./tests/test_runner.sh python

# Test with verbose logging
./tests/test_all_apis.py --verbose
```

### 2. Manual API Testing
```bash
# Test with cURL directly
curl -X POST "https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_SUBSCRIBIX_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}/trunks" \
  -H "Content-Type: application/json" \
  -d '{"trunk_name":"debug_test","nso_code":"ANY-ANY","domain_name":"test.pstn.exotel.com"}' \
  -v  # Verbose output for debugging
```

### 3. Log Analysis
```bash
# View latest test logs
tail -f logs/api_test_*.log

# Search for errors
grep -i error logs/*.log

# Analyze specific test results
cat logs/test_results/test_report_*.json | jq '.results'
```

## 📊 Error Codes Reference

| Code | Status | Description | Action Required |
|------|--------|-------------|-----------------|
| 200 | OK | Request successful | None |
| 201 | Created | Resource created | None |
| 400 | Bad Request | Invalid request format | Fix request payload |
| 401 | Unauthorized | Authentication failed | Check credentials |
| 403 | Forbidden | Access denied | Check permissions |
| 404 | Not Found | Resource not found | Verify resource ID |
| 409 | Conflict | Resource already exists | Use different name |
| 422 | Unprocessable Entity | Validation failed | Fix data format |
| 429 | Too Many Requests | Rate limit exceeded | Implement retry logic |
| 500 | Internal Server Error | Server error | Contact Exotel support |
| 502 | Bad Gateway | Service unavailable | Retry later |
| 503 | Service Unavailable | Maintenance mode | Check status page |

## 🔍 Troubleshooting Steps

### Step 1: Environment Verification
```bash
# Check environment variables
echo "Auth Key: ${EXO_AUTH_KEY:0:8}..."
echo "Domain: $EXO_SUBSCRIBIX_DOMAIN"
echo "Account: $EXO_ACCOUNT_SID"

# Test basic connectivity
curl -I "https://$EXO_SUBSCRIBIX_DOMAIN" --max-time 10
```

### Step 2: Credential Testing
```bash
# Test authentication with minimal request
curl -X GET "https://${EXO_AUTH_KEY}:${EXO_AUTH_TOKEN}@${EXO_SUBSCRIBIX_DOMAIN}/v2/accounts/${EXO_ACCOUNT_SID}" \
  -H "Accept: application/json" \
  --fail --show-error
```

### Step 3: Data Validation
```bash
# Validate phone number format
python3 -c "
import re
phone = '$DID_NUMBER'
if re.match(r'^\+[1-9]\d{1,14}$', phone):
    print('✅ Valid phone format')
else:
    print('❌ Invalid phone format')
"

# Validate IP address
python3 -c "
import ipaddress
try:
    ipaddress.IPv4Address('$WHITELIST_IP')
    print('✅ Valid IP address')
except:
    print('❌ Invalid IP address')
"
```

### Step 4: API Endpoint Testing
```bash
# Test each endpoint individually
./tests/test_all_apis.py --test create --verbose
./tests/test_all_apis.py --test map --verbose
./tests/test_all_apis.py --test whitelist --verbose
```

### Step 5: Network Debugging
```bash
# Check DNS resolution
nslookup $EXO_SUBSCRIBIX_DOMAIN

# Test HTTPS connectivity
openssl s_client -connect $EXO_SUBSCRIBIX_DOMAIN:443 -servername $EXO_SUBSCRIBIX_DOMAIN

# Check for proxy issues
echo "HTTP_PROXY: $HTTP_PROXY"
echo "HTTPS_PROXY: $HTTPS_PROXY"
```

## 📝 Logging and Monitoring

### Log Levels
- **DEBUG**: Detailed request/response data
- **INFO**: General operation status
- **WARNING**: Non-critical issues
- **ERROR**: Failed operations
- **CRITICAL**: System failures

### Log Locations
```
logs/
├── api_test_YYYYMMDD_HHMMSS.log      # Python test logs
├── test_runner_YYYYMMDD_HHMMSS.log   # Shell test logs
└── test_results/
    ├── test_report_YYYYMMDD_HHMMSS.json   # JSON results
    ├── test_report_YYYYMMDD_HHMMSS.html   # HTML report
    └── [language]_[test]_YYYYMMDD_HHMMSS.log  # Individual test logs
```

### Monitoring Commands
```bash
# Real-time log monitoring
tail -f logs/api_test_*.log

# Error analysis
grep -B2 -A2 "ERROR\|FAILED" logs/*.log

# Success rate calculation
grep -c "SUCCESS\|PASSED" logs/*.log
```

## ⚙️ Environment Setup

### Development Environment
```bash
# Create .env from template
cp .env.example .env

# Edit with your credentials
vim .env

# Export environment variables
set -a
source .env
set +a

# Verify setup
./tests/test_runner.sh curl
```

### CI/CD Environment
```bash
# Set environment variables in CI
export EXO_AUTH_KEY="your_key"
export EXO_AUTH_TOKEN="your_token"
export EXO_SUBSCRIBIX_DOMAIN="api.exotel.com"
export EXO_ACCOUNT_SID="your_sid"

# Run tests
./tests/test_runner.sh
```

### Docker Environment
```bash
# Run tests in Docker
docker run --rm \
  -e EXO_AUTH_KEY="$EXO_AUTH_KEY" \
  -e EXO_AUTH_TOKEN="$EXO_AUTH_TOKEN" \
  -e EXO_SUBSCRIBIX_DOMAIN="$EXO_SUBSCRIBIX_DOMAIN" \
  -e EXO_ACCOUNT_SID="$EXO_ACCOUNT_SID" \
  -v $(pwd):/app \
  -w /app \
  ubuntu:20.04 \
  ./tests/test_runner.sh
```

## 🆘 Getting Help

### Exotel Support
- **Documentation**: [developer.exotel.com](https://developer.exotel.com/)
- **Support Email**: support@exotel.com
- **Status Page**: [status.exotel.com](https://status.exotel.com/)

### Community Resources
- GitHub Issues for this repository
- Stack Overflow: `exotel` tag
- API Documentation: Check latest version for updates

### Debugging Checklist

Before contacting support, ensure you have:

- [ ] Valid Exotel credentials
- [ ] Correct environment variable configuration
- [ ] Network connectivity to Exotel APIs
- [ ] Valid test data (phone numbers, IP addresses)
- [ ] Recent log files from failed tests
- [ ] Clear description of the issue
- [ ] Steps to reproduce the problem

### Emergency Contacts

For production issues:
1. Check [status.exotel.com](https://status.exotel.com/) for service status
2. Contact Exotel support with:
   - Account SID
   - Timestamp of the issue
   - Error messages and codes
   - Log files (with sensitive data redacted) 