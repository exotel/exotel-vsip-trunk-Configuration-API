# Exotel SIP Trunking - curl Scripts

Ready-to-use bash scripts for all SIP Trunking API operations.

---

## Setup

1. Copy the environment template:
   ```bash
   cp env.example.txt .env
   ```

2. Edit `.env` with your credentials:
   ```bash
   API_KEY="your_api_key"
   API_TOKEN="your_api_token"
   ACCOUNT_SID="your_account_sid"
   ```

3. Make scripts executable:
   ```bash
   chmod +x *.sh
   ```

---

## Scripts

### PSTN Setup (Standard Calls)

| Order | Script | Description |
|-------|--------|-------------|
| 1 | `create_trunk.sh` | Create a new SIP trunk |
| 2 | `map_did.sh` | Map phone number to trunk |
| 3 | `whitelist_ip.sh` | Whitelist your server IP (for Outbound) |
| 4 | `add_destination.sh` | Add destination URI (for Inbound) |
| 5 | `set_trunk_alias.sh` | Set outbound caller ID (optional) |

### StreamKit Setup (Voice AI)

For StreamKit, run scripts in this order with `MODE=flow`:

```bash
# Step 1: Create trunk
./create_trunk.sh

# Step 2: Map phone number with flow mode
MODE=flow ./map_did.sh

# Step 3: Whitelist IP
./whitelist_ip.sh
```

### View & Manage

| Script | Description |
|--------|-------------|
| `get_phone_numbers.sh` | List mapped phone numbers |
| `get_whitelisted_ips.sh` | List whitelisted IPs |
| `get_destination_uris.sh` | List destination URIs |
| `update_phone_number.sh` | Switch mode (pstn ↔ flow) |
| `delete_trunk.sh` | Delete trunk (⚠️ permanent!) |

---

## Usage Examples

### PSTN Setup (Outbound + Inbound)

```bash
# 1. Create trunk
./create_trunk.sh
# → Save TRUNK_SID to .env

# 2. Map phone number
PHONE_NUMBER="+919876543210" ./map_did.sh
# → Save PHONE_NUMBER_ID to .env

# 3. Whitelist your server IP
SERVER_IP="your.server.ip" ./whitelist_ip.sh

# 4. Add destination for inbound calls
DESTINATION="your.server.ip" ./add_destination.sh
```

### StreamKit Setup (Voice AI)

```bash
# 1. Create trunk
./create_trunk.sh
# → Save TRUNK_SID to .env

# 2. Map phone number with flow mode
MODE=flow PHONE_NUMBER="+919876543210" ./map_did.sh

# 3. Whitelist your server IP
SERVER_IP="your.server.ip" ./whitelist_ip.sh
```

### Switch Mode (pstn ↔ flow)

```bash
# Switch to flow mode
MODE=flow ./update_phone_number.sh

# Switch back to pstn mode
MODE=pstn ./update_phone_number.sh
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | Yes | API Key from Exotel Dashboard |
| `API_TOKEN` | Yes | API Token from Exotel Dashboard |
| `ACCOUNT_SID` | Yes | Account SID from Exotel Dashboard |
| `TRUNK_SID` | After create_trunk | Trunk SID from create response |
| `PHONE_NUMBER` | For map_did | Phone number in E.164 format |
| `PHONE_NUMBER_ID` | For update_phone_number | Numeric ID from map response |
| `SERVER_IP` | For whitelist_ip | Your server's public IP |
| `DESTINATION` | For add_destination | IP or FQDN for inbound routing |
| `MODE` | Optional | `pstn` (default) or `flow` |

---

## Notes

- **Order matters**: Run scripts in the order shown above
- **Whitelist first**: For IP destinations, whitelist the IP before adding as destination
- **FQDNs**: Don't need whitelisting for destination URIs
- **Phone Number ID**: The numeric ID (e.g., `41523`) from map_did response, NOT the phone number itself
