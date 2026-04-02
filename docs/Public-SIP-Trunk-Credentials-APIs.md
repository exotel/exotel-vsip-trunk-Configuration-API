# Public SIP trunk credentials (customer API)

These endpoints configure **SIP digest credentials** on an Exotel **vSIP / SIP outbound** trunk. They are the usual choice for **cloud Voice AI** and **Streamkit-style** integrations where **source IPs are dynamic**, so IP-only ACLs are impractical. The same Subscribix `v2/accounts/...` API also supports **whitelisted IPs** for fixed SBC/PBX egress (see below).

**Related:** Postman collection folders **Setup — SIP outbound trunk** (create) and **Manage and view → SIP credentials** (list/update/delete). Multi-language samples: `create_credentials.*`, `list_credentials.*`, etc.

---

## When to use Credentials vs ACL (Whitelisted IPs)

Use these guidelines to decide whether you should configure **credentials**, **ACL (whitelisted IPs)**, or **both** on a trunk.

### Credentials (SIP Digest) — recommended for Voice AI direct trunking

Use **credentials** when your SIP endpoint is a **cloud Voice AI platform** (or any environment where source IPs are dynamic/unknown), and you want to **avoid managing IP allowlists**.

- **Best for**: Voice AI direct trunking, dynamic SBCs, multi-tenant provider networks.
- **Typical choice**: **Credentials-only** (skip ACL whitelisting) when IPs are not stable.

### ACL (Whitelisted IPs) — recommended for static enterprise PBX/SBC

Use **ACL-only** when your trunk connects to a customer-controlled PBX/SBC with **stable, known egress IPs**.

- **Best for**: On‑prem SBCs, fixed datacenter IPs, tightly controlled networks.
- **Typical choice**: **ACL-only** if credentials are not required and IPs are stable.

### Combination (ACL + Credentials) — highest security when IPs are stable

Use **both** when you have credentials *and* stable IPs and want a stricter security posture.

- **Best for**: Production trunks with fixed IP ranges and stricter access controls.
- **Why**: Reduces blast radius—credentials alone aren’t sufficient without also matching the allowlist (and vice‑versa).

---

## Authentication

All credential routes accept the same auth as other vSIP APIs:

- **HTTP Basic:** `https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/...` or `Authorization: Basic` with base64(`API_KEY:API_TOKEN`).
- **Bearer:** `Authorization: Bearer <token>` (when enabled for your account).

---

### 1. Create credentials (SIP digest)

Creates a **username/password** pair for **SIP Digest authentication** on the trunk. Configure the same values on your Voice AI platform’s SIP trunk settings.

#### HTTP Request

POST `https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials`

#### Request Headers

| Header | Value |
| --- | --- |
| Content-Type | application/json |

#### Request Parameters

The following parameters are sent as JSON in the body of the request:

| Parameter Name | Mandatory/Optional | Value |
| --- | --- | --- |
| user_name | Mandatory | String; SIP digest username. Example: `voice_ai_user` |
| password | Mandatory | String; SIP digest password. Use a strong secret. |
| friendly_name | Optional | String; Label to identify where the creds are used (max 32 chars). Example: `elevenlabs-prod`, `livekit-staging` |

#### Example Request

```bash
curl -s -X POST "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "voice_ai_user",
    "password": "REPLACE_WITH_STRONG_PASSWORD",
    "friendly_name": "voice_ai_platform"
  }'
```

#### HTTP Response

On success, the HTTP response status code will be **200 OK**.

#### Example Response

```json
{
  "request_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "method": "POST",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "id": "1234",
      "trunk_sid": "trmum1exampleonly000000000000",
      "user_name": "voice_ai_user",
      "friendly_name": "voice_ai_platform",
      "date_created": "2026-01-23T11:37:36Z",
      "date_updated": "2026-01-23T11:37:36Z"
    }
  }
}
```

#### Response Parameters

| Parameter Name | Type & Value |
| --- | --- |
| request_id | String; Unique identifier for this API request |
| method | String; HTTP method used (POST) |
| http_code | Integer; HTTP status code (200 for success) |
| id | String; Unique identifier for this credential entry. Example: `1234` |
| trunk_sid | String; The trunk these credentials are associated with |
| user_name | String; The SIP digest username you set |
| friendly_name | String or null; Optional label |
| date_created | String; ISO 8601 timestamp when credentials were created |
| date_updated | String; ISO 8601 timestamp when credentials were last updated |

---

### 2. List credentials (verify)

Lists credentials configured for the trunk (or fetches one row if `id` is set).

#### HTTP Request

GET `https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials`

#### Query parameters (optional)

| Parameter   | Description |
| ----------- | ----------- |
| `page_size` | Page size; default and maximum are enforced by the server. |
| `offset`    | Offset for pagination (default `0`). |
| `id`        | If set, returns the matching credential row. |

#### Example Request

```bash
curl -s "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials"
```

```bash
curl -s "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials?page_size=50&offset=0"
```

#### HTTP Response

On success, the HTTP response status code will be **200 OK**.

#### Example Response

```json
{
  "request_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "method": "GET",
  "http_code": 200,
  "metadata": {
    "total": 1,
    "page_size": 50,
    "page": 1,
    "first_page_uri": "/v2/accounts/exotelacct1/trunks/trmum1exampleonly000000000000/credentials?page_size=50&offset=0",
    "prev_page_uri": null,
    "next_page_uri": null
  },
  "response": [
    {
      "code": 200,
      "error_data": null,
      "status": "success",
      "data": {
        "id": "1234",
        "trunk_sid": "trmum1exampleonly000000000000",
        "user_name": "voice_ai_user",
        "friendly_name": "voice_ai_platform",
        "date_created": "2026-01-23T11:37:36Z",
        "date_updated": "2026-01-23T11:37:36Z"
      }
    }
  ]
}
```

#### Response Parameters

| Parameter Name | Type & Value |
| --- | --- |
| request_id | String; Unique identifier for this API request |
| method | String; HTTP method used (GET) |
| http_code | Integer; HTTP status code (200 for success) |
| metadata.total | Integer; Total credential records available |
| metadata.page_size | Integer; Page size applied |
| metadata.page | Integer; Page number (if present) |
| metadata.first_page_uri | String; URI for first page |
| metadata.prev_page_uri | String or null; URI for previous page |
| metadata.next_page_uri | String or null; URI for next page |
| response | Array; List of credential objects |
| response[].data.id | String; Unique identifier for the credential entry |
| response[].data.trunk_sid | String; The trunk these credentials are associated with |
| response[].data.user_name | String; SIP digest username |
| response[].data.friendly_name | String or null; Optional label |
| response[].data.date_created | String; ISO 8601 timestamp when created |
| response[].data.date_updated | String; ISO 8601 timestamp when updated |

---

### 3. Delete credentials (rotate / revoke)

Deletes a credential entry when rotating credentials or removing access for a provider environment.

#### HTTP Request

DELETE `https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials?id=<CREDENTIAL_ID>`

**Important:** credential id is passed as **query param** `id` (not `/credentials/<CREDENTIAL_ID>`). The path form `/credentials/<CREDENTIAL_ID>` is used for **PUT (update)**, not for DELETE.

#### Example Request

```bash
curl -s -X DELETE "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials?id=<CREDENTIAL_ID>"
```

#### HTTP Response

On success, the HTTP response status code will be **200 OK**.

#### Example Response

```json
{
  "request_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "method": "DELETE",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "id": "1234",
      "trunk_sid": "trmum1exampleonly000000000000",
      "user_name": "voice_ai_user",
      "friendly_name": "voice_ai_platform",
      "date_created": "2026-01-23T11:37:36Z",
      "date_updated": "2026-01-23T11:37:36Z"
    }
  }
}
```

#### Response Parameters

| Parameter Name | Type & Value |
| --- | --- |
| request_id | String; Unique identifier for this API request |
| method | String; HTTP method used (DELETE) |
| http_code | Integer; HTTP status code (200 for success) |
| id | String; Deleted credential identifier |
| trunk_sid | String; Trunk SID this credential belonged to |
| user_name | String; SIP digest username that was deleted |
| friendly_name | String or null; Optional label |
| date_created | String; ISO 8601 timestamp when credential was originally created |
| date_updated | String; ISO 8601 timestamp when credential was last updated |

---

### 4. Update credentials

Updates an existing credential (e.g. rotate password or change label). Uses the **path** segment for the credential id.

#### HTTP Request

PUT `https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials/<CREDENTIAL_ID>`

#### Request body (JSON)

All fields are optional; include only what you want to change.

| Field           | Description |
| --------------- | ----------- |
| `user_name`     | New SIP digest username. |
| `password`      | New SIP digest password. |
| `friendly_name` | Label (max 32 characters). |

#### Example Request

```bash
curl -s -X PUT "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials/<CREDENTIAL_ID>" \
  -H "Content-Type: application/json" \
  -d '{"friendly_name":"prod_voice_ai"}'
```

On success, the API returns **200 OK** with a body in the same family as the create response (`response.data` with credential fields; passwords are not echoed).

