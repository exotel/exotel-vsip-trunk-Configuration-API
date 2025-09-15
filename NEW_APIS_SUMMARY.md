# 🆕 New APIs Added to Exotel vSIP Repository

## Overview
Added 5 new API operations to the existing Exotel vSIP trunk configuration repository, expanding from 5 to 10 total operations.

## 📋 New APIs Added

### 1. **GET Destination URIs**
- **Endpoint**: `GET /v2/accounts/{account_sid}/trunks/{trunk_sid}/destination-uris`
- **Purpose**: Retrieve all destination URIs configured for a trunk
- **Files Added**:
  - `curl/get_destination_uris.sh`
  - `python/get_destination_uris.py`
  - `go/get_destination_uris.go`
  - `java/GetDestinationUris.java`
  - `php/get_destination_uris.php`

### 2. **GET Whitelisted IPs**
- **Endpoint**: `GET /v2/accounts/{account_sid}/trunks/{trunk_sid}/whitelisted-ips`
- **Purpose**: Retrieve all whitelisted IP addresses for a trunk
- **Files Added**:
  - `curl/get_whitelisted_ips.sh`
  - `python/get_whitelisted_ips.py`
  - `go/get_whitelisted_ips.go`
  - `java/GetWhitelistedIps.java`
  - `php/get_whitelisted_ips.php`

### 3. **GET Credentials**
- **Endpoint**: `GET /v2/accounts/{account_sid}/trunks/{trunk_sid}/credentials`
- **Purpose**: Retrieve authentication credentials for a trunk
- **Files Added**:
  - `curl/get_credentials.sh`
  - `python/get_credentials.py`
  - `go/get_credentials.go`
  - `java/GetCredentials.java`
  - `php/get_credentials.php`

### 4. **GET Phone Numbers**
- **Endpoint**: `GET /v2/accounts/{account_sid}/trunks/{trunk_sid}/destination-uris`
- **Purpose**: Retrieve phone numbers associated with a trunk (same endpoint as destination URIs)
- **Files Added**:
  - `curl/get_phone_numbers.sh`
  - `python/get_phone_numbers.py`
  - `go/get_phone_numbers.go`
  - `java/GetPhoneNumbers.java`
  - `php/get_phone_numbers.php`

### 5. **DELETE Trunk**
- **Endpoint**: `DELETE /v2/accounts/{account_sid}/trunks?trunk_sid={trunk_sid}`
- **Purpose**: Delete an existing trunk
- **Files Added**:
  - `curl/delete_trunk.sh`
  - `python/delete_trunk.py`
  - `go/delete_trunk.go`
  - `java/DeleteTrunk.java`
  - `php/delete_trunk.php`

## 🔧 Client Library Updates

### Enhanced Client Libraries
All client libraries (`_client.py`, `_client.go`, `_Client.java`, `_client.php`) were updated with:
- **GET method**: For retrieving data from the API
- **DELETE method**: For deleting resources

### Method Signatures
- **Python**: `get(path)`, `delete(path)`
- **Go**: `get(path string)`, `delete(path string)`
- **Java**: `get(String path)`, `delete(String path)`
- **PHP**: `exo_get($path)`, `exo_delete($path)`

## 📚 Documentation Updates

### README.md Changes
- Updated API operations table from 5 to 10 operations
- Added new GET and DELETE examples
- Updated feature count and API coverage statistics
- Added usage examples for new APIs

### New Files
- `demo_new_apis.py`: Interactive demo script showing how to use the new APIs
- `NEW_APIS_SUMMARY.md`: This summary document
- `POSTMAN_UPDATES_SUMMARY.md`: Complete Postman collection updates summary

### Updated Postman Collection
- **Enhanced Collection**: All 5 new APIs added to Postman collection
- **Complete CRUD**: Now supports full Create, Read, Delete operations
- **Safety Features**: DELETE operation with warnings and auto-cleanup
- **Updated Documentation**: Enhanced POSTMAN_GUIDE.md with new workflows

## 🚀 Usage Examples

### Environment Variables Required
All new APIs require the `TRUNK_SID` environment variable:
```bash
export TRUNK_SID="your_trunk_sid_here"
```

### Quick Test Commands

#### cURL Examples
```bash
# Get destination URIs
./curl/get_destination_uris.sh

# Get whitelisted IPs  
./curl/get_whitelisted_ips.sh

# Get credentials
./curl/get_credentials.sh

# Delete trunk (be careful!)
./curl/delete_trunk.sh
```

#### Python Examples
```bash
# Get destination URIs
python3 python/get_destination_uris.py

# Get whitelisted IPs
python3 python/get_whitelisted_ips.py

# Delete trunk
python3 python/delete_trunk.py
```

#### Interactive Demo
```bash
# Run the demo script
python3 demo_new_apis.py
```

## ⚠️ Important Notes

### DELETE Operation Warning
The DELETE trunk operation is **destructive** and **permanent**. Always:
1. Test with non-production trunks first
2. Verify the trunk SID before deletion
3. Ensure you have backups of trunk configurations

### Error Handling
All new API implementations include:
- ✅ Environment variable validation
- ✅ HTTP error handling
- ✅ Consistent error messages
- ✅ Proper exit codes

### Authentication
All APIs use the same authentication method as existing APIs:
- HTTP Basic Auth with API Key and Token
- Credentials from environment variables

## 🔄 Backward Compatibility

### Fully Compatible
- All existing APIs remain unchanged
- No breaking changes to existing client libraries
- Existing scripts and code continue to work

### Additive Changes Only
- New methods added to client libraries
- New files added to each language directory
- Enhanced documentation and examples

## 📊 Repository Statistics

### Before
- **5 API operations** (all POST)
- **35 files** across 5 languages
- **POST-only** functionality

### After  
- **10 API operations** (5 POST, 4 GET, 1 DELETE)
- **60 files** across 5 languages
- **Full CRUD** functionality (Create, Read, Delete)

## 🎯 Next Steps

### For Users
1. Update your `.env` file with credentials
2. Set `TRUNK_SID` environment variable
3. Test the new APIs with your trunk
4. Integrate into your workflows

### For Developers
1. Review the new client library methods
2. Check error handling patterns
3. Test with your specific use cases
4. Provide feedback on the implementations

---

**🚀 The repository now provides complete vSIP trunk management capabilities with full CRUD operations across all supported languages!** 