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
- Requires static IP whitelisting
- Uses `mode: "pstn"`

### Inbound / Origination

Your system receives calls from phone numbers.

```
CUSTOMER PHONE ──> PSTN ──> EXOTEL ──> YOUR SYSTEM
```

- Customer dials your number
- Exotel routes to your server
- Supports IP or FQDN destination

### StreamKit

Your system connects to Voice AI bots via WebSocket.

```
YOUR SYSTEM ──> EXOTEL ──> VOICE AI BOT (WebSocket) configured in App Bazaar flow with VoiceBot Applet
```

- Calls route to AI voicebot
- Real-time audio streaming
- Requires static IP whitelisting
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
| Outbound / Termination | Required | Not supported |
| Inbound / Origination | Supported | Supported |
| StreamKit | Required | Not supported |

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
| 403 | Forbidden | Whitelist your IP |
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
| 401 on registration | Wrong credentials | Get credentials via API |
| 403 on calls | IP not whitelisted | Add IP via Whitelist API |
| 404 on calls | Invalid number | Use E.164 format |
| No inbound calls | Missing destination | Add destination URI |
| One-way audio | Firewall | Open UDP 10000-20000 |

---

## PBX Configuration

After completing API setup, configure your PBX:

| Setting | Value |
|---------|-------|
| SIP Server | `<your_sid>.pstn.exotel.com` |
| Port | 5060 (TCP) or 5061 (TLS) |
| Username | `trunk_sid` from Create Trunk |
| Password | From Get Credentials API |
| Transport | TCP or TLS |

---

## Support

- Documentation: https://developer.exotel.com
- StreamKit: https://exotel.com/products/streamkit-cloud-connector/
- Email: support@exotel.com
