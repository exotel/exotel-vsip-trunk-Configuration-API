# Exotel vSIP API Error Reports & Analysis

This document provides detailed error analysis, common failure patterns, and resolution strategies for Exotel vSIP API integration.

## 📊 Error Categories

### 1. Authentication & Authorization Errors

#### Error Code: 401 - Unauthorized
```json
{
  "error": "Authentication failed",
  "message": "Invalid API credentials",
  "code": "AUTH_FAILED",
  "timestamp": "2025-01-13T10:30:00Z"
}
```

**Common Causes:**
- Incorrect `EXO_AUTH_KEY` or `EXO_AUTH_TOKEN`
- Expired API credentials
- Wrong `EXO_SUBSCRIBIX_DOMAIN`
- Malformed Authorization header

**Resolution Steps:**
1. Verify credentials in Exotel dashboard
2. Check environment variable spelling
3. Ensure no trailing spaces in credentials
4. Test with minimal cURL request

**Example Fix:**
```bash
# Test credentials
curl -u "$EXO_AUTH_KEY:$EXO_AUTH_TOKEN" \
  "https://$EXO_SUBSCRIBIX_DOMAIN/v2/accounts/$EXO_ACCOUNT_SID" \
  -H "Accept: application/json"
```

#### Error Code: 403 - Forbidden
```json
{
  "error": "Access denied",
  "message": "Account does not have vSIP feature enabled",
  "code": "FEATURE_NOT_ENABLED",
  "timestamp": "2025-01-13T10:30:00Z"
}
```

**Resolution:**
- Contact Exotel support to enable vSIP features
- Verify account subscription includes trunk management
- Check API key permissions scope

### 2. Validation Errors

#### Error Code: 400 - Bad Request
```json
{
  "error": "Validation failed",
  "details": {
    "trunk_name": ["Name already exists", "Must be 3-50 characters"],
    "nso_code": ["Invalid format. Expected: ABC-XYZ"]
  },
  "code": "VALIDATION_ERROR"
}
```

**Common Field Errors:**

| Field | Error | Valid Format | Example |
|-------|-------|--------------|---------|
| `trunk_name` | Name too short/long | 3-50 characters | `my_trunk_001` |
| `trunk_name` | Special characters | Alphanumeric + underscore | `production_trunk` |
| `nso_code` | Invalid format | XXX-XXX pattern | `IND-MUM` |
| `phone_number` | Invalid format | E.164 format | `+919876543210` |
| `ip` | Invalid IP | IPv4 format | `192.168.1.100` |
| `mask` | Invalid range | 0-32 | `24` |

#### Error Code: 422 - Unprocessable Entity
```json
{
  "error": "Resource conflict",
  "message": "Trunk name 'production_trunk' already exists",
  "code": "DUPLICATE_RESOURCE",
  "existing_resource_id": "TR12345678"
}
```

**Resolution Strategies:**
- Use unique trunk names with timestamps
- Check existing resources before creation
- Implement retry logic with name variations

### 3. Network & Connectivity Errors

#### Connection Timeout
```
Error: urllib.error.URLError: <urlopen error timed out>
Request timeout after 30 seconds
```

**Diagnostic Steps:**
```bash
# Test network connectivity
ping $EXO_SUBSCRIBIX_DOMAIN

# Test DNS resolution
nslookup $EXO_SUBSCRIBIX_DOMAIN

# Test HTTPS connectivity
curl -I "https://$EXO_SUBSCRIBIX_DOMAIN" --max-time 10

# Check for proxy interference
echo "HTTP_PROXY: $HTTP_PROXY"
echo "HTTPS_PROXY: $HTTPS_PROXY"
```

#### SSL Certificate Issues
```
Error: certificate verify failed: unable to get local issuer certificate
```

**Resolution:**
```bash
# Update CA certificates (Ubuntu/Debian)
sudo apt-get update && sudo apt-get install ca-certificates

# Update CA certificates (macOS)
brew install ca-certificates

# For development only - disable SSL verification (NOT RECOMMENDED for production)
export PYTHONHTTPSVERIFY=0
```

### 4. Rate Limiting Errors

#### Error Code: 429 - Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 100 requests per minute exceeded",
  "retry_after": 60,
  "limit": 100,
  "remaining": 0,
  "reset_time": "2025-01-13T10:31:00Z"
}
```

**Rate Limiting Implementation:**
```python
import time
import random

def api_request_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = int(e.headers.get('Retry-After', 60))
                jitter = random.uniform(0.1, 0.5)  # Add jitter
                sleep_time = retry_after + jitter
                
                print(f"Rate limited. Waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                continue
            raise
    raise Exception(f"Failed after {max_retries} attempts")
```

### 5. Resource Errors

#### Error Code: 404 - Resource Not Found
```json
{
  "error": "Resource not found",
  "message": "Trunk with SID 'TR12345' not found",
  "code": "RESOURCE_NOT_FOUND",
  "resource_type": "trunk",
  "resource_id": "TR12345"
}
```

**Common Causes:**
- Using wrong `TRUNK_SID` in environment
- Trunk was deleted or expired
- Incorrect account context

**Debugging Script:**
```bash
# List all trunks to verify SID
curl -u "$EXO_AUTH_KEY:$EXO_AUTH_TOKEN" \
  "https://$EXO_SUBSCRIBIX_DOMAIN/v2/accounts/$EXO_ACCOUNT_SID/trunks" \
  -H "Accept: application/json" | jq '.trunks[].sid'
```

## 🔍 Error Analysis Patterns

### Pattern 1: Intermittent 500 Errors
```
HTTP 500: Internal Server Error
Frequency: 2-5% of requests
Time Pattern: Random, no specific pattern
```

**Analysis:**
- Likely server-side transient issues
- Implement exponential backoff retry
- Log request details for pattern analysis

**Mitigation:**
```python
def exponential_backoff_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
```

### Pattern 2: Peak Hour Failures
```
Time Pattern: 9 AM - 6 PM IST
Error Types: 429 (Rate Limiting), 503 (Service Unavailable)
Success Rate: Drops to 85% during peak hours
```

**Recommendations:**
- Schedule non-critical operations during off-peak hours
- Implement queue-based processing
- Use distributed rate limiting

### Pattern 3: Regional Connectivity Issues
```
Error Pattern: Timeouts from specific regions
Affected: Asia-Pacific region (occasional)
Duration: 5-15 minutes
```

**Monitoring Setup:**
```bash
# Multi-region connectivity test
for region in us-east eu-west asia-pacific; do
  echo "Testing from $region..."
  curl -w "@curl-format.txt" -o /dev/null -s \
    "https://$EXO_SUBSCRIBIX_DOMAIN/v2/health"
done
```

## 📈 Error Monitoring & Alerting

### Log Analysis Queries

#### Find High Error Rate Periods
```bash
# Extract error rates by hour
grep -E "HTTP [4-5][0-9][0-9]" logs/api_test_*.log | \
  cut -d' ' -f1,2 | cut -d: -f1,2 | \
  sort | uniq -c | sort -nr
```

#### Identify Most Common Errors
```bash
# Top error messages
grep "ERROR" logs/*.log | \
  grep -o '"message":"[^"]*"' | \
  sort | uniq -c | sort -nr | head -10
```

#### Track API Response Times
```bash
# Extract response times over threshold
grep "response_time" logs/test_results/*.json | \
  jq -r 'select(.response_time > 2.0) | "\(.timestamp) \(.endpoint) \(.response_time)s"'
```

### Automated Error Detection

#### Error Rate Alert Script
```bash
#!/bin/bash
# alert_on_errors.sh

LOG_FILE="logs/api_test_$(date +%Y%m%d)*.log"
ERROR_THRESHOLD=5  # Alert if >5% error rate

total_requests=$(grep -c "Testing" $LOG_FILE)
failed_requests=$(grep -c "❌" $LOG_FILE)

if [ $total_requests -gt 0 ]; then
    error_rate=$((failed_requests * 100 / total_requests))
    
    if [ $error_rate -gt $ERROR_THRESHOLD ]; then
        echo "🚨 ALERT: Error rate is ${error_rate}% (threshold: ${ERROR_THRESHOLD}%)"
        echo "Total requests: $total_requests"
        echo "Failed requests: $failed_requests"
        
        # Send notification (integrate with your alerting system)
        # curl -X POST "https://hooks.slack.com/..." -d "..."
    fi
fi
```

## 🛠️ Debugging Tools & Scripts

### Quick Error Diagnosis
```bash
#!/bin/bash
# diagnose_api_errors.sh

echo "🔍 Exotel API Error Diagnosis"
echo "=============================="

# Check environment
echo "📋 Environment Check:"
env | grep EXO_ | sed 's/=.*/=***/'

# Test basic connectivity
echo -e "\n🌐 Connectivity Test:"
if curl -s --max-time 5 "https://$EXO_SUBSCRIBIX_DOMAIN" > /dev/null; then
    echo "✅ Domain reachable"
else
    echo "❌ Domain unreachable"
fi

# Test authentication
echo -e "\n🔐 Authentication Test:"
response=$(curl -s -w "%{http_code}" -u "$EXO_AUTH_KEY:$EXO_AUTH_TOKEN" \
  "https://$EXO_SUBSCRIBIX_DOMAIN/v2/accounts/$EXO_ACCOUNT_SID" \
  -H "Accept: application/json")

http_code="${response: -3}"
if [ "$http_code" = "200" ]; then
    echo "✅ Authentication successful"
else
    echo "❌ Authentication failed (HTTP $http_code)"
fi

# Recent error summary
echo -e "\n📊 Recent Error Summary:"
if [ -f "logs/api_test_*.log" ]; then
    echo "Last 5 errors:"
    grep "❌" logs/api_test_*.log | tail -5
else
    echo "No recent logs found"
fi
```

### Error Pattern Analysis
```python
#!/usr/bin/env python3
# analyze_error_patterns.py

import json
import glob
import datetime
from collections import defaultdict, Counter

def analyze_error_patterns():
    error_patterns = defaultdict(list)
    hourly_errors = defaultdict(int)
    
    # Process all test result files
    for file_path in glob.glob("logs/test_results/*.json"):
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        for result in data.get('test_results', []):
            if not result.get('success', True):
                # Extract hour from timestamp
                timestamp = result.get('timestamp', '')
                if timestamp:
                    hour = timestamp[:13]  # YYYY-MM-DDTHH
                    hourly_errors[hour] += 1
                
                # Categorize error
                error_type = result.get('result', {}).get('status_code', 'Unknown')
                error_patterns[error_type].append(result)
    
    # Generate report
    print("🔍 Error Pattern Analysis")
    print("=" * 50)
    
    print(f"\n📊 Error Distribution:")
    for error_code, occurrences in Counter(error_patterns.keys()).most_common():
        print(f"  HTTP {error_code}: {len(error_patterns[error_code])} occurrences")
    
    print(f"\n⏰ Hourly Error Distribution:")
    for hour in sorted(hourly_errors.keys())[-24:]:  # Last 24 hours
        print(f"  {hour}: {hourly_errors[hour]} errors")
    
    # Most problematic endpoints
    endpoint_errors = defaultdict(int)
    for errors in error_patterns.values():
        for error in errors:
            endpoint = error.get('endpoint', 'Unknown')
            endpoint_errors[endpoint] += 1
    
    print(f"\n🎯 Most Problematic Endpoints:")
    for endpoint, count in Counter(endpoint_errors).most_common(5):
        print(f"  {endpoint}: {count} errors")

if __name__ == "__main__":
    analyze_error_patterns()
```

## 📝 Error Reporting Template

### Bug Report Template
```markdown
## 🐛 API Error Report

### Environment
- **Timestamp**: 2025-01-13T10:30:00Z
- **Account SID**: AC... (redacted)
- **API Endpoint**: POST /v2/accounts/.../trunks
- **Request ID**: req_12345 (if available)

### Error Details
- **HTTP Status**: 400
- **Error Code**: VALIDATION_ERROR
- **Error Message**: Invalid trunk name format

### Request Payload
```json
{
  "trunk_name": "test-trunk!",
  "nso_code": "IND-MUM",
  "domain_name": "account.pstn.exotel.com"
}
```

### Response Body
```json
{
  "error": "Validation failed",
  "details": {
    "trunk_name": ["Special characters not allowed"]
  }
}
```

### Debugging Steps Taken
1. ✅ Verified authentication credentials
2. ✅ Checked network connectivity
3. ✅ Validated payload format
4. ❌ Issue persists with valid trunk name

### Resolution
- Updated trunk_name to use underscores instead of hyphens
- Request succeeded after modification

### Prevention
- Add client-side validation for trunk names
- Update documentation with character restrictions
```

## 🎯 Best Practices for Error Handling

### 1. Implement Comprehensive Logging
```python
import logging
import json

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_requests.log'),
        logging.StreamHandler()
    ]
)

def log_api_request(endpoint, payload, response, duration):
    log_data = {
        "endpoint": endpoint,
        "payload_hash": hash(json.dumps(payload, sort_keys=True)),
        "status_code": response.get("status_code"),
        "duration_ms": duration * 1000,
        "success": response.get("success", False)
    }
    
    if not log_data["success"]:
        log_data["error_details"] = response.get("error")
    
    logging.info(f"API_REQUEST: {json.dumps(log_data)}")
```

### 2. Graceful Error Recovery
```python
class ExotelAPIClient:
    def __init__(self):
        self.max_retries = 3
        self.base_delay = 1.0
    
    def create_trunk_with_retry(self, payload):
        for attempt in range(self.max_retries):
            try:
                return self._create_trunk(payload)
            except ValidationError as e:
                # Don't retry validation errors
                raise
            except (NetworkError, ServerError) as e:
                if attempt == self.max_retries - 1:
                    raise
                
                delay = self.base_delay * (2 ** attempt)
                time.sleep(delay)
        
        raise Exception("All retry attempts failed")
```

### 3. Proactive Monitoring
```bash
# Set up continuous monitoring
*/5 * * * * /path/to/diagnose_api_errors.sh >> /var/log/exotel_monitor.log 2>&1

# Daily error summary
0 9 * * * /path/to/analyze_error_patterns.py | mail -s "Daily API Error Report" admin@company.com
```

This comprehensive error reporting framework provides the tools and processes needed to quickly identify, diagnose, and resolve API integration issues. 