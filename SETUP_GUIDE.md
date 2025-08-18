# 🚀 Complete Setup Guide for Exotel vSIP Trunk API

## 📋 **Step-by-Step Setup Process**

### **Step 1: Get Your Exotel Credentials**

1. **Login to Exotel Dashboard**: Go to [https://my.in.exotel.com](https://my.in.exotel.com)

2. **Get API Credentials**: Visit [API Settings](https://my.in.exotel.com/apisettings/site#api-credentials)
   - Copy your **API Key** (EXO_AUTH_KEY)
   - Copy your **Auth Token** (EXO_AUTH_TOKEN) 
   - Note your **Account SID** (EXO_ACCOUNT_SID)
   - Note your **API Domain** (EXO_SUBSCRIBIX_DOMAIN)

3. **Get Virtual Numbers**: Visit [Virtual Numbers](https://my.in.exotel.com/numbers)
   - Note your DIDs/Exophones for testing
   - These will be used for DID_NUMBER and EXOPHONE

4. **Optional - Create Call Flows**: Visit [Apps & Flows](https://my.in.exotel.com/apps#installed-apps)
   - Create flows with Connect Applet if needed for call routing

### **Step 2: Configure Environment**

1. **Clone Repository**:
   ```bash
   git clone https://github.com/your-username/exotel-vsip-trunk-api.git
   cd exotel-vsip-trunk-api
   ```

2. **Setup Environment**:
   ```bash
   cp .env.example .env
   ```

3. **Edit .env File** with your credentials:
   ```bash
   # From https://my.in.exotel.com/apisettings/site#api-credentials
   EXO_AUTH_KEY=your_actual_api_key_here
   EXO_AUTH_TOKEN=your_actual_auth_token_here
   EXO_SUBSCRIBIX_DOMAIN=api.in.exotel.com
   EXO_ACCOUNT_SID=your_actual_account_sid_here
   
   # From https://my.in.exotel.com/numbers
   DID_NUMBER=+91XXXXXXXXXX
   EXOPHONE=+91XXXXXXXXXX
   
   # Your SIP server details
   TRUNK_DEST_IP=your_sip_server_ip
   WHITELIST_IP=your_sip_server_public_ip
   ```

### **Step 3: Test Your Setup**

1. **Quick Test with cURL**:
   ```bash
   cd curl/
   ./create_trunk.sh
   ```

2. **Comprehensive Test with Python**:
   ```bash
   # Install test dependencies (optional)
   pip3 install -r tests/requirements.txt
   
   # Run all tests
   python3 tests/test_all_apis.py --verbose
   ```

3. **Test Individual Operations**:
   ```bash
   # Test trunk creation only
   python3 tests/test_all_apis.py --test create
   
   # Test DID mapping only  
   python3 tests/test_all_apis.py --test map
   ```

### **Step 4: Verify Your Integration**

1. **Check Logs**: Test results are saved in `logs/` directory

2. **Verify in Exotel Dashboard**: 
   - Check your trunks in Exotel dashboard
   - Verify DID mappings
   - Test call routing

3. **Test Call Flow**:
   - Make a test call to your DID
   - Verify it reaches your SIP server
   - Check webhook data for troubleshooting

---

## 🔧 **Common Configuration Examples**

### **India Setup**
```bash
EXO_SUBSCRIBIX_DOMAIN=api.in.exotel.com
DID_NUMBER=+918048636999
EXOPHONE=+918048636999
```

### **Singapore Setup**
```bash
EXO_SUBSCRIBIX_DOMAIN=api.sg.exotel.com
DID_NUMBER=+6512345678
EXOPHONE=+6512345678
```

### **US Setup**
```bash
EXO_SUBSCRIBIX_DOMAIN=api.us.exotel.com
DID_NUMBER=+14155552671
EXOPHONE=+14155552671
```

---

## 🚨 **Troubleshooting**

### **Authentication Issues**
- ✅ Verify credentials at [API Settings](https://my.in.exotel.com/apisettings/site#api-credentials)
- ✅ Check no extra spaces in .env file
- ✅ Ensure API is enabled for your account

### **Phone Number Issues**
- ✅ Use E.164 format (+CountryCodeNumber)
- ✅ Verify number ownership at [Virtual Numbers](https://my.in.exotel.com/numbers)
- ✅ No dashes or spaces in phone numbers

### **SIP Connection Issues**
- ✅ Verify your SIP server is running at TRUNK_DEST_IP:5060
- ✅ Check firewall allows traffic from Exotel IPs
- ✅ Ensure WHITELIST_IP matches your SIP server's public IP

### **Call Routing Issues**
- ✅ Verify DID is mapped to the trunk
- ✅ Check call flows at [Apps & Flows](https://my.in.exotel.com/apps#installed-apps)
- ✅ Test with webhook.site for debugging

---

## 📞 **Testing Call Flow**

### **Complete Workflow Test**
1. **Create trunk** with API
2. **Map your DID** to the trunk
3. **Whitelist your SIP server IP**
4. **Add destination URI** pointing to your SIP server
5. **Make test call** to your DID
6. **Verify call reaches** your SIP server

### **Expected Call Flow**
```
Caller → Exotel DID → Trunk → Your SIP Server
         ↓
    Webhook notification with call details
```

---

## 🔗 **Important URLs Reference**

| Purpose | URL | Description |
|---------|-----|-------------|
| **API Credentials** | [https://my.in.exotel.com/apisettings/site#api-credentials](https://my.in.exotel.com/apisettings/site#api-credentials) | Get API Key, Token, Account SID |
| **Virtual Numbers** | [https://my.in.exotel.com/numbers](https://my.in.exotel.com/numbers) | Manage DIDs and Exophones |
| **Call Flows** | [https://my.in.exotel.com/apps#installed-apps](https://my.in.exotel.com/apps#installed-apps) | Create flows with Connect Applet |
| **Dashboard** | [https://my.in.exotel.com](https://my.in.exotel.com) | Main Exotel dashboard |
| **API Documentation** | [https://developer.exotel.com](https://developer.exotel.com) | Official API docs |

---

## ✅ **Setup Checklist**

- [ ] ✅ Got API credentials from Exotel dashboard
- [ ] ✅ Noted virtual numbers from Exotel dashboard  
- [ ] ✅ Cloned repository and configured .env
- [ ] ✅ Tested trunk creation with cURL/Python
- [ ] ✅ Verified SIP server is accessible
- [ ] ✅ Made test call to validate complete flow
- [ ] ✅ Reviewed error reference guide
- [ ] ✅ Set up monitoring and logging

---

**🎉 Your Exotel vSIP integration is ready for production!** 