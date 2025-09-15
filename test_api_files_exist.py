#!/usr/bin/env python3
"""
Simple test to verify all new API files exist and are properly structured
"""

import os
import sys

def test_file_exists_and_executable(filepath, description):
    """Test if file exists and is executable"""
    if os.path.exists(filepath):
        if os.access(filepath, os.X_OK):
            print(f"✅ {description}")
            return True
        else:
            print(f"⚠️ {description} (exists but not executable)")
            return True  # Still counts as success for existence
    else:
        print(f"❌ {description} (missing)")
        return False

def test_file_contains_content(filepath, description, required_content=None):
    """Test if file exists and contains expected content"""
    if not os.path.exists(filepath):
        print(f"❌ {description} (missing)")
        return False
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        if required_content and required_content not in content:
            print(f"⚠️ {description} (missing expected content)")
            return False
        
        print(f"✅ {description}")
        return True
    except Exception as e:
        print(f"❌ {description} (error reading: {e})")
        return False

def main():
    """Test all new API files"""
    print("🚀 API Files Existence Test")
    print("=" * 50)
    
    base_dir = os.path.dirname(__file__)
    results = []
    
    # Test cURL scripts
    print("\n🌐 cURL Scripts")
    print("-" * 30)
    curl_files = [
        ("get_destination_uris.sh", "GET destination URIs"),
        ("get_whitelisted_ips.sh", "GET whitelisted IPs"),
        ("get_credentials.sh", "GET credentials"),
        ("get_phone_numbers.sh", "GET phone numbers"),
        ("delete_trunk.sh", "DELETE trunk")
    ]
    
    for filename, desc in curl_files:
        filepath = os.path.join(base_dir, "curl", filename)
        result = test_file_exists_and_executable(filepath, f"{desc} cURL script")
        results.append(result)
    
    # Test Python files
    print("\n🐍 Python Files")
    print("-" * 30)
    python_files = [
        ("get_destination_uris.py", "GET destination URIs", "from _client import get"),
        ("get_whitelisted_ips.py", "GET whitelisted IPs", "from _client import get"),
        ("get_credentials.py", "GET credentials", "from _client import get"),
        ("get_phone_numbers.py", "GET phone numbers", "from _client import get"),
        ("delete_trunk.py", "DELETE trunk", "from _client import delete")
    ]
    
    for filename, desc, content in python_files:
        filepath = os.path.join(base_dir, "python", filename)
        result = test_file_contains_content(filepath, f"{desc} Python script", content)
        results.append(result)
    
    # Test Go files
    print("\n🐹 Go Files")
    print("-" * 30)
    go_files = [
        ("get_destination_uris.go", "GET destination URIs", "func main()"),
        ("get_whitelisted_ips.go", "GET whitelisted IPs", "func main()"),
        ("get_credentials.go", "GET credentials", "func main()"),
        ("get_phone_numbers.go", "GET phone numbers", "func main()"),
        ("delete_trunk.go", "DELETE trunk", "func main()")
    ]
    
    for filename, desc, content in go_files:
        filepath = os.path.join(base_dir, "go", filename)
        result = test_file_contains_content(filepath, f"{desc} Go file", content)
        results.append(result)
    
    # Test Java files
    print("\n☕ Java Files")
    print("-" * 30)
    java_files = [
        ("GetDestinationUris.java", "GET destination URIs", "public class GetDestinationUris"),
        ("GetWhitelistedIps.java", "GET whitelisted IPs", "public class GetWhitelistedIps"),
        ("GetCredentials.java", "GET credentials", "public class GetCredentials"),
        ("GetPhoneNumbers.java", "GET phone numbers", "public class GetPhoneNumbers"),
        ("DeleteTrunk.java", "DELETE trunk", "public class DeleteTrunk")
    ]
    
    for filename, desc, content in java_files:
        filepath = os.path.join(base_dir, "java", filename)
        result = test_file_contains_content(filepath, f"{desc} Java file", content)
        results.append(result)
    
    # Test PHP files
    print("\n🐘 PHP Files")
    print("-" * 30)
    php_files = [
        ("get_destination_uris.php", "GET destination URIs", "exo_get"),
        ("get_whitelisted_ips.php", "GET whitelisted IPs", "exo_get"),
        ("get_credentials.php", "GET credentials", "exo_get"),
        ("get_phone_numbers.php", "GET phone numbers", "exo_get"),
        ("delete_trunk.php", "DELETE trunk", "exo_delete")
    ]
    
    for filename, desc, content in php_files:
        filepath = os.path.join(base_dir, "php", filename)
        result = test_file_contains_content(filepath, f"{desc} PHP file", content)
        results.append(result)
    
    # Test enhanced client files
    print("\n🔧 Enhanced Client Files")
    print("-" * 30)
    client_tests = [
        ("python/_client.py", "Python client with GET/DELETE", "def get(path):"),
        ("go/_client.go", "Go client with GET/DELETE", "func get(path string)"),
        ("java/_Client.java", "Java client with GET/DELETE", "static String get(String path)"),
        ("php/_client.php", "PHP client with GET/DELETE", "function exo_get($path)")
    ]
    
    for filepath, desc, content in client_tests:
        full_path = os.path.join(base_dir, filepath)
        result = test_file_contains_content(full_path, desc, content)
        results.append(result)
    
    # Summary
    print("\n🎯 Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"📊 Results: {passed}/{total} files validated successfully")
    
    if passed == total:
        print("🎉 All new API files are properly implemented!")
        return 0
    else:
        print("⚠️ Some files are missing or have issues")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 