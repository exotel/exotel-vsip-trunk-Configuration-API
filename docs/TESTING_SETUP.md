# Local Testing Setup Guide

This guide provides step-by-step instructions for setting up and running the complete Exotel vSIP API testing framework locally.

## 📋 Prerequisites

### 1. Exotel Account Requirements

Before testing, ensure you have:

- **Active Exotel Account** with vSIP features enabled
- **API Credentials** (Auth Key and Auth Token)
- **Account SID** and **Subscribix Domain**
- **NSO Code** (obtain from Exotel support)
- **Valid DID Numbers** for testing
- **Network Access** to destination IPs

### 2. System Requirements

#### Operating System
- **Linux** (Ubuntu 20.04+ recommended)
- **macOS** (10.15+ recommended)  
- **Windows** (with WSL2 for bash scripts)

#### Required Software
```bash
# Check versions
curl --version        # >= 7.68.0
python3 --version     # >= 3.8
php --version         # >= 7.4
go version           # >= 1.18
java --version       # >= 11
javac --version      # >= 11
git --version        # >= 2.25
```

## 🚀 Installation Steps

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd "vSIP- Trunk Configuration API"
```

### Step 2: Environment Setup

#### Create Environment File
```bash
# Copy template
cp .env.example .env

# Edit with your credentials
vim .env  # or use your preferred editor
```

#### Configure Environment Variables
```bash
# .env file content
EXO_AUTH_KEY=your_exotel_api_key_here
EXO_AUTH_TOKEN=your_exotel_auth_token_here
EXO_SUBSCRIBIX_DOMAIN=your_domain.exotel.com
EXO_ACCOUNT_SID=your_account_sid_here

# Trunk configuration
TRUNK_NAME=test_trunk_001
NSO_CODE=YOUR-NSO-CODE

# Test data
DID_NUMBER=+1234567890
WHITELIST_IP=192.168.1.100
WHITELIST_MASK=32
TRUNK_DEST_IP=192.168.1.200
TRUNK_DEST_PORT=5060

# Optional
EXOPHONE=+1234567890
```

#### Export Environment Variables
```bash
# Make variables available to all scripts
set -a
source .env
set +a
```

### Step 3: Install Language Dependencies

#### Python Dependencies
```bash
# Install Python testing dependencies
cd tests/
pip3 install -r requirements.txt
cd ..
```

#### PHP Dependencies (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y php php-cli php-curl php-json
```

#### Go Dependencies
```bash
# Go modules are handled automatically
# No additional installation needed
```

#### Java Dependencies (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk openjdk-11-jre
```

### Step 4: Verify Installation
```bash
# Test environment setup
./tests/test_runner.sh curl

# Check if all tools are working
python3 tests/test_all_apis.py --help
```

## 🧪 Testing Framework Components

### 1. Individual Language Tests
```bash
# Test specific language implementation
./tests/test_runner.sh python
./tests/test_runner.sh php
./tests/test_runner.sh go
./tests/test_runner.sh java
./tests/test_runner.sh curl
```

### 2. Comprehensive API Testing
```bash
# Test all APIs with detailed logging
python3 tests/test_all_apis.py --verbose

# Test specific API endpoint
python3 tests/test_all_apis.py --test create
python3 tests/test_all_apis.py --test map
python3 tests/test_all_apis.py --test whitelist
```

### 3. Integration Testing
```bash
# Full workflow test
python3 tests/integration_test.py --verbose

# Integration test without cleanup (for debugging)
python3 tests/integration_test.py --no-cleanup --verbose
```

### 4. Load Testing
```bash
# Test with mock server (safe for development)
python3 tests/mock_server.py --port 8080 &  # Start mock server
python3 tests/load_test.py --mock --concurrent 10 --requests 50

# Test against real API (use with caution)
python3 tests/load_test.py --concurrent 5 --requests 20
```

### 5. Mock Server Testing
```bash
# Start mock server for development
python3 tests/mock_server.py --port 8080 --verbose

# Test against mock server (in another terminal)
export EXO_SUBSCRIBIX_DOMAIN=localhost:8080
export EXO_AUTH_KEY=test_key
export EXO_AUTH_TOKEN=test_token
export EXO_ACCOUNT_SID=test_account

python3 tests/test_all_apis.py --verbose
```

## 📊 Understanding Test Results

### Log Files Location
```
logs/
├── api_test_YYYYMMDD_HHMMSS.log           # Python test logs
├── test_runner_YYYYMMDD_HHMMSS.log        # Shell test runner logs
├── integration_test_YYYYMMDD_HHMMSS.log   # Integration test logs
└── test_results/
    ├── test_report_YYYYMMDD_HHMMSS.json   # JSON results
    ├── test_report_YYYYMMDD_HHMMSS.html   # HTML report
    └── [language]_[test]_YYYYMMDD_HHMMSS.log
```

### Reading Test Results

#### JSON Results Format
```json
{
  "total_tests": 7,
  "successful_tests": 6,
  "failed_tests": 1,
  "success_rate": 85.7,
  "test_results": [
    {
      "test_name": "create_trunk",
      "success": true,
      "result": {
        "status_code": 201,
        "response": {"sid": "TR12345", ...}
      }
    }
  ]
}
```

#### HTML Reports
Open `logs/test_results/test_report_*.html` in a browser for visual results.

## 🔧 Troubleshooting

### Common Setup Issues

#### 1. Environment Variables Not Set
```bash
# Error: Missing required environment variables
# Solution: Verify .env file and export variables
echo $EXO_AUTH_KEY  # Should not be empty
source .env
set -a && source .env && set +a
```

#### 2. Python Dependencies Missing
```bash
# Error: ModuleNotFoundError: No module named 'aiohttp'
# Solution: Install dependencies
pip3 install -r tests/requirements.txt

# If pip3 not found
sudo apt-get install python3-pip
```

#### 3. Permission Denied on Scripts
```bash
# Error: Permission denied: ./tests/test_runner.sh
# Solution: Make scripts executable
chmod +x tests/*.sh tests/*.py
chmod +x curl/*.sh python/*.py php/*.php
```

#### 4. Java Compilation Errors
```bash
# Error: javac: command not found
# Solution: Install Java Development Kit
sudo apt-get install openjdk-11-jdk

# Set JAVA_HOME if needed
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

#### 5. Go Module Issues
```bash
# Error: go: cannot find main module
# Solution: Initialize Go module in the directory
cd go/
go mod init exotel-vsip-test
cd ..
```

### Network Issues

#### Test Connectivity
```bash
# Test domain resolution
nslookup $EXO_SUBSCRIBIX_DOMAIN

# Test HTTPS connectivity
curl -I "https://$EXO_SUBSCRIBIX_DOMAIN" --max-time 10

# Test with verbose output
curl -v "https://$EXO_SUBSCRIBIX_DOMAIN"
```

#### Proxy Configuration
```bash
# If behind corporate proxy
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1
```

### API Credential Issues

#### Verify Credentials
```bash
# Test minimal API call
curl -u "$EXO_AUTH_KEY:$EXO_AUTH_TOKEN" \
  "https://$EXO_SUBSCRIBIX_DOMAIN/v2/accounts/$EXO_ACCOUNT_SID" \
  -H "Accept: application/json"
```

#### Debug Authentication
```bash
# Enable debug mode for detailed output
python3 tests/test_all_apis.py --verbose --test create
```

## 📝 Development Workflow

### 1. Before Making Changes
```bash
# Run baseline tests
./tests/test_runner.sh all > baseline_results.log 2>&1
```

### 2. During Development
```bash
# Test specific changes
python3 tests/test_all_apis.py --test create --verbose

# Use mock server for rapid iteration
python3 tests/mock_server.py --port 8080 &
# Modify EXO_SUBSCRIBIX_DOMAIN=localhost:8080 for testing
```

### 3. Before Committing
```bash
# Run full test suite
./tests/test_runner.sh all

# Run integration test
python3 tests/integration_test.py

# Check for any new error patterns
python3 -c "
import glob, json
for f in glob.glob('logs/test_results/*.json'):
    with open(f) as file:
        data = json.load(file)
        if data.get('success_rate', 100) < 90:
            print(f'Warning: Low success rate in {f}')
"
```

## 🎯 Next Steps

### Production Deployment
1. Set up CI/CD pipeline using `.github/workflows/api-tests.yml`
2. Configure monitoring and alerting
3. Set up regular health checks
4. Implement proper secret management

### Advanced Testing
1. Performance benchmarking
2. Security testing
3. Chaos engineering
4. Multi-region testing

### Monitoring Setup
1. Set up log aggregation
2. Configure metrics collection
3. Create dashboards
4. Set up alerting rules

For additional help, refer to:
- `docs/DEBUGGING.md` - Detailed debugging guide
- `docs/ERROR_REPORTS.md` - Common errors and solutions
- `README.md` - General usage information 