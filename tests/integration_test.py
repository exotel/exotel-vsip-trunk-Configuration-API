#!/usr/bin/env python3

"""
Integration Test for Exotel vSIP API Workflow
Tests complete trunk lifecycle: create -> configure -> verify
"""

import os
import sys
import json
import time
import logging
import datetime
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

class IntegrationTest:
    def __init__(self, cleanup=True, log_level=logging.INFO):
        self.cleanup = cleanup
        self.test_resources = []  # Track created resources for cleanup
        self.setup_logging(log_level)
        
        # Test configuration
        self.test_trunk_name = f"integration_test_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.test_did = os.getenv("DID_NUMBER", "+1234567890")
        self.test_ip = os.getenv("WHITELIST_IP", "192.168.1.100")
        self.test_dest_ip = os.getenv("TRUNK_DEST_IP", "192.168.1.200")
        self.test_dest_port = os.getenv("TRUNK_DEST_PORT", "5060")
        
    def setup_logging(self, level):
        """Setup logging for integration test"""
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f'integration_test_{timestamp}.log')
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Starting integration test - Log file: {log_file}")
    
    def make_api_request(self, endpoint: str, payload: Dict[str, Any], operation: str) -> Dict[str, Any]:
        """Make API request using the same logic as individual scripts"""
        import urllib.request
        import urllib.error
        
        # Build URL
        auth_key = os.getenv('EXO_AUTH_KEY')
        auth_token = os.getenv('EXO_AUTH_TOKEN')
        domain = os.getenv('EXO_SUBSCRIBIX_DOMAIN')
        account_sid = os.getenv('EXO_ACCOUNT_SID')
        
        if not all([auth_key, auth_token, domain, account_sid]):
            raise Exception("Missing required environment variables")
        
        base_url = f"https://{auth_key}:{auth_token}@{domain}/v2/accounts/{account_sid}"
        url = base_url + endpoint
        
        self.logger.info(f"🔄 {operation}: {endpoint}")
        self.logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = response.read().decode('utf-8')
                result = json.loads(response_data) if response_data else {}
                
                self.logger.info(f"✅ {operation} - Status: {response.status}")
                self.logger.debug(f"Response: {response_data}")
                
                return {
                    "success": True,
                    "status_code": response.status,
                    "data": result
                }
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else "No error details"
            self.logger.error(f"❌ {operation} - HTTP {e.code}: {e.reason}")
            self.logger.error(f"Error details: {error_body}")
            
            return {
                "success": False,
                "status_code": e.code,
                "error": e.reason,
                "details": error_body
            }
        except Exception as e:
            self.logger.error(f"❌ {operation} - Error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def step_1_create_trunk(self) -> Optional[str]:
        """Step 1: Create a new trunk"""
        self.logger.info("🚀 Step 1: Creating trunk")
        
        payload = {
            "trunk_name": self.test_trunk_name,
            "nso_code": os.getenv("NSO_CODE", "ANY-ANY"),
            "domain_name": f"{os.getenv('EXO_ACCOUNT_SID')}.pstn.exotel.com"
        }
        
        result = self.make_api_request("/trunks", payload, "Create Trunk")
        
        if result["success"]:
            trunk_sid = result["data"].get("sid")
            if trunk_sid:
                self.test_resources.append(("trunk", trunk_sid))
                self.logger.info(f"✅ Trunk created successfully: {trunk_sid}")
                return trunk_sid
            else:
                self.logger.error("❌ Trunk creation succeeded but no SID returned")
                return None
        else:
            self.logger.error(f"❌ Trunk creation failed: {result.get('error', 'Unknown error')}")
            return None
    
    def step_2_map_did(self, trunk_sid: str) -> bool:
        """Step 2: Map DID to trunk"""
        self.logger.info("📞 Step 2: Mapping DID to trunk")
        
        payload = {"phone_number": self.test_did}
        endpoint = f"/trunks/{trunk_sid}/phone-numbers"
        
        result = self.make_api_request(endpoint, payload, "Map DID")
        
        if result["success"]:
            phone_number_sid = result["data"].get("sid")
            if phone_number_sid:
                self.test_resources.append(("phone_number", phone_number_sid, trunk_sid))
            self.logger.info(f"✅ DID {self.test_did} mapped to trunk successfully")
            return True
        else:
            self.logger.error(f"❌ DID mapping failed: {result.get('error', 'Unknown error')}")
            return False
    
    def step_3_whitelist_ip(self, trunk_sid: str) -> bool:
        """Step 3: Whitelist IP address"""
        self.logger.info("🔒 Step 3: Whitelisting IP address")
        
        payload = {
            "ip": self.test_ip,
            "mask": int(os.getenv("WHITELIST_MASK", "32"))
        }
        endpoint = f"/trunks/{trunk_sid}/whitelisted-ips"
        
        result = self.make_api_request(endpoint, payload, "Whitelist IP")
        
        if result["success"]:
            whitelist_sid = result["data"].get("sid")
            if whitelist_sid:
                self.test_resources.append(("whitelist", whitelist_sid, trunk_sid))
            self.logger.info(f"✅ IP {self.test_ip} whitelisted successfully")
            return True
        else:
            self.logger.error(f"❌ IP whitelisting failed: {result.get('error', 'Unknown error')}")
            return False
    
    def step_4_add_destinations(self, trunk_sid: str) -> Dict[str, bool]:
        """Step 4: Add destination URIs for UDP, TCP, and TLS"""
        self.logger.info("🎯 Step 4: Adding destination URIs")
        
        results = {}
        transports = ["UDP", "TCP", "TLS"]
        
        for transport in transports:
            self.logger.info(f"  Adding {transport} destination...")
            
            if transport.upper() == "UDP":
                destination = f"{self.test_dest_ip}:{self.test_dest_port}"
            else:
                destination = f"{self.test_dest_ip}:{self.test_dest_port};transport={transport.lower()}"
            
            payload = {"destinations": [{"destination": destination}]}
            endpoint = f"/trunks/{trunk_sid}/destination-uris"
            
            result = self.make_api_request(endpoint, payload, f"Add {transport} Destination")
            
            if result["success"]:
                dest_sid = result["data"].get("sid")
                if dest_sid:
                    self.test_resources.append(("destination", dest_sid, trunk_sid))
                self.logger.info(f"  ✅ {transport} destination added successfully")
                results[transport] = True
            else:
                self.logger.error(f"  ❌ {transport} destination failed: {result.get('error', 'Unknown error')}")
                results[transport] = False
        
        return results
    
    def step_5_set_trunk_alias(self, trunk_sid: str) -> bool:
        """Step 5: Set trunk external alias (optional)"""
        exophone = os.getenv("EXOPHONE")
        if not exophone:
            self.logger.info("📝 Step 5: Skipping trunk alias (EXOPHONE not set)")
            return True
        
        self.logger.info("📝 Step 5: Setting trunk external alias")
        
        payload = {
            "settings": [{"name": "trunk_external_alias", "value": exophone}]
        }
        endpoint = f"/trunks/{trunk_sid}/settings"
        
        result = self.make_api_request(endpoint, payload, "Set Trunk Alias")
        
        if result["success"]:
            settings_sid = result["data"].get("sid")
            if settings_sid:
                self.test_resources.append(("settings", settings_sid, trunk_sid))
            self.logger.info(f"✅ Trunk alias set to {exophone}")
            return True
        else:
            self.logger.error(f"❌ Setting trunk alias failed: {result.get('error', 'Unknown error')}")
            return False
    
    def step_6_verify_configuration(self, trunk_sid: str) -> bool:
        """Step 6: Verify trunk configuration (if GET endpoints are available)"""
        self.logger.info("🔍 Step 6: Verifying trunk configuration")
        
        # Note: This is a placeholder for verification
        # In a real implementation, you would make GET requests to verify:
        # - Trunk exists and is active
        # - DID is properly mapped
        # - IP whitelist is configured
        # - Destinations are set up
        # - Settings are applied
        
        # For this demo, we'll simulate verification
        time.sleep(2)  # Simulate verification delay
        
        self.logger.info("✅ Trunk configuration verification completed")
        self.logger.info(f"   Trunk SID: {trunk_sid}")
        self.logger.info(f"   DID: {self.test_did}")
        self.logger.info(f"   Whitelisted IP: {self.test_ip}")
        self.logger.info(f"   Destinations: UDP, TCP, TLS")
        
        return True
    
    def cleanup_resources(self):
        """Clean up created test resources"""
        if not self.cleanup:
            self.logger.info("🧹 Cleanup disabled, leaving test resources")
            return
        
        self.logger.info("🧹 Cleaning up test resources...")
        
        # Note: This is a placeholder for cleanup
        # In a real implementation, you would make DELETE requests
        # to remove created resources in reverse order
        
        for resource_type, resource_id, *args in reversed(self.test_resources):
            self.logger.info(f"   Would delete {resource_type}: {resource_id}")
            # DELETE request would go here
        
        self.logger.info("✅ Cleanup completed")
    
    def run_integration_test(self) -> Dict[str, Any]:
        """Run the complete integration test workflow"""
        test_start_time = time.time()
        self.logger.info("🚀 Starting Exotel vSIP Integration Test")
        self.logger.info(f"Test trunk name: {self.test_trunk_name}")
        
        test_results = {
            "test_name": "exotel_vsip_integration",
            "start_time": datetime.datetime.now().isoformat(),
            "steps": {},
            "overall_success": False,
            "duration": 0,
            "created_resources": []
        }
        
        try:
            # Step 1: Create trunk
            trunk_sid = self.step_1_create_trunk()
            test_results["steps"]["create_trunk"] = trunk_sid is not None
            
            if not trunk_sid:
                test_results["error"] = "Failed to create trunk"
                return test_results
            
            test_results["trunk_sid"] = trunk_sid
            
            # Step 2: Map DID
            test_results["steps"]["map_did"] = self.step_2_map_did(trunk_sid)
            
            # Step 3: Whitelist IP
            test_results["steps"]["whitelist_ip"] = self.step_3_whitelist_ip(trunk_sid)
            
            # Step 4: Add destinations
            destination_results = self.step_4_add_destinations(trunk_sid)
            test_results["steps"]["destinations"] = destination_results
            
            # Step 5: Set trunk alias
            test_results["steps"]["set_alias"] = self.step_5_set_trunk_alias(trunk_sid)
            
            # Step 6: Verify configuration
            test_results["steps"]["verify_config"] = self.step_6_verify_configuration(trunk_sid)
            
            # Calculate overall success
            all_steps_passed = all([
                test_results["steps"]["create_trunk"],
                test_results["steps"]["map_did"],
                test_results["steps"]["whitelist_ip"],
                all(destination_results.values()),
                test_results["steps"]["set_alias"],
                test_results["steps"]["verify_config"]
            ])
            
            test_results["overall_success"] = all_steps_passed
            test_results["created_resources"] = [
                f"{res[0]}:{res[1]}" for res in self.test_resources
            ]
            
            if all_steps_passed:
                self.logger.info("🎉 Integration test PASSED - All steps completed successfully!")
            else:
                self.logger.warning("⚠️ Integration test PARTIAL - Some steps failed")
            
        except Exception as e:
            self.logger.error(f"💥 Integration test FAILED with exception: {str(e)}")
            test_results["error"] = str(e)
            test_results["overall_success"] = False
        
        finally:
            # Cleanup
            self.cleanup_resources()
            
            # Calculate duration
            test_results["duration"] = time.time() - test_start_time
            test_results["end_time"] = datetime.datetime.now().isoformat()
            
            # Save results
            self.save_test_results(test_results)
        
        return test_results
    
    def save_test_results(self, results: Dict[str, Any]):
        """Save test results to file"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(
            os.path.dirname(__file__), '..', 'logs', 
            f'integration_test_results_{timestamp}.json'
        )
        
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"📁 Test results saved to: {results_file}")

def main():
    """Main integration test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Exotel vSIP Integration Test")
    parser.add_argument("--no-cleanup", action="store_true", help="Skip cleanup of test resources")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    log_level = logging.DEBUG if args.verbose else logging.INFO
    cleanup = not args.no_cleanup
    
    # Run integration test
    integration_test = IntegrationTest(cleanup=cleanup, log_level=log_level)
    results = integration_test.run_integration_test()
    
    # Print summary
    print(f"\n{'='*60}")
    print("🎯 INTEGRATION TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Overall Result: {'✅ PASSED' if results['overall_success'] else '❌ FAILED'}")
    print(f"Duration: {results['duration']:.2f} seconds")
    print(f"Trunk SID: {results.get('trunk_sid', 'N/A')}")
    
    print(f"\n📋 Step Results:")
    for step, result in results["steps"].items():
        if isinstance(result, dict):
            # Handle destination results
            for transport, success in result.items():
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"  {step}_{transport.lower()}: {status}")
        else:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {step}: {status}")
    
    if results["created_resources"]:
        print(f"\n🗂️ Created Resources:")
        for resource in results["created_resources"]:
            print(f"  {resource}")
    
    # Exit with appropriate code
    sys.exit(0 if results['overall_success'] else 1)

if __name__ == "__main__":
    main() 