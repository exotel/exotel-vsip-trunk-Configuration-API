#!/usr/bin/env python3

import os
import sys
import json
import urllib.request
import urllib.error
import logging
import datetime
from typing import Dict, Any, Optional, Tuple

# Add parent directory to path to import _client
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

class ExotelAPITester:
    def __init__(self, log_level=logging.INFO):
        self.setup_logging(log_level)
        self.test_results = []
        self.base_url = self._get_base_url()
        
    def setup_logging(self, level):
        """Setup comprehensive logging"""
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f'api_test_{timestamp}.log')
        
        # Configure logging
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Starting API tests - Log file: {log_file}")
    
    def _get_base_url(self) -> Optional[str]:
        """Build base URL from environment variables"""
        required_vars = ['EXO_AUTH_KEY', 'EXO_AUTH_TOKEN', 'EXO_SUBSCRIBIX_DOMAIN', 'EXO_ACCOUNT_SID']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            self.logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            return None
            
        return f"https://{os.getenv('EXO_AUTH_KEY')}:{os.getenv('EXO_AUTH_TOKEN')}@{os.getenv('EXO_SUBSCRIBIX_DOMAIN')}/v2/accounts/{os.getenv('EXO_ACCOUNT_SID')}"
    
    def make_request(self, endpoint: str, payload: Dict[str, Any], test_name: str) -> Tuple[bool, Dict[str, Any]]:
        """Make API request with comprehensive error handling"""
        if not self.base_url:
            return False, {"error": "Missing credentials", "details": "Required environment variables not set"}
        
        # Build URL without credentials embedded
        domain = os.getenv('EXO_SUBSCRIBIX_DOMAIN')
        account_sid = os.getenv('EXO_ACCOUNT_SID')
        url = f"https://{domain}/v2/accounts/{account_sid}{endpoint}"
        
        self.logger.info(f"Testing {test_name}: {endpoint}")
        self.logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            data = json.dumps(payload).encode('utf-8')
            
            # Create request with separate authentication
            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            # Add Basic Authentication
            import base64
            auth_key = os.getenv('EXO_AUTH_KEY')
            auth_token = os.getenv('EXO_AUTH_TOKEN')
            credentials = f"{auth_key}:{auth_token}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            req.add_header('Authorization', f'Basic {encoded_credentials}')
            
            # Handle SSL context for macOS
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
                response_data = response.read().decode('utf-8')
                self.logger.info(f"✅ {test_name} - Status: {response.status}")
                self.logger.debug(f"Response: {response_data}")
                
                return True, {
                    "status_code": response.status,
                    "response": json.loads(response_data) if response_data else {},
                    "headers": dict(response.headers)
                }
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else "No error details"
            self.logger.error(f"❌ {test_name} - HTTP {e.code}: {e.reason}")
            self.logger.error(f"Error details: {error_body}")
            
            return False, {
                "status_code": e.code,
                "error": e.reason,
                "details": error_body,
                "headers": dict(e.headers) if e.headers else {}
            }
            
        except urllib.error.URLError as e:
            self.logger.error(f"❌ {test_name} - Network error: {e.reason}")
            return False, {"error": "Network error", "details": str(e.reason)}
            
        except Exception as e:
            self.logger.error(f"❌ {test_name} - Unexpected error: {str(e)}")
            return False, {"error": "Unexpected error", "details": str(e)}
    
    def test_create_trunk(self) -> Dict[str, Any]:
        """Test trunk creation"""
        payload = {
            "trunk_name": os.getenv("TRUNK_NAME", "test_trunk_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")),
            "nso_code": os.getenv("NSO_CODE", "ANY-ANY"),
            "domain_name": f"{os.getenv('EXO_ACCOUNT_SID')}.pstn.exotel.com"
        }
        
        success, result = self.make_request("/trunks", payload, "Create Trunk")
        
        test_result = {
            "test_name": "create_trunk",
            "endpoint": "/trunks",
            "method": "POST",
            "payload": payload,
            "success": success,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def test_map_did(self, trunk_sid: str = None) -> Dict[str, Any]:
        """Test DID mapping to trunk"""
        if not trunk_sid:
            trunk_sid = os.getenv("TRUNK_SID", "TR_test_dummy")
            
        payload = {
            "phone_number": os.getenv("DID_NUMBER", "+1234567890")
        }
        
        endpoint = f"/trunks/{trunk_sid}/phone-numbers"
        success, result = self.make_request(endpoint, payload, "Map DID")
        
        test_result = {
            "test_name": "map_did",
            "endpoint": endpoint,
            "method": "POST",
            "payload": payload,
            "success": success,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def test_whitelist_ip(self, trunk_sid: str = None) -> Dict[str, Any]:
        """Test IP whitelisting"""
        if not trunk_sid:
            trunk_sid = os.getenv("TRUNK_SID", "TR_test_dummy")
            
        payload = {
            "ip": os.getenv("WHITELIST_IP", "192.168.1.100"),
            "mask": int(os.getenv("WHITELIST_MASK", "32"))
        }
        
        endpoint = f"/trunks/{trunk_sid}/whitelisted-ips"
        success, result = self.make_request(endpoint, payload, "Whitelist IP")
        
        test_result = {
            "test_name": "whitelist_ip",
            "endpoint": endpoint,
            "method": "POST",
            "payload": payload,
            "success": success,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def test_add_destination(self, transport: str, trunk_sid: str = None) -> Dict[str, Any]:
        """Test adding destination URI"""
        if not trunk_sid:
            trunk_sid = os.getenv("TRUNK_SID", "TR_test_dummy")
            
        dest_ip = os.getenv("TRUNK_DEST_IP", "192.168.1.200")
        dest_port = os.getenv("TRUNK_DEST_PORT", "5060")
        
        if transport.lower() == "udp":
            destination = f"{dest_ip}:{dest_port}"
        else:
            destination = f"{dest_ip}:{dest_port};transport={transport.lower()}"
            
        payload = {
            "destinations": [{"destination": destination}]
        }
        
        endpoint = f"/trunks/{trunk_sid}/destination-uris"
        success, result = self.make_request(endpoint, payload, f"Add {transport.upper()} Destination")
        
        test_result = {
            "test_name": f"add_destination_{transport.lower()}",
            "endpoint": endpoint,
            "method": "POST",
            "payload": payload,
            "success": success,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def test_set_trunk_alias(self, trunk_sid: str = None) -> Dict[str, Any]:
        """Test setting trunk alias"""
        if not trunk_sid:
            trunk_sid = os.getenv("TRUNK_SID", "TR_test_dummy")
            
        exophone = os.getenv("EXOPHONE")
        if not exophone:
            self.logger.warning("EXOPHONE not set, skipping trunk alias test")
            return {
                "test_name": "set_trunk_alias",
                "skipped": True,
                "reason": "EXOPHONE not configured",
                "timestamp": datetime.datetime.now().isoformat()
            }
            
        payload = {
            "settings": [{"name": "trunk_external_alias", "value": exophone}]
        }
        
        endpoint = f"/trunks/{trunk_sid}/settings"
        success, result = self.make_request(endpoint, payload, "Set Trunk Alias")
        
        test_result = {
            "test_name": "set_trunk_alias",
            "endpoint": endpoint,
            "method": "POST",
            "payload": payload,
            "success": success,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        self.logger.info("🚀 Starting comprehensive API test suite")
        
        # Test 1: Create trunk (this gives us a trunk_sid for other tests)
        trunk_result = self.test_create_trunk()
        
        # Extract trunk_sid from response if successful
        trunk_sid = None
        if trunk_result["success"] and "response" in trunk_result["result"]:
            trunk_response = trunk_result["result"]["response"]
            trunk_sid = trunk_response.get("sid") or trunk_response.get("trunk_sid")
        
        if not trunk_sid:
            trunk_sid = os.getenv("TRUNK_SID")
            self.logger.warning(f"Using fallback TRUNK_SID: {trunk_sid}")
        
        # Test 2: Map DID
        self.test_map_did(trunk_sid)
        
        # Test 3: Whitelist IP
        self.test_whitelist_ip(trunk_sid)
        
        # Test 4: Add destinations (UDP, TCP, TLS)
        for transport in ["UDP", "TCP", "TLS"]:
            self.test_add_destination(transport, trunk_sid)
        
        # Test 5: Set trunk alias
        self.test_set_trunk_alias(trunk_sid)
        
        # Generate summary
        total_tests = len(self.test_results)
        successful_tests = sum(1 for test in self.test_results if test.get("success", False))
        skipped_tests = sum(1 for test in self.test_results if test.get("skipped", False))
        
        summary = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests - skipped_tests,
            "skipped_tests": skipped_tests,
            "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
            "test_results": self.test_results,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.logger.info(f"📊 Test Summary: {successful_tests}/{total_tests} passed ({summary['success_rate']:.1f}%)")
        
        # Save detailed results
        results_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 
                                  f"test_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(results_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.logger.info(f"📁 Detailed results saved to: {results_file}")
        return summary

def main():
    """Main test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Exotel vSIP APIs")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--test", "-t", choices=["create", "map", "whitelist", "destination", "alias", "all"], 
                       default="all", help="Run specific test")
    
    args = parser.parse_args()
    
    log_level = logging.DEBUG if args.verbose else logging.INFO
    tester = ExotelAPITester(log_level)
    
    if args.test == "all":
        summary = tester.run_all_tests()
        print(f"\n🎯 Final Results: {summary['successful_tests']}/{summary['total_tests']} tests passed")
    else:
        # Run individual tests
        if args.test == "create":
            tester.test_create_trunk()
        elif args.test == "map":
            tester.test_map_did()
        elif args.test == "whitelist":
            tester.test_whitelist_ip()
        elif args.test == "destination":
            for transport in ["UDP", "TCP", "TLS"]:
                tester.test_add_destination(transport)
        elif args.test == "alias":
            tester.test_set_trunk_alias()

if __name__ == "__main__":
    main() 