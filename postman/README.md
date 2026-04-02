# 📬 Postman Collection for Exotel vSIP APIs

Layout matches the **[Exotel SIP Trunking APIs](https://www.postman.com/grey-star-272776/exotel-sip-trunking-apis/overview)** workspace style:

1. **`1. GETTING STARTED (PSTN)`** — `POST Step 1:` … `Step 4:` (trunk, DID **pstn**, ACL, destination)
2. **`2. STREAMKIT (Voice AI)`** — trunk, DID **flow**, ACL, SIP **digest credentials**
3. **`3. MANAGE & VIEW`** — same GET/PUT/POST/**DEL** naming as the workspace, plus extra management calls (list trunks, trunk-map, credential CRUD, etc.)

Collection **Overview** text (introduction, getting started, best practices) is in the collection’s **description** field in Postman.

## 📦 **What's Included**

| File | Description |
|------|-------------|
| `Exotel_vSIP_API_Collection.json` | **Exotel SIP Trunking APIs** — three numbered folders + overview-style description |
| `Exotel_vSIP_Environment.json` | Environment variables (credentials, resource IDs, pagination) |
| `POSTMAN_GUIDE.md` | Setup and usage guide |
| `_generate_collection.py` | Regenerates `Exotel_vSIP_API_Collection.json` from the same layout (`python3 _generate_collection.py`) |

## 🚀 **Quick Start**

1. **Import**: Postman → Import → both JSON files
2. **Environment**: Set `EXO_AUTH_KEY`, `EXO_AUTH_TOKEN`, `EXO_API_DOMAIN`, `EXO_ACCOUNT_SID`
3. **Run Setup folder** in order (starts with **1. Trunk Creation**); use **6. Create SIP credentials** for Voice AI / Streamkit-style digest auth
4. **Manage and view**: list/update/delete trunks, credentials, whitelist, destinations, DIDs, settings — set `WHITELIST_ENTRY_ID`, `DESTINATION_ID`, `PHONE_MAPPING_ID`, `CREDENTIAL_ID` from prior responses as needed

## ✨ **Features**

- **Two top-level folders**: Setup vs Manage and view (with subfolders per resource)
- **Basic Auth** on the collection (Bearer also supported by the API where enabled) — see [SIP Trunking APIs](https://developer.exotel.com/api/sip-trunking-apis)
- **Auto-save** where tests extract IDs (`TRUNK_SID`, `CREDENTIAL_ID`, etc.)
- **SIP outbound / Streamkit-oriented** descriptions on credential and setup requests

## 📚 **Documentation**

👉 **[POSTMAN_GUIDE.md](POSTMAN_GUIDE.md)** — full setup and troubleshooting  
👉 **[SIP Trunking APIs (official)](https://developer.exotel.com/api/sip-trunking-apis)**

## 🔗 **Links**

- **India** — [API credentials](https://my.in.exotel.com/apisettings/site#api-credentials), [numbers](https://my.in.exotel.com/numbers)
- **Global** — [API credentials](https://my.exotel.com/apisettings/site#api-credentials), [numbers](https://my.exotel.com/numbers)
