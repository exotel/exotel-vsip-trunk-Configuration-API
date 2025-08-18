#!/bin/bash

# Exotel vSIP API Test Runner
# Tests all language implementations with comprehensive error reporting

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_ROOT/logs"
RESULTS_DIR="$LOG_DIR/test_results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create directories
mkdir -p "$LOG_DIR" "$RESULTS_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_DIR/test_runner_$TIMESTAMP.log"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_DIR/test_runner_$TIMESTAMP.log"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_DIR/test_runner_$TIMESTAMP.log"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_DIR/test_runner_$TIMESTAMP.log"
}

# Test result tracking
declare -A test_results
total_tests=0
passed_tests=0
failed_tests=0

# Function to test environment setup
check_environment() {
    log_info "Checking environment setup..."
    
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        log_warning ".env file not found. Using .env.example as reference."
        if [ -f "$PROJECT_ROOT/.env.example" ]; then
            log_info "You can copy .env.example to .env and update with your credentials"
            log_info "cp $PROJECT_ROOT/.env.example $PROJECT_ROOT/.env"
        fi
        return 1
    fi
    
    source "$PROJECT_ROOT/.env"
    
    local required_vars=("EXO_AUTH_KEY" "EXO_AUTH_TOKEN" "EXO_SUBSCRIBIX_DOMAIN" "EXO_ACCOUNT_SID")
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        log_error "Missing required environment variables: ${missing_vars[*]}"
        return 1
    fi
    
    log_success "Environment setup complete"
    return 0
}

# Function to run a single test with error capture
run_test() {
    local test_name="$1"
    local command="$2"
    local language="$3"
    
    total_tests=$((total_tests + 1))
    local test_log="$RESULTS_DIR/${language}_${test_name}_$TIMESTAMP.log"
    
    log_info "Running $language test: $test_name"
    
    if timeout 30 bash -c "$command" > "$test_log" 2>&1; then
        log_success "$language - $test_name: PASSED"
        test_results["${language}_${test_name}"]="PASSED"
        passed_tests=$((passed_tests + 1))
        return 0
    else
        local exit_code=$?
        log_error "$language - $test_name: FAILED (exit code: $exit_code)"
        test_results["${language}_${test_name}"]="FAILED"
        failed_tests=$((failed_tests + 1))
        
        # Show last few lines of error log
        log_error "Last 5 lines of error log:"
        tail -n 5 "$test_log" | while IFS= read -r line; do
            log_error "  $line"
        done
        
        return $exit_code
    fi
}

# Function to test cURL implementations
test_curl() {
    log_info "Testing cURL implementations..."
    
    local curl_dir="$PROJECT_ROOT/curl"
    
    # Test each script
    run_test "create_trunk" "cd '$curl_dir' && ./create_trunk.sh" "curl"
    
    # If trunk creation was successful, run other tests
    if [ "${test_results[curl_create_trunk]}" = "PASSED" ]; then
        run_test "map_did" "cd '$curl_dir' && ./map_did.sh" "curl"
        run_test "whitelist_ip" "cd '$curl_dir' && ./whitelist_ip.sh" "curl"
        run_test "add_destination_udp" "cd '$curl_dir' && ./add_destination_udp.sh" "curl"
        run_test "add_destination_tcp" "cd '$curl_dir' && ./add_destination_tcp.sh" "curl"
        run_test "add_destination_tls" "cd '$curl_dir' && ./add_destination_tls.sh" "curl"
        run_test "set_trunk_alias" "cd '$curl_dir' && ./set_trunk_alias.sh" "curl"
    else
        log_warning "Skipping other cURL tests due to trunk creation failure"
    fi
}

# Function to test Python implementations
test_python() {
    log_info "Testing Python implementations..."
    
    local python_dir="$PROJECT_ROOT/python"
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        log_error "python3 not found. Skipping Python tests."
        return 1
    fi
    
    # Test each script
    run_test "create_trunk" "cd '$python_dir' && python3 create_trunk.py" "python"
    
    if [ "${test_results[python_create_trunk]}" = "PASSED" ]; then
        run_test "map_did" "cd '$python_dir' && python3 map_did.py" "python"
        run_test "whitelist_ip" "cd '$python_dir' && python3 whitelist_ip.py" "python"
        run_test "add_destination_udp" "cd '$python_dir' && python3 add_destination_udp.py" "python"
        run_test "add_destination_tcp" "cd '$python_dir' && python3 add_destination_tcp.py" "python"
        run_test "add_destination_tls" "cd '$python_dir' && python3 add_destination_tls.py" "python"
        run_test "set_trunk_alias" "cd '$python_dir' && python3 set_trunk_alias.py" "python"
    else
        log_warning "Skipping other Python tests due to trunk creation failure"
    fi
}

# Function to test PHP implementations
test_php() {
    log_info "Testing PHP implementations..."
    
    local php_dir="$PROJECT_ROOT/php"
    
    # Check if PHP is available
    if ! command -v php &> /dev/null; then
        log_error "php not found. Skipping PHP tests."
        return 1
    fi
    
    # Test each script
    run_test "create_trunk" "cd '$php_dir' && php create_trunk.php" "php"
    
    if [ "${test_results[php_create_trunk]}" = "PASSED" ]; then
        run_test "map_did" "cd '$php_dir' && php map_did.php" "php"
        run_test "whitelist_ip" "cd '$php_dir' && php whitelist_ip.php" "php"
        run_test "add_destination_udp" "cd '$php_dir' && php add_destination_udp.php" "php"
        run_test "add_destination_tcp" "cd '$php_dir' && php add_destination_tcp.php" "php"
        run_test "add_destination_tls" "cd '$php_dir' && php add_destination_tls.php" "php"
        run_test "set_trunk_alias" "cd '$php_dir' && php set_trunk_alias.php" "php"
    else
        log_warning "Skipping other PHP tests due to trunk creation failure"
    fi
}

# Function to test Go implementations
test_go() {
    log_info "Testing Go implementations..."
    
    local go_dir="$PROJECT_ROOT/go"
    
    # Check if Go is available
    if ! command -v go &> /dev/null; then
        log_error "go not found. Skipping Go tests."
        return 1
    fi
    
    # Test each script
    run_test "create_trunk" "cd '$go_dir' && go run _client.go create_trunk.go" "go"
    
    if [ "${test_results[go_create_trunk]}" = "PASSED" ]; then
        run_test "map_did" "cd '$go_dir' && go run _client.go map_did.go" "go"
        run_test "whitelist_ip" "cd '$go_dir' && go run _client.go whitelist_ip.go" "go"
        run_test "add_destination_udp" "cd '$go_dir' && go run _client.go add_destination_udp.go" "go"
        run_test "add_destination_tcp" "cd '$go_dir' && go run _client.go add_destination_tcp.go" "go"
        run_test "add_destination_tls" "cd '$go_dir' && go run _client.go add_destination_tls.go" "go"
        run_test "set_trunk_alias" "cd '$go_dir' && go run _client.go set_trunk_alias.go" "go"
    else
        log_warning "Skipping other Go tests due to trunk creation failure"
    fi
}

# Function to test Java implementations
test_java() {
    log_info "Testing Java implementations..."
    
    local java_dir="$PROJECT_ROOT/java"
    
    # Check if Java is available
    if ! command -v java &> /dev/null || ! command -v javac &> /dev/null; then
        log_error "java or javac not found. Skipping Java tests."
        return 1
    fi
    
    # Compile Java files
    log_info "Compiling Java files..."
    if ! javac -cp "$java_dir" "$java_dir"/*.java 2> "$RESULTS_DIR/java_compile_$TIMESTAMP.log"; then
        log_error "Java compilation failed. Check $RESULTS_DIR/java_compile_$TIMESTAMP.log"
        return 1
    fi
    
    # Test each class
    run_test "create_trunk" "cd '$java_dir' && java CreateTrunk" "java"
    
    if [ "${test_results[java_create_trunk]}" = "PASSED" ]; then
        run_test "map_did" "cd '$java_dir' && java MapDid" "java"
        run_test "whitelist_ip" "cd '$java_dir' && java WhitelistIp" "java"
        run_test "add_destination_udp" "cd '$java_dir' && java AddDestinationUdp" "java"
        run_test "add_destination_tcp" "cd '$java_dir' && java AddDestinationTcp" "java"
        run_test "add_destination_tls" "cd '$java_dir' && java AddDestinationTls" "java"
        run_test "set_trunk_alias" "cd '$java_dir' && java SetTrunkAlias" "java"
    else
        log_warning "Skipping other Java tests due to trunk creation failure"
    fi
}

# Function to generate test report
generate_report() {
    local report_file="$RESULTS_DIR/test_report_$TIMESTAMP.html"
    local json_report="$RESULTS_DIR/test_report_$TIMESTAMP.json"
    
    log_info "Generating test report..."
    
    # Generate JSON report
    cat > "$json_report" << EOF
{
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "summary": {
        "total_tests": $total_tests,
        "passed_tests": $passed_tests,
        "failed_tests": $failed_tests,
        "success_rate": $(echo "scale=2; $passed_tests * 100 / $total_tests" | bc -l 2>/dev/null || echo "0")
    },
    "results": {
EOF

    local first=true
    for test_name in "${!test_results[@]}"; do
        if [ "$first" = true ]; then
            first=false
        else
            echo "," >> "$json_report"
        fi
        echo "        \"$test_name\": \"${test_results[$test_name]}\"" >> "$json_report"
    done

    cat >> "$json_report" << EOF
    }
}
EOF

    # Generate HTML report
    cat > "$report_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Exotel vSIP API Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
        .summary { margin: 20px 0; }
        .passed { color: green; }
        .failed { color: red; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Exotel vSIP API Test Report</h1>
        <p>Generated: $(date)</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Tests: $total_tests</p>
        <p class="passed">Passed: $passed_tests</p>
        <p class="failed">Failed: $failed_tests</p>
        <p>Success Rate: $(echo "scale=1; $passed_tests * 100 / $total_tests" | bc -l 2>/dev/null || echo "0")%</p>
    </div>
    
    <h2>Test Results</h2>
    <table>
        <tr>
            <th>Test</th>
            <th>Language</th>
            <th>API</th>
            <th>Status</th>
        </tr>
EOF

    for test_name in "${!test_results[@]}"; do
        local language=$(echo "$test_name" | cut -d'_' -f1)
        local api=$(echo "$test_name" | cut -d'_' -f2-)
        local status="${test_results[$test_name]}"
        local status_class=$([ "$status" = "PASSED" ] && echo "passed" || echo "failed")
        
        cat >> "$report_file" << EOF
        <tr>
            <td>$test_name</td>
            <td>$language</td>
            <td>$api</td>
            <td class="$status_class">$status</td>
        </tr>
EOF
    done

    cat >> "$report_file" << EOF
    </table>
</body>
</html>
EOF

    log_success "Test report generated: $report_file"
    log_success "JSON report generated: $json_report"
}

# Main execution
main() {
    log_info "🚀 Starting Exotel vSIP API Test Suite"
    log_info "Timestamp: $TIMESTAMP"
    log_info "Log directory: $LOG_DIR"
    log_info "Results directory: $RESULTS_DIR"
    
    # Check environment
    if ! check_environment; then
        log_error "Environment check failed. Please fix the issues above."
        exit 1
    fi
    
    # Run tests for each language
    test_curl
    test_python
    test_php
    test_go
    test_java
    
    # Generate reports
    generate_report
    
    # Final summary
    log_info "📊 Test Suite Complete"
    log_success "Passed: $passed_tests/$total_tests tests"
    
    if [ $failed_tests -gt 0 ]; then
        log_error "Failed: $failed_tests tests"
        exit 1
    else
        log_success "All tests passed! 🎉"
        exit 0
    fi
}

# Parse command line arguments
case "${1:-all}" in
    "curl")
        check_environment && test_curl
        ;;
    "python")
        check_environment && test_python
        ;;
    "php")
        check_environment && test_php
        ;;
    "go")
        check_environment && test_go
        ;;
    "java")
        check_environment && test_java
        ;;
    "all"|*)
        main
        ;;
esac 