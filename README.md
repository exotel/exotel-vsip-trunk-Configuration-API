# Exotel SIP Trunking APIs

Sample clients for Exotel **vSIP / SIP trunking** HTTP APIs. Use **`curl/`** (bash), **`python/`**, **`go/`**, or **`postman/`** — pick one workflow and ignore the rest.

Official reference: [SIP Trunking APIs (developer.exotel.com)](https://developer.exotel.com/api/sip-trunking-apis)

---

## Repository layout

| Folder | What it is |
|--------|------------|
| [`curl/`](curl/) | Bash scripts; PSTN setup, manage/view, SIP digest credentials |
| [`python/`](python/) | Python 3 samples using shared `_client.py` |
| [`go/`](go/) | Go samples; `exotel_client.go` plus one `*.go` per operation |
| [`postman/`](postman/) | Postman collection + environment + import guide |

Configuration template: copy **`.env.example`** → **`.env`** in the repo root (used by Python, Go, and the newer curl scripts that reference `EXO_*` variables).

---

## API host vs dashboard

| Account | Dashboard | API hostname (`EXO_API_DOMAIN`) |
|---------|-----------|-----------------------------------|
| India | [my.in.exotel.com](https://my.in.exotel.com) | `api.in.exotel.com` |
| Global | [my.exotel.com](https://my.exotel.com) | `api.exotel.com` |

Use the API host that matches where the account was created.

---

## Quick start

### Environment (Python / Go / credential curl scripts)

```bash
cp .env.example .env
# Edit .env: EXO_AUTH_KEY, EXO_AUTH_TOKEN, EXO_ACCOUNT_SID, EXO_API_DOMAIN
```

### curl

See [`curl/README.md`](curl/README.md). Older PSTN scripts use `curl/env.example.txt` (`API_KEY`, `SUBDOMAIN`, …). Scripts under `curl/` that call SIP credentials / list endpoints expect the **`EXO_*`** variables from the root `.env`.

### Python

From the repository root (so `python/` can import `_client.py`):

```bash
cd python
python3 list_trunks.py
```

### Go

From the `go/` directory, pass **`exotel_client.go`** together with the script you want:

```bash
cd go
go run exotel_client.go list_trunks.go
```

### Postman

Import `postman/Exotel_vSIP_API_Collection.json` and `postman/Exotel_vSIP_Environment.json`, set environment variables, then run requests. Details: [`postman/POSTMAN_GUIDE.md`](postman/POSTMAN_GUIDE.md).

---

## SIP digest credentials (optional)

For Voice AI / dynamic source IPs, use `POST/GET/PUT/DELETE` on `.../trunks/{trunk_sid}/credentials`. See the **official API docs** linked above.

---

## Authentication

| Setting | Value |
|---------|-------|
| Base URL | `https://<EXO_API_DOMAIN>` |
| Auth | HTTP Basic (`<api_key>:<api_token>`) |
| Content-Type | `application/json` |
| Rate limit | 200 requests/minute (typical) |

---

## Support

- **Documentation:** [developer.exotel.com](https://developer.exotel.com)
- **Email:** support@exotel.com
