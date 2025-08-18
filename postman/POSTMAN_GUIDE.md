# 🚀 Exotel vSIP Postman Collection Guide

## 📋 **Overview**

This Postman collection provides a complete set of requests for testing all Exotel vSIP Trunk APIs. It includes automatic authentication, environment variables, response validation, and comprehensive documentation.

## ✨ **Features**

- **🔧 Complete API Coverage**: All 5 core vSIP operations
- **🔐 Automatic Authentication**: Basic Auth configured at collection level
- **🌍 Environment Variables**: Easy configuration management
- **✅ Response Tests**: Automatic validation of API responses
- **📝 Auto-Population**: Trunk SID automatically saved for subsequent requests
- **📚 Rich Documentation**: Detailed descriptions for each endpoint

---

## 🛠️ **Setup Instructions**

### **Step 1: Import Collection & Environment**

1. **Download Files**:
   - `Exotel_vSIP_API_Collection.json` - Main collection
   - `Exotel_vSIP_Environment.json` - Environment variables

2. **Import in Postman**:
   - Open Postman
   - Click **Import** button
   - Select both JSON files
   - Click **Import**

### **Step 2: Configure Environment**

1. **Select Environment**: Choose "Exotel vSIP Environment" from dropdown
2. **Set Required Variables**:
   ```
   EXO_AUTH_KEY = your_actual_api_key
   EXO_AUTH_TOKEN = your_actual_auth_token
   EXO_SUBSCRIBIX_DOMAIN = api.in.exotel.com
   EXO_ACCOUNT_SID = your_actual_account_sid
   ```

3. **Get Credentials**: Visit [Exotel API Settings](https://my.in.exotel.com/apisettings/site#api-credentials)

4. **Optional Configuration**:
   ```
   DID_NUMBER = +91XXXXXXXXXX (from https://my.in.exotel.com/numbers)
   WHITELIST_IP = your_sip_server_ip
   TRUNK_DEST_IP = your_sip_server_ip
   EXOPHONE = +91XXXXXXXXXX
   ```

### **Step 3: Test Your Setup**

1. **Run Pre-request Check**: Any request will validate your environment variables
2. **Start with Trunk Creation**: Run "1. Trunk Creation" first
3. **Follow Sequence**: Use the numbered order for best results

---

## 📋 **API Operations**

### **1. Trunk Creation** 
- **Purpose**: Creates a new SIP trunk
- **Auto-saves**: `TRUNK_SID` for subsequent requests
- **Required**: `TRUNK_NAME`, `NSO_CODE`, `EXO_ACCOUNT_SID`

### **2. Map DID to Trunk**
- **Purpose**: Maps a phone number to the trunk
- **Required**: `DID_NUMBER`, `TRUNK_SID` (auto-populated)
- **Format**: E.164 (+CountryCodeNumber)

### **3. Whitelist IP Address**
- **Purpose**: Adds IP to trunk's security whitelist
- **Required**: `WHITELIST_IP`, `WHITELIST_MASK`
- **Recommended**: Use your SIP server's public IP

### **4a. Add UDP Destination**
- **Purpose**: Configures UDP SIP destination
- **Format**: `IP:PORT` (UDP is default)

### **4b. Add TCP Destination**
- **Purpose**: Configures TCP SIP destination
- **Format**: `IP:PORT;transport=tcp`

### **4c. Add TLS Destination**
- **Purpose**: Configures secure TLS SIP destination
- **Format**: `IP:PORT;transport=tls`

### **5. Set Trunk Alias**
- **Purpose**: Sets optional trunk external alias
- **Required**: `EXOPHONE` (virtual number)

---

## 🔧 **Environment Variables Reference**

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| **Authentication** |
| `EXO_AUTH_KEY` | ✅ | API Key | `your_api_key` |
| `EXO_AUTH_TOKEN` | ✅ | Auth Token | `your_auth_token` |
| `EXO_SUBSCRIBIX_DOMAIN` | ✅ | API Domain | `api.in.exotel.com` |
| `EXO_ACCOUNT_SID` | ✅ | Account SID | `your_account_sid` |
| **Configuration** |
| `TRUNK_NAME` | ✅ | Trunk Name | `postman_trunk` |
| `NSO_CODE` | ✅ | NSO Code | `ANY-ANY` |
| `DID_NUMBER` | ⚠️ | Virtual Number | `+91XXXXXXXXXX` |
| `WHITELIST_IP` | ⚠️ | SIP Server IP | `192.168.1.100` |
| `WHITELIST_MASK` | ⚠️ | Subnet Mask | `32` |
| `TRUNK_DEST_IP` | ⚠️ | Destination IP | `192.168.1.200` |
| `TRUNK_DEST_PORT` | ⚠️ | SIP Port | `5060` |
| `EXOPHONE` | ⚠️ | Alias Number | `+91XXXXXXXXXX` |
| **Auto-populated** |
| `TRUNK_SID` | 🔄 | Trunk ID | `trmum1XXXXX` |

---

## 🧪 **Testing Workflow**

### **Complete Workflow Test**
```
1. Create Trunk → Gets TRUNK_SID
2. Map DID → Associates phone number
3. Whitelist IP → Allows SIP traffic
4. Add Destinations → Configures routing (UDP/TCP/TLS)
5. Set Alias → Optional trunk configuration
```

### **Individual Testing**
- Each request can be run independently
- Trunk creation is prerequisite for others
- TRUNK_SID auto-populates from step 1

### **Response Validation**
- ✅ **Status Code**: All requests should return 200
- ✅ **Success Status**: `response.status = "success"`
- ✅ **Data Extraction**: Important IDs logged to console
- ✅ **Auto-population**: TRUNK_SID saved automatically

---

## 🔍 **Debugging & Troubleshooting**

### **Common Issues**

#### **❌ Missing Environment Variables**
```
Error: Missing required environment variables
Solution: Set all required variables in environment
```

#### **❌ Authentication Failed (401)**
```
Error: HTTP 401 Unauthorized
Solution: Verify EXO_AUTH_KEY and EXO_AUTH_TOKEN
Check: https://my.in.exotel.com/apisettings/site#api-credentials
```

#### **❌ Invalid Parameters (400)**
```
Error: HTTP 400 Bad Request
Common causes:
- Trunk name > 16 characters
- Invalid phone number format (use E.164: +CountryCodeNumber)
- Invalid IP address format
- Mask not between 16-32
```

#### **❌ Duplicate Resource (409)**
```
Error: Duplicate resource
Solution: Use unique trunk names, or check if resource already exists
```

### **Console Logging**
- All requests log success/failure to Postman console
- Check **Console** tab (bottom of Postman) for detailed logs
- TRUNK_SID extraction logged for verification

### **Response Inspection**
- **Status**: Should be 200 for successful requests
- **Body**: Contains detailed response with data/error information
- **Tests**: Green ✅ indicates passing validation

---

## 🌍 **Multi-Region Support**

### **India**
```
EXO_SUBSCRIBIX_DOMAIN = api.in.exotel.com
DID_NUMBER = +91XXXXXXXXXX
```

### **Singapore**
```
EXO_SUBSCRIBIX_DOMAIN = api.sg.exotel.com
DID_NUMBER = +65XXXXXXXX
```

### **United States**
```
EXO_SUBSCRIBIX_DOMAIN = api.us.exotel.com
DID_NUMBER = +1XXXXXXXXXX
```

---

## 📊 **Response Examples**

### **Successful Trunk Creation**
```json
{
  "response": {
    "status": "success",
    "data": {
      "trunk_name": "postman_trunk",
      "trunk_sid": "trmum1abc123def456ghi789",
      "status": "active",
      "domain_name": "your_account.pstn.exotel.com"
    }
  }
}
```

### **Error Response**
```json
{
  "response": {
    "status": "failure",
    "error_data": {
      "code": 1002,
      "message": "Invalid parameter",
      "description": "Maximum allowed length for TrunkName is 16"
    }
  }
}
```

---

## 🔗 **Additional Resources**

- **📚 Complete Error Reference**: [TRUNK_ERRORS_README.md](../TRUNK_ERRORS_README.md)
- **🛠️ Setup Guide**: [SETUP_GUIDE.md](../SETUP_GUIDE.md)
- **📖 Main Documentation**: [README.md](../README.md)
- **🔑 API Credentials**: [Exotel Dashboard](https://my.in.exotel.com/apisettings/site#api-credentials)
- **📱 Virtual Numbers**: [Number Management](https://my.in.exotel.com/numbers)
- **🔄 Call Flows**: [App Configuration](https://my.in.exotel.com/apps#installed-apps)

---

## 💡 **Pro Tips**

1. **⚡ Quick Start**: Run requests in numbered order for fastest setup
2. **🔄 Re-run Safe**: Most requests can be run multiple times (will show duplicate errors)
3. **📝 Console Logs**: Always check console for detailed success/failure information
4. **🎯 Environment**: Use different environments for dev/staging/production
5. **🔒 Security**: Keep credentials secure, don't share environment files
6. **📊 Testing**: Use Postman's test results to validate API responses
7. **🛠️ Debugging**: Check both response body and console logs for issues

---

**🎉 Happy Testing with Exotel vSIP APIs!** 

For issues or questions, check the [Complete Error Reference Guide](../TRUNK_ERRORS_README.md) or create an issue on GitHub. 