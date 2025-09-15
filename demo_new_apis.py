#!/usr/bin/env python3
"""
Demo script for the new Exotel vSIP APIs
Shows how to use GET and DELETE operations

Usage:
1. Set environment variables in .env file
2. Set TRUNK_SID environment variable to an existing trunk
3. Run: python3 demo_new_apis.py
"""

import os
import sys

# Add python directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))

from _client import get, delete

def demo_get_apis():
    """Demonstrate the new GET APIs"""
    trunk_sid = os.getenv('TRUNK_SID')
    if not trunk_sid:
        print("❌ Error: TRUNK_SID environment variable is required")
        print("   Set it to an existing trunk SID to test the GET APIs")
        return False
    
    print(f"🔍 Testing GET APIs for trunk: {trunk_sid}")
    print("=" * 50)
    
    # Test each GET API
    apis_to_test = [
        ("destination-uris", "Destination URIs"),
        ("whitelisted-ips", "Whitelisted IPs"), 
        ("credentials", "Credentials")
    ]
    
    for endpoint, description in apis_to_test:
        try:
            print(f"\n📡 Getting {description}...")
            result = get(f'/trunks/{trunk_sid}/{endpoint}')
            print(f"✅ Successfully retrieved {description}")
        except Exception as e:
            print(f"❌ Failed to get {description}: {e}")
    
    return True

def demo_delete_api():
    """Demonstrate the DELETE API (with warning)"""
    trunk_sid = os.getenv('TRUNK_SID_TO_DELETE')
    
    if not trunk_sid:
        print("\n🗑️  DELETE API Demo")
        print("=" * 50)
        print("⚠️  To test DELETE API, set TRUNK_SID_TO_DELETE environment variable")
        print("   WARNING: This will permanently delete the trunk!")
        print("   Example: export TRUNK_SID_TO_DELETE=your_test_trunk_sid")
        return False
    
    print(f"\n🗑️  Testing DELETE API for trunk: {trunk_sid}")
    print("⚠️  WARNING: This will delete the trunk permanently!")
    
    confirm = input("Type 'DELETE' to confirm: ")
    if confirm != 'DELETE':
        print("❌ Delete cancelled")
        return False
    
    try:
        print(f"🗑️  Deleting trunk {trunk_sid}...")
        result = delete(f'/trunks?trunk_sid={trunk_sid}')
        print("✅ Trunk deleted successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to delete trunk: {e}")
        return False

def main():
    """Main demo function"""
    print("🚀 Exotel vSIP New APIs Demo")
    print("=" * 50)
    print("This demo shows the new GET and DELETE APIs added to the repository")
    print()
    
    # Check basic environment setup
    required_vars = ['EXO_AUTH_KEY', 'EXO_AUTH_TOKEN', 'EXO_SUBSCRIBIX_DOMAIN', 'EXO_ACCOUNT_SID']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("   Please set up your .env file with Exotel credentials")
        return 1
    
    # Demo GET APIs
    if not demo_get_apis():
        return 1
    
    # Demo DELETE API
    demo_delete_api()
    
    print("\n🎉 Demo completed!")
    print("\n📚 Available new API files:")
    print("   • curl/get_*.sh - cURL scripts for GET operations")
    print("   • curl/delete_trunk.sh - cURL script for DELETE operation")
    print("   • python/get_*.py - Python scripts for GET operations") 
    print("   • python/delete_trunk.py - Python script for DELETE operation")
    print("   • Similar files available in go/, java/, and php/ directories")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 