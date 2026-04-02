#!/usr/bin/env python3
"""Generate Exotel_vSIP_API_Collection.json — layout matches Postman workspace format:
   1. GETTING STARTED (PSTN)  2. STREAMKIT (Voice AI)  3. MANAGE & VIEW
   Run: python3 _generate_collection.py
"""
import json
from pathlib import Path

HOST = "{{EXO_API_DOMAIN}}"
ACC = "{{EXO_ACCOUNT_SID}}"
BASE_PATH = ["v2", "accounts", ACC]

def url(path_segments, query=None):
    path_join = "/".join(path_segments)
    raw = f"https://{HOST}/{path_join}"
    qlist = None
    if query:
        qstr = "&".join(f"{k}={v}" for k, v in query.items())
        raw += "?" + qstr
        qlist = [{"key": k, "value": str(v)} for k, v in query.items()]
    u = {
        "raw": raw,
        "protocol": "https",
        "host": [HOST],
        "path": path_segments,
    }
    if qlist:
        u["query"] = qlist
    return u

def req(method, path_segments, body=None, query=None, desc=""):
    h = []
    if body is not None and method not in ("GET", "DELETE"):
        h.append({"key": "Content-Type", "value": "application/json"})
    u = url(path_segments, query)
    r = {"method": method, "header": h, "url": u, "description": desc}
    if body is not None:
        r["body"] = {"mode": "raw", "raw": body}
    return r

def tests_trunk_create():
    return [{
        "listen": "test",
        "script": {
            "type": "text/javascript",
            "exec": [
                "pm.test(\"Status 200\", () => pm.response.to.have.status(200));",
                "const j = pm.response.json();",
                "pm.test(\"success\", () => pm.expect(j.response.status).to.eql(\"success\"));",
                "if (j.response.status === \"success\" && j.response.data) {",
                "  pm.environment.set(\"TRUNK_SID\", j.response.data.trunk_sid);",
                "  console.log(\"✅ TRUNK_SID=\" + j.response.data.trunk_sid);",
                "}",
            ],
        },
    }]

def tests_whitelist_post():
    return [{
        "listen": "test",
        "script": {
            "type": "text/javascript",
            "exec": [
                "pm.test(\"Status 200\", () => pm.response.to.have.status(200));",
                "const j = pm.response.json();",
                "if (j.response && j.response.status === \"success\" && j.response.data && j.response.data.id) {",
                "  pm.environment.set(\"WHITELIST_ENTRY_ID\", j.response.data.id);",
                "}",
            ],
        },
    }]

def tests_dest_post():
    return [{
        "listen": "test",
        "script": {
            "type": "text/javascript",
            "exec": [
                "pm.test(\"Status 200\", () => pm.response.to.have.status(200));",
                "const j = pm.response.json();",
                "if (j.response && j.response[0] && j.response[0].status === \"success\" && j.response[0].data) {",
                "  pm.environment.set(\"DESTINATION_ID\", j.response[0].data.id);",
                "}",
            ],
        },
    }]

def tests_did_post():
    return [{
        "listen": "test",
        "script": {
            "type": "text/javascript",
            "exec": [
                "pm.test(\"Status 200\", () => pm.response.to.have.status(200));",
                "const j = pm.response.json();",
                "if (j.response && j.response.status === \"success\" && j.response.data && j.response.data.id) {",
                "  pm.environment.set(\"PHONE_MAPPING_ID\", j.response.data.id);",
                "}",
            ],
        },
    }]

def tests_cred_create():
    return [{
        "listen": "test",
        "script": {
            "type": "text/javascript",
            "exec": [
                "pm.test(\"Status 200\", () => pm.response.to.have.status(200));",
                "const j = pm.response.json();",
                "if (j.response && j.response.data && j.response.data.id) {",
                "  pm.environment.set(\"CREDENTIAL_ID\", j.response.data.id);",
                "}",
            ],
        },
    }]

def tests_basic():
    return [{
        "listen": "test",
        "script": {
            "type": "text/javascript",
            "exec": [
                "pm.test(\"Status 200\", () => pm.response.to.have.status(200));",
                "const j = pm.response.json();",
                "pm.test(\"Has response\", () => pm.expect(j).to.have.property(\"response\"));",
            ],
        },
    }]

def tests_alias_post():
    return [{
        "listen": "test",
        "script": {
            "type": "text/javascript",
            "exec": [
                "pm.test(\"Status 200\", () => pm.response.to.have.status(200));",
                "const j = pm.response.json();",
                "pm.test(\"response array\", () => pm.expect(j.response).to.be.an(\"array\"));",
            ],
        },
    }]

def item(name, request, events=None):
    o = {"name": name, "request": request}
    if events:
        o["event"] = events
    return o

CREATE_TRUNK_BODY = (
    '{\n  "trunk_name": "{{TRUNK_NAME}}",\n  "nso_code": "{{NSO_CODE}}",\n'
    '  "domain_name": "{{EXO_ACCOUNT_SID}}.pstn.exotel.com"\n}'
)

# --- 1. GETTING STARTED (PSTN) ---
folder_pstn = {
    "name": "1. GETTING STARTED (PSTN)",
    "description": "Blueprint workflow for **PSTN / SIP outbound** trunking. Run steps in order. Uses `mode: pstn` for DID mapping.",
    "item": [
        item(
            "POST Step 1: Create Trunk",
            req("POST", BASE_PATH + ["trunks"], CREATE_TRUNK_BODY,
                desc="Creates the vSIP trunk. Saves **`TRUNK_SID`** to the active environment."),
            tests_trunk_create(),
        ),
        item(
            "POST Step 2: Map Phone Number to Trunk",
            req(
                "POST",
                BASE_PATH + ["trunks", "{{TRUNK_SID}}", "phone-numbers"],
                '{\n  "phone_number": "{{DID_NUMBER}}",\n  "mode": "pstn"\n}',
                desc="Maps your Exophone (E.164) to the trunk in **pstn** mode. Saves **`PHONE_MAPPING_ID`** when returned.",
            ),
            tests_did_post(),
        ),
        item(
            "POST Step 3(a): Map ACL to Trunk (Whitelist IP)",
            req(
                "POST",
                BASE_PATH + ["trunks", "{{TRUNK_SID}}", "whitelisted-ips"],
                '{\n  "ip": "{{WHITELIST_IP}}",\n  "mask": {{WHITELIST_MASK}}\n}',
                desc="Use **ACL / whitelisted IPs** when your SIP infrastructure has **stable, known egress IPs** (enterprise SBC/PBX).\n\nIf your provider/platform has **dynamic IPs** (cloud Voice AI), also do **Step 3(b)**. Saves **`WHITELIST_ENTRY_ID`** when returned.",
            ),
            tests_whitelist_post(),
        ),
        item(
            "POST Step 3(b): Create SIP Credentials (Digest Auth)",
            req(
                "POST",
                BASE_PATH + ["trunks", "{{TRUNK_SID}}", "credentials"],
                '{\n  "user_name": "{{SIP_CRED_USERNAME}}",\n  "password": "{{SIP_CRED_PASSWORD}}",\n  "friendly_name": "{{SIP_CRED_FRIENDLY_NAME}}"\n}',
                desc="Use **SIP digest credentials** when source IPs are **dynamic/unknown** (cloud Voice AI / Streamkit-style). This avoids managing IP allowlists.\n\nYou can use **ACL-only**, **credentials-only**, or **both** (best security when IPs are stable). Saves **`CREDENTIAL_ID`**. DELETE uses query `?id=`; PUT uses path `/credentials/{{CREDENTIAL_ID}}`.",
            ),
            tests_cred_create(),
        ),
        item(
            "POST Step 4: Map Destination URI to Trunk",
            req(
                "POST",
                BASE_PATH + ["trunks", "{{TRUNK_SID}}", "destination-uris"],
                '{\n  "destinations": [\n    {\n      "destination": "{{TRUNK_DEST_IP}}:{{TRUNK_DEST_PORT}}"\n    }\n  ]\n}',
                desc="Default **UDP** SIP destination (`IP:port`). For TCP use `;transport=tcp`, for TLS use `;transport=tls` on the destination string. Saves **`DESTINATION_ID`**.",
            ),
            tests_dest_post(),
        ),
    ],
}

# --- 2. STREAMKIT (Voice AI) ---
folder_streamkit = {
    "name": "2. STREAMKIT (Voice AI)",
    "description": "Workflow for **Voice AI / Streamkit**-style setups: Exophone in **flow** mode, ACL, then **SIP digest credentials** for dynamic source IPs.",
    "item": [
        item(
            "POST Step 1: Create Trunk",
            req("POST", BASE_PATH + ["trunks"], CREATE_TRUNK_BODY,
                desc="Same as PSTN — creates trunk and saves **`TRUNK_SID`**."),
            tests_trunk_create(),
        ),
        item(
            "POST Step 2: Map Phone Number (Flow Mode)",
            req(
                "POST",
                BASE_PATH + ["trunks", "{{TRUNK_SID}}", "phone-numbers"],
                '{\n  "phone_number": "{{DID_NUMBER}}",\n  "mode": "flow"\n}',
                desc="Maps the virtual number in **flow** mode (Exotel App / Flow). Saves **`PHONE_MAPPING_ID`** when returned.",
            ),
            tests_did_post(),
        ),
        item(
            "POST Step 3(a): Map ACL to Trunk",
            req(
                "POST",
                BASE_PATH + ["trunks", "{{TRUNK_SID}}", "whitelisted-ips"],
                '{\n  "ip": "{{WHITELIST_IP}}",\n  "mask": {{WHITELIST_MASK}}\n}',
                desc="Use **ACL / whitelisted IPs** when your SIP infrastructure has **stable, known egress IPs**. If your Voice AI platform has **dynamic IPs**, do **Step 3(b)**.\n\nSaves **`WHITELIST_ENTRY_ID`** when returned.",
            ),
            tests_whitelist_post(),
        ),
        item(
            "POST Step 3(b): Create SIP Credentials (Digest Auth)",
            req(
                "POST",
                BASE_PATH + ["trunks", "{{TRUNK_SID}}", "credentials"],
                '{\n  "user_name": "{{SIP_CRED_USERNAME}}",\n  "password": "{{SIP_CRED_PASSWORD}}",\n  "friendly_name": "{{SIP_CRED_FRIENDLY_NAME}}"\n}',
                desc="Use **SIP digest credentials** when source IPs are **dynamic/unknown** (common for cloud Voice AI / Streamkit-style). Configure the same values on your Voice AI SIP trunk.\n\nYou can use **ACL-only**, **credentials-only**, or **both**. Saves **`CREDENTIAL_ID`**. **DELETE** credential: query `?id=`; **PUT** update: path `/credentials/{{CREDENTIAL_ID}}`.",
            ),
            tests_cred_create(),
        ),
        item(
            "POST Step 4: Map Destination URI to Trunk",
            req(
                "POST",
                BASE_PATH + ["trunks", "{{TRUNK_SID}}", "destination-uris"],
                '{\n  "destinations": [\n    {\n      "destination": "{{TRUNK_DEST_IP}}:{{TRUNK_DEST_PORT}}"\n    }\n  ]\n}',
                desc="Default **UDP** SIP destination (`IP:port`). For TCP use `;transport=tcp`, for TLS use `;transport=tls` on the destination string. Saves **`DESTINATION_ID`**.",
            ),
            tests_dest_post(),
        ),
    ],
}

# --- 3. MANAGE & VIEW --- (flat list: screenshot order + extra applicable APIs)
manage_items = [
    item(
        "GET Get Phone Numbers",
        req("GET", BASE_PATH + ["trunks", "{{TRUNK_SID}}", "phone-numbers"],
            desc="List DID ↔ trunk mappings for this trunk."),
        tests_basic(),
    ),
    item(
        "GET Get ACLs (Whitelisted IPs)",
        req("GET", BASE_PATH + ["trunks", "{{TRUNK_SID}}", "whitelisted-ips"],
            desc="List IP whitelist entries."),
        tests_basic(),
    ),
    item(
        "GET Get Destination URIs",
        req("GET", BASE_PATH + ["trunks", "{{TRUNK_SID}}", "destination-uris"],
            desc="List configured SIP destination URIs."),
        tests_basic(),
    ),
    item(
        "PUT Update Phone Number Mode",
        req(
            "PUT",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "phone-numbers", "{{PHONE_MAPPING_ID}}"],
            '{\n  "phone_number": "{{DID_NUMBER}}",\n  "mode": "{{PHONE_MODE}}"\n}',
            desc="Switch mapping **`mode`** between `pstn` and `flow`. Set env **`PHONE_MODE`** (default `pstn`). Requires **`PHONE_MAPPING_ID`** from a create step.",
        ),
        tests_basic(),
    ),
    item(
        "POST Set Trunk Alias (Caller ID)",
        req(
            "POST",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "settings"],
            '{\n  "settings": [\n    {\n      "name": "trunk_external_alias",\n      "value": "{{EXOPHONE}}"\n    }\n  ]\n}',
            desc="Sets **`trunk_external_alias`** (caller ID / external alias).",
        ),
        tests_alias_post(),
    ),
    item(
        "DEL Delete Trunk",
        req(
            "DELETE",
            BASE_PATH + ["trunks"],
            desc="**Destructive.** Query param **`trunk_sid`** required.",
            query={"trunk_sid": "{{TRUNK_SID}}"},
        ),
        tests_basic(),
    ),
    # --- Additional customer APIs (same folder) ---
    item(
        "GET List Trunks",
        req(
            "GET",
            BASE_PATH + ["trunks"],
            desc="Paginated trunk list. Query: `page_size`, `offset`, optional `trunk_sid`.",
            query={"page_size": "{{PAGE_SIZE}}", "offset": "{{PAGE_OFFSET}}"},
        ),
        tests_basic(),
    ),
    item(
        "GET Trunk Map Lookup (Exophone)",
        req(
            "GET",
            BASE_PATH + ["trunk-maps"],
            desc="Resolve which trunk a virtual number maps to. Query **`exophone`** (required).",
            query={"exophone": "{{DID_NUMBER}}", "trunk_sid": "{{TRUNK_SID}}"},
        ),
        tests_basic(),
    ),
    item(
        "GET List SIP Credentials",
        req(
            "GET",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "credentials"],
            desc="Optional query: `page_size`, `offset`, or `id` for one row.",
            query={"page_size": "{{PAGE_SIZE}}", "offset": "{{PAGE_OFFSET}}"},
        ),
        tests_basic(),
    ),
    item(
        "PUT Update SIP Credential",
        req(
            "PUT",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "credentials", "{{CREDENTIAL_ID}}"],
            '{\n  "friendly_name": "{{SIP_CRED_FRIENDLY_NAME}}"\n}',
            desc="Path includes credential id. Body may include `user_name`, `password`, `friendly_name`.",
        ),
        tests_basic(),
    ),
    item(
        "DEL Delete SIP Credential",
        req(
            "DELETE",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "credentials"],
            desc="**Query `id`** (not path).",
            query={"id": "{{CREDENTIAL_ID}}"},
        ),
        tests_basic(),
    ),
    item(
        "PUT Update Whitelisted IP",
        req(
            "PUT",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "whitelisted-ips", "{{WHITELIST_ENTRY_ID}}"],
            '{\n  "ip": "{{WHITELIST_IP}}",\n  "mask": {{WHITELIST_MASK}}\n}',
            desc="Requires **`WHITELIST_ENTRY_ID`**.",
        ),
        tests_basic(),
    ),
    item(
        "DEL Delete Whitelisted IP",
        req(
            "DELETE",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "whitelisted-ips"],
            query={"id": "{{WHITELIST_ENTRY_ID}}"},
            desc="Query **`id`** = whitelist row id.",
        ),
        tests_basic(),
    ),
    item(
        "PUT Update Destination URI",
        req(
            "PUT",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "destination-uris", "{{DESTINATION_ID}}"],
            '{\n  "priority": 0,\n  "weight": 5\n}',
            desc="Adjust priority/weight per API limits. Requires **`DESTINATION_ID`**.",
        ),
        tests_basic(),
    ),
    item(
        "DEL Delete Destination URI",
        req(
            "DELETE",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "destination-uris"],
            query={"id": "{{DESTINATION_ID}}"},
            desc="Query **`id`**.",
        ),
        tests_basic(),
    ),
    item(
        "DEL Delete Phone Number Mapping",
        req(
            "DELETE",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "phone-numbers"],
            query={"id": "{{PHONE_MAPPING_ID}}"},
            desc="Query **`id`**.",
        ),
        tests_basic(),
    ),
    item(
        "GET List Trunk Settings",
        req("GET", BASE_PATH + ["trunks", "{{TRUNK_SID}}", "settings"],
            desc="Read all settings for the trunk."),
        tests_basic(),
    ),
    item(
        "DEL Delete Trunk Setting",
        req(
            "DELETE",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}", "settings"],
            query={"name": "trunk_external_alias"},
            desc="Query **`name`** = setting key to remove.",
        ),
        tests_basic(),
    ),
    item(
        "PUT Update Trunk",
        req(
            "PUT",
            BASE_PATH + ["trunks", "{{TRUNK_SID}}"],
            '{\n  "trunk_name": "{{TRUNK_NAME}}"\n}',
            desc="Partial trunk update (`trunk_name`, `auth_type`, `nso_code`, etc. per API).",
        ),
        tests_basic(),
    ),
]

folder_manage = {
    "name": "3. MANAGE & VIEW",
    "description": "CRUD and readbacks: matches the **Manage & View** folder in the Exotel SIP Trunking APIs workspace, plus extra list/update/delete calls for trunks, trunk maps, and credentials where applicable.",
    "item": manage_items,
}

COLLECTION_DESCRIPTION = """# Exotel SIP Trunking APIs

Resources you can **demo and share** with customers and partners. Import the companion **Environment** and set API key, token, domain, and account SID.

## 👋 Introduction

This collection mirrors the **Exotel SIP Trunking APIs** workspace layout:

- **1. GETTING STARTED (PSTN)** — Step-by-step PSTN trunk setup (`pstn` DID mode).
- **2. STREAMKIT (Voice AI)** — Flow-mode DID, ACL, and SIP **digest credentials** for Voice AI.
- **3. MANAGE & VIEW** — GET/PUT/POST/DEL operations to inspect and change existing configuration.

## 🚀 Getting started

1. Import **Exotel_vSIP_Environment.json** and select it.
2. Set `EXO_AUTH_KEY`, `EXO_AUTH_TOKEN`, `EXO_API_DOMAIN`, `EXO_ACCOUNT_SID`.
3. Run **Step 1: Create Trunk** in either workflow folder; `TRUNK_SID` is saved for later requests.
4. Use **MANAGE & VIEW** for audits and clean-up (`PHONE_MAPPING_ID`, `WHITELIST_ENTRY_ID`, `DESTINATION_ID`, `CREDENTIAL_ID` from responses or env).

## ⭐ Best practices

- Do **not** commit real API keys; use Postman **secret** type for tokens.
- Prefer **environment variables** for all secrets and IDs.
- **Delete trunk** is destructive — use a test account when possible.

**Auth:** Collection uses **Basic** auth (`API_KEY` / `API_TOKEN`). The API also accepts **Bearer** where enabled.

**Docs:** https://developer.exotel.com/api/sip-trunking-apis
"""

collection = {
    "info": {
        "name": "Exotel SIP Trunking APIs",
        "description": COLLECTION_DESCRIPTION,
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "item": [folder_pstn, folder_streamkit, folder_manage],
    "auth": {
        "type": "basic",
        "basic": [
            {"key": "username", "value": "{{EXO_AUTH_KEY}}", "type": "string"},
            {"key": "password", "value": "{{EXO_AUTH_TOKEN}}", "type": "string"},
        ],
    },
    "event": [
        {
            "listen": "prerequest",
            "script": {
                "type": "text/javascript",
                "exec": [
                    "const required = ['EXO_AUTH_KEY','EXO_AUTH_TOKEN','EXO_API_DOMAIN','EXO_ACCOUNT_SID'];",
                    "const miss = required.filter(k => !pm.environment.get(k));",
                    "if (miss.length) console.log('Missing env: ' + miss.join(', '));",
                ],
            },
        }
    ],
    "variable": [
        {"key": "baseUrl", "value": "https://{{EXO_API_DOMAIN}}/v2/accounts/{{EXO_ACCOUNT_SID}}", "type": "string"}
    ],
}

out = Path(__file__).resolve().parent / "Exotel_vSIP_API_Collection.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(collection, f, indent=2)
print("Wrote", out)
