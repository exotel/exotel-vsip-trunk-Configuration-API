#!/usr/bin/env python3

"""
Mock Exotel API Server for Testing
Simulates Exotel API responses for development and testing
"""

import json
import logging
import datetime
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

class MockExotelAPIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests to simulate Exotel API"""
        
        # Parse URL and get path
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        # Get request body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            request_payload = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
            return
        
        # Log request
        self.log_request_details(self.path, request_payload)
        
        # Route to appropriate handler
        if self.is_trunks_endpoint(path_parts):
            self.handle_create_trunk(request_payload)
        elif self.is_phone_numbers_endpoint(path_parts):
            self.handle_map_did(path_parts, request_payload)
        elif self.is_whitelisted_ips_endpoint(path_parts):
            self.handle_whitelist_ip(path_parts, request_payload)
        elif self.is_destination_uris_endpoint(path_parts):
            self.handle_add_destination(path_parts, request_payload)
        elif self.is_settings_endpoint(path_parts):
            self.handle_set_trunk_alias(path_parts, request_payload)
        else:
            self.send_error_response(404, "Endpoint not found")
    
    def is_trunks_endpoint(self, path_parts):
        return len(path_parts) >= 3 and path_parts[-1] == 'trunks'
    
    def is_phone_numbers_endpoint(self, path_parts):
        return len(path_parts) >= 5 and path_parts[-1] == 'phone-numbers'
    
    def is_whitelisted_ips_endpoint(self, path_parts):
        return len(path_parts) >= 5 and path_parts[-1] == 'whitelisted-ips'
    
    def is_destination_uris_endpoint(self, path_parts):
        return len(path_parts) >= 5 and path_parts[-1] == 'destination-uris'
    
    def is_settings_endpoint(self, path_parts):
        return len(path_parts) >= 5 and path_parts[-1] == 'settings'
    
    def handle_create_trunk(self, payload):
        """Mock trunk creation"""
        
        # Validate required fields
        required_fields = ['trunk_name', 'nso_code', 'domain_name']
        missing_fields = [field for field in required_fields if field not in payload]
        
        if missing_fields:
            self.send_error_response(400, f"Missing required fields: {', '.join(missing_fields)}")
            return
        
        # Simulate different responses based on trunk name
        trunk_name = payload['trunk_name']
        
        if 'error' in trunk_name.lower():
            self.send_error_response(400, "Invalid trunk name")
            return
        elif 'conflict' in trunk_name.lower():
            self.send_error_response(409, "Trunk name already exists")
            return
        elif 'forbidden' in trunk_name.lower():
            self.send_error_response(403, "Access denied")
            return
        
        # Generate successful response
        trunk_sid = f"TR{uuid.uuid4().hex[:8].upper()}"
        response = {
            "sid": trunk_sid,
            "trunk_name": payload['trunk_name'],
            "nso_code": payload['nso_code'],
            "domain_name": payload['domain_name'],
            "status": "active",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        
        self.send_success_response(201, response)
    
    def handle_map_did(self, path_parts, payload):
        """Mock DID mapping"""
        
        trunk_sid = path_parts[-3]  # Extract trunk SID from path
        
        if 'phone_number' not in payload:
            self.send_error_response(400, "Missing required field: phone_number")
            return
        
        phone_number = payload['phone_number']
        
        # Validate phone number format
        if not phone_number.startswith('+'):
            self.send_error_response(400, "Phone number must start with +")
            return
        
        # Simulate error conditions
        if 'invalid' in phone_number.lower():
            self.send_error_response(400, "Invalid phone number format")
            return
        elif 'unavailable' in phone_number.lower():
            self.send_error_response(422, "Phone number not available")
            return
        
        response = {
            "sid": f"PN{uuid.uuid4().hex[:8].upper()}",
            "phone_number": phone_number,
            "trunk_sid": trunk_sid,
            "status": "active",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        
        self.send_success_response(201, response)
    
    def handle_whitelist_ip(self, path_parts, payload):
        """Mock IP whitelisting"""
        
        trunk_sid = path_parts[-3]
        
        required_fields = ['ip', 'mask']
        missing_fields = [field for field in required_fields if field not in payload]
        
        if missing_fields:
            self.send_error_response(400, f"Missing required fields: {', '.join(missing_fields)}")
            return
        
        # Validate IP format (basic check)
        ip = payload['ip']
        if not all(0 <= int(part) <= 255 for part in ip.split('.') if part.isdigit()):
            self.send_error_response(400, "Invalid IP address format")
            return
        
        response = {
            "sid": f"WL{uuid.uuid4().hex[:8].upper()}",
            "ip": payload['ip'],
            "mask": payload['mask'],
            "trunk_sid": trunk_sid,
            "status": "active",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        
        self.send_success_response(201, response)
    
    def handle_add_destination(self, path_parts, payload):
        """Mock destination URI addition"""
        
        trunk_sid = path_parts[-3]
        
        if 'destinations' not in payload or not payload['destinations']:
            self.send_error_response(400, "Missing required field: destinations")
            return
        
        destinations = payload['destinations']
        
        # Validate destination format
        for dest in destinations:
            if 'destination' not in dest:
                self.send_error_response(400, "Missing destination in destinations array")
                return
            
            destination = dest['destination']
            if ':' not in destination:
                self.send_error_response(400, "Invalid destination format")
                return
        
        response = {
            "sid": f"DU{uuid.uuid4().hex[:8].upper()}",
            "destinations": destinations,
            "trunk_sid": trunk_sid,
            "status": "active",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        
        self.send_success_response(201, response)
    
    def handle_set_trunk_alias(self, path_parts, payload):
        """Mock trunk alias setting"""
        
        trunk_sid = path_parts[-3]
        
        if 'settings' not in payload or not payload['settings']:
            self.send_error_response(400, "Missing required field: settings")
            return
        
        settings = payload['settings']
        
        # Validate settings format
        for setting in settings:
            if 'name' not in setting or 'value' not in setting:
                self.send_error_response(400, "Invalid setting format")
                return
        
        response = {
            "sid": f"TS{uuid.uuid4().hex[:8].upper()}",
            "settings": settings,
            "trunk_sid": trunk_sid,
            "status": "active",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        
        self.send_success_response(201, response)
    
    def send_success_response(self, status_code, data):
        """Send successful JSON response"""
        response_json = json.dumps(data, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_json)))
        self.end_headers()
        self.wfile.write(response_json.encode('utf-8'))
        
        logging.info(f"✅ Sent {status_code} response: {response_json[:100]}...")
    
    def send_error_response(self, status_code, message):
        """Send error JSON response"""
        error_data = {
            "error": "API Error",
            "message": message,
            "status_code": status_code,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
        
        response_json = json.dumps(error_data, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_json)))
        self.end_headers()
        self.wfile.write(response_json.encode('utf-8'))
        
        logging.error(f"❌ Sent {status_code} error: {message}")
    
    def log_request_details(self, path, payload):
        """Log incoming request details"""
        logging.info(f"📨 Request: {self.command} {path}")
        logging.debug(f"Headers: {dict(self.headers)}")
        logging.debug(f"Payload: {json.dumps(payload, indent=2)}")
    
    def log_message(self, format, *args):
        """Override to use our logging system"""
        logging.info(f"{self.address_string()} - {format % args}")

class MockServer:
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        self.thread = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def start(self):
        """Start the mock server"""
        self.server = HTTPServer(('localhost', self.port), MockExotelAPIHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        
        logging.info(f"🚀 Mock Exotel API server started on http://localhost:{self.port}")
        logging.info("📖 Available endpoints:")
        logging.info("  POST /v2/accounts/{account_sid}/trunks")
        logging.info("  POST /v2/accounts/{account_sid}/trunks/{trunk_sid}/phone-numbers")
        logging.info("  POST /v2/accounts/{account_sid}/trunks/{trunk_sid}/whitelisted-ips")
        logging.info("  POST /v2/accounts/{account_sid}/trunks/{trunk_sid}/destination-uris")
        logging.info("  POST /v2/accounts/{account_sid}/trunks/{trunk_sid}/settings")
    
    def stop(self):
        """Stop the mock server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logging.info("🛑 Mock server stopped")
    
    def wait(self):
        """Wait for the server thread"""
        if self.thread:
            self.thread.join()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Mock Exotel API Server")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Server port")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    server = MockServer(args.port)
    
    try:
        server.start()
        print(f"\n🔧 Mock server running on http://localhost:{args.port}")
        print("💡 To test against this server, set your environment:")
        print(f"   export EXO_SUBSCRIBIX_DOMAIN=localhost:{args.port}")
        print("   export EXO_AUTH_KEY=test_key")
        print("   export EXO_AUTH_TOKEN=test_token")
        print("   export EXO_ACCOUNT_SID=test_account")
        print("\n⭐ Special test cases:")
        print("   - trunk_name with 'error' -> 400 error")
        print("   - trunk_name with 'conflict' -> 409 error")
        print("   - trunk_name with 'forbidden' -> 403 error")
        print("   - phone_number with 'invalid' -> 400 error")
        print("   - phone_number with 'unavailable' -> 422 error")
        print("\n🛑 Press Ctrl+C to stop")
        
        server.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        server.stop()

if __name__ == "__main__":
    main() 