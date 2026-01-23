# Exotel SIP Trunking Guide

Understanding SIP Trunking and Voice connectivity.

---

## What is SIP Trunking?

SIP (Session Initiation Protocol) Trunking delivers voice services over the internet. It replaces traditional phone lines (PRI/ISDN) with a virtual connection.

A SIP Trunk connects your PBX, Contact Center, or SBC to the telephone network (PSTN) through Exotel.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  YOUR SYSTEM    │       │     EXOTEL      │       │      PSTN       │
│                 │       │                 │       │                 │
│  - PBX          │       │  - SIP Gateway  │       │  - Mobile       │
│  - Contact      │  SIP  │  - Media Server │       │  - Landline     │
│    Center       │<----->│  - Routing      │<----->│  - International│
│  - SBC          │       │                 │       │                 │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

---

## Call Directions

### Outbound / Termination

Your system makes calls to phone numbers.

```
YOUR SYSTEM ──> EXOTEL ──> PSTN ──> CUSTOMER PHONE
```

- Calls originate from your PBX/Contact Center
- Exotel routes to the telephone network
- Requires Map ACL (IP whitelisting)
- Uses `mode: "pstn"`

### Inbound / Origination

Your system receives calls from phone numbers.

```
CUSTOMER PHONE ──> PSTN ──> EXOTEL ──> YOUR SYSTEM
```

- Customer dials your number
- Exotel routes to your server
- Supports IP or FQDN destination
- Requires Map Destination URI

### StreamKit

Your system connects to Voice AI bots via WebSocket.

```
YOUR SYSTEM ──> EXOTEL ──> VOICE AI BOT (WebSocket) configured in App Bazaar flow with VoiceBot Applet
```

- Calls route to AI voicebot
- Real-time audio streaming
- Requires Map ACL (IP whitelisting)
- Uses `mode: "flow"`

---

## Mode Parameter

The `mode` parameter in Map Phone Number API determines call routing:

| Mode | Description | Use Case |
|------|-------------|----------|
| `pstn` | Routes to telephone network | Standard outbound calls |
| `flow` | Routes to Voice AI platform | StreamKit, voicebot integration |

---

## Connectivity Requirements

| Use Case | Static IP | FQDN |
|----------|-----------|------|
| Outbound / Termination | Required (Map ACL) | Not supported |
| Inbound / Origination | Supported | Supported |
| StreamKit | Required (Map ACL) | Not supported |

---

## Setup Flow Summary

### PSTN (Outbound + Inbound)

```
1. Create Trunk
2. Map Phone Number to Trunk
3. Map ACL to Trunk (for Outbound - whitelist your server IP)
4. Map Destination URI to Trunk (for Inbound - your server endpoint)
```

### StreamKit (Voice AI)

```
1. Create Trunk
2. Map Phone Number to Trunk (mode: flow)
3. Map ACL to Trunk (whitelist your server IP)
```
Firewall allows SIP + RTP from Exotel
---

## StreamKit Overview

StreamKit is a cloud-native SIP-to-WebSocket connector for Voice AI integration.

**Features:**
- Real-time SIP to WebSocket streaming
- Connect contact center to AI voicebots
- Multi-bot routing per trunk
- Agent escalation support

**Use Cases:**
- AI-powered IVR systems
- Voice bot customer service
- Real-time speech analytics
- Agent assist with AI suggestions

**How it differs from standard termination:**
- Standard: Calls go to PSTN (phone network)
- StreamKit: Calls go to Voice AI platform

Learn more: https://exotel.com/products/streamkit-cloud-connector/

https://docs.exotel.com/exotel-agentstream/streamkit-cloud

---

## SIP Response Codes

### Success

| Code | Description |
|------|-------------|
| 100 | Trying |
| 180 | Ringing |
| 200 | OK (Connected) |

### Client Errors

| Code | Description | Solution |
|------|-------------|----------|
| 401 | Unauthorized | Check SIP credentials |
| 403 | Forbidden | Map ACL (whitelist your IP) |
| 404 | Not Found | Check phone number format |
| 486 | Busy | User on another call |

### Server Errors

| Code | Description | Solution |
|------|-------------|----------|
| 500 | Server Error | Contact support |
| 503 | Unavailable | Retry later |

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 403 on calls | IP not in ACL | Use Map ACL API to whitelist IP |
| 404 on calls | Invalid number | Use E.164 format (+919876543210) |
| No inbound calls | Missing destination | Use Map Destination URI API (map ACL first for IP!) |
| "Destination not whitelisted" | IP not in ACL | Map ACL before mapping as destination |
| One-way audio | Firewall blocking RTP | Open UDP 10000-20000 |
| HTTP 415 error | Wrong content type | Use `Content-Type: application/json` |
| Duplicate resource error | Already exists | Use different name/IP or delete existing |

---

## PBX Configuration

After completing API setup, configure your PBX:

| Setting | Value |
|---------|-------|
| SIP Server | `<your_account_sid>.pstn.exotel.com` |
| Port | 5070 (TCP) or 443 (TLS) |
| Username | `trunk_sid` from Create Trunk response |
| Transport | TCP or TLS |

> **Note:** Ensure your server IP is mapped to ACL (whitelisted) before attempting to connect.

---

## API Reference

For detailed API documentation with request/response examples, see [API Reference](API_REFERENCE.md).

| API | Purpose |
|-----|---------|
| Create Trunk | Create new SIP trunk |
| Map Phone Number | Associate phone number with trunk |
| Map ACL | Whitelist IP for authentication |
| Map Destination URI | Configure inbound routing |
| Update Phone Number Mode | Switch between pstn and flow modes |
| Set Trunk Alias | Set outbound caller ID |
| Delete Trunk | Remove trunk and all configurations |

---

##Rule of Thumb

• Outbound (SIP → PSTN): Always whitelist your source IP
• Inbound (PSTN → SIP):
  – Using FQDN destination → No whitelist required
  – Using IP destination → Destination IP must be allowlisted
• StreamKit: Always whitelist your source IP

## Support

- Documentation: https://developer.exotel.com
- StreamKit: https://exotel.com/products/streamkit-cloud-connector/
- Email: support@exotel.com
