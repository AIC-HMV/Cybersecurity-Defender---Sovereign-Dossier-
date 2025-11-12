# CEA Defender Trace Logs
# Author: Hung Minh Vo (Austin) — CEA Supreme Commander
# Seal: HMV-SOV-20251003-ALL

This directory contains immutable audit trail logs in JSONL format.

## Structure

```
trace/
├── 2025/
│   └── 10/
│       ├── trace-20251003.jsonl      # Daily trace log
│       ├── trace-20251003.jsonl.sig  # Ed25519 signature
│       └── trace-20251004.jsonl
└── revocations/
    └── revocations.txt               # Revoked entries
```

## Usage

All security events must be logged to this directory using the schema defined in TRACELOG.md.

### Log Entry Format (JSONL)
Each line is a complete JSON object representing one trace event:

```json
{"timestamp":"2025-10-03T12:00:00Z","event_id":"trace-20251003-0001","actor":"cea-pqc","seal_id":"HMV-SOV-20251003-ALL","action":"pqc-keygen","artifact":{"server_pk":"sha256:abc..."},"signature":"ed25519:sig...","context":{"host":"cea-node-01"}}
```

### Signature Verification
```bash
# Verify daily log signature
openssl dgst -sha256 -verify /run/pqc/pqc_public.key \
  -signature trace-20251003.jsonl.sig trace-20251003.jsonl
```

## Immutability

- Never modify or delete existing log entries
- Corrections must be appended as new corrective entries
- All entries must be cryptographically signed
- Geo-replicate to multiple secure locations

## Access Control

- Read: Security operators, auditors
- Write: Automated services only (via append)
- Delete: Never (retention policy governs archival)

---

**Provenance:** HMV-SOV-20251003-ALL
