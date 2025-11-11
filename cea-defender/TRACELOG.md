# 🔎 TRACELOG — Audit Trail & Memory Indexing

**Author:** Hung Minh Vo (Austin) — CEA Supreme Commander  
**Seal:** HMV-SOV-20251003-ALL

---

## Purpose
Persistent, tamper-evident logging format for provenance and forensic traceability. Designed to store event metadata, identity seals, and signed snapshots.

**Principles:**
- **Always record seal_id** and a cryptographic digest of artifacts
- **Rotate signing keys** periodically and publish revocation lists in `/trace/revocations`
- **Store copies** of trace logs in at least two geographically separated secure stores

**Immutability:**
- After a log entry is signed, **do not modify**
- If corrections are required, append a new corrective entry referencing the original event_id

---

## Log Entry Schema (JSON)

All trace events must conform to this schema:

```json
{
  "timestamp": "2025-10-03T12:00:00Z",
  "event_id": "trace-20251003-0001",
  "actor": "cea-pqc",
  "seal_id": "HMV-SOV-20251003-ALL",
  "action": "pqc-keygen",
  "artifact": {
    "server_pk": "sha256:abcd1234...",
    "server_sk": "sha256:ef015678...",
    "ct": "sha256:9abc4567..."
  },
  "signature": "ed25519:BASE64SIG",
  "context": {
    "host": "cea-node-01",
    "commit": "abcdef012345",
    "service": "pqc_keygen.py"
  }
}
```

### Required Fields
- **timestamp**: ISO 8601 format (UTC)
- **event_id**: Unique identifier (`trace-YYYYMMDD-NNNN`)
- **actor**: Service or user performing the action
- **seal_id**: Provenance seal (HMV-SOV-20251003-ALL)
- **action**: Operation performed (pqc-keygen, blocklist-update, ip-block, etc.)
- **artifact**: Object hashes and references
- **signature**: Ed25519 or Kyber signature of the entry
- **context**: Additional metadata (host, commit, version)

---

## 2025-10-03 — Initial Architecture Design

**Event:** Repository initialization and core architecture definition

**Components Established:**
- Post-Quantum Cryptography (PQC) provider service with Kyber512
- Blocklist updater with atomic ipset swaps
- Network sniffer with automatic threshold-based blocking
- Docker containerization strategy
- SystemD integration for host-native deployment

**Security Posture:**
- Kyber512 PQC keys for PSK derivation
- Automated key rotation (24-hour cycle)
- Multi-source threat intelligence aggregation with offline audit storage
- Real-time packet inspection with temporary blocking capability

**Provenance:** All files tagged with HMV-SOV-20251003-ALL

### Trace Entry
```json
{
  "timestamp": "2025-10-03T00:00:00Z",
  "event_id": "trace-20251003-0001",
  "actor": "system-init",
  "seal_id": "HMV-SOV-20251003-ALL",
  "action": "repository-init",
  "artifact": {
    "repo_hash": "sha256:repo_initial_commit",
    "structure": "cea-defender"
  },
  "signature": "ed25519:INIT_SIGNATURE",
  "context": {
    "host": "development",
    "version": "1.0.0"
  }
}
```

---

## Example Trace Entries

### PQC Key Generation Event
```json
{
  "timestamp": "2025-10-03T12:30:00Z",
  "event_id": "trace-20251003-0042",
  "actor": "cea-pqc",
  "seal_id": "HMV-SOV-20251003-ALL",
  "action": "pqc-keygen-kyber512",
  "artifact": {
    "server_pk": "sha256:a7f3c9d2e8b1f4a6c5e9d3b7f1a8c4e6",
    "server_sk": "sha256:b2e8f1a9c7d3e5f9a1b8c6d4e2f8a9c1",
    "ct": "sha256:c9f1e3a7b5d9f2e8a4c7b1f6e9d3a5c8"
  },
  "signature": "ed25519:SGVsbG8gV29ybGQh...",
  "context": {
    "host": "cea-node-01",
    "commit": "abcdef012345",
    "service": "pqc_keygen.py",
    "algorithm": "Kyber512"
  }
}
```

### Blocklist Update Event
```json
{
  "timestamp": "2025-10-03T13:00:00Z",
  "event_id": "trace-20251003-0043",
  "actor": "cea-blocklist",
  "seal_id": "HMV-SOV-20251003-ALL",
  "action": "blocklist-atomic-swap",
  "artifact": {
    "old_set": "cea_blocklist_old",
    "new_set": "cea_blocklist",
    "ip_count": 15234,
    "sources_hash": "sha256:d3e8f9a1c7b5e9f2a8c4d1e7b9f3a5c6"
  },
  "signature": "ed25519:QmxvY2tsaXN0IFN3YXAh...",
  "context": {
    "host": "cea-node-01",
    "service": "blocklist_updater.py",
    "duration_ms": 1234
  }
}
```

### IP Block Event (Temporary)
```json
{
  "timestamp": "2025-10-03T13:15:42Z",
  "event_id": "trace-20251003-0044",
  "actor": "cea-sniffer",
  "seal_id": "HMV-SOV-20251003-ALL",
  "action": "ip-block-temporary",
  "artifact": {
    "blocked_ip": "192.0.2.123",
    "reason": "rate-limit-exceeded",
    "packet_count": 156,
    "threshold": 100,
    "duration_seconds": 3600
  },
  "signature": "ed25519:VGVtcG9yYXJ5IEJsb2Nr...",
  "context": {
    "host": "cea-node-01",
    "service": "net_sniffer.py",
    "interface": "eth0",
    "review_required": true
  }
}
```

### Corrective Entry Example
```json
{
  "timestamp": "2025-10-03T14:00:00Z",
  "event_id": "trace-20251003-0045",
  "actor": "admin-operator",
  "seal_id": "HMV-SOV-20251003-ALL",
  "action": "correction",
  "artifact": {
    "corrects_event": "trace-20251003-0044",
    "correction": "IP 192.0.2.123 was legitimate traffic, unblocked",
    "original_action": "ip-block-temporary"
  },
  "signature": "ed25519:Q29ycmVjdGlvbiBFbnRyeQ==...",
  "context": {
    "host": "cea-node-01",
    "operator": "admin",
    "reason": "false-positive"
  }
}
```

---

## Storage & Replication

### Primary Storage
```
/var/log/cea/trace/
├── 2025/
│   └── 10/
│       ├── trace-20251003.jsonl
│       ├── trace-20251003.jsonl.sig
│       └── trace-20251004.jsonl
└── revocations/
    └── revocations.txt
```

### Geo-Replication Requirements
- **Primary site:** Production infrastructure
- **Secondary site:** Geographically separated backup
- **Tertiary site:** Cold storage / archive (optional)
- **Sync frequency:** Real-time or near-real-time
- **Integrity checks:** Verify signatures on replication

---

## Revocation List Format

File: `/var/log/cea/trace/revocations/revocations.txt`

```
# CEA Defender Revocation List
# Seal: HMV-SOV-20251003-ALL
# Format: event_id | timestamp | reason | signature

trace-20251001-0123 | 2025-10-02T10:00:00Z | key-compromise | ed25519:...
trace-20251002-0456 | 2025-10-03T15:30:00Z | operational-error | ed25519:...
```

---

## Compliance & Attribution

All trace logs are:
- **Authored by:** Hung Minh Vo (Austin)
- **Licensed under:** AIC-HMV Sovereign License v3
- **Provenance Seal:** HMV-SOV-20251003-ALL
- **Immutability:** Cryptographically enforced
- **Retention:** Per organizational policy (recommended: 7 years minimum)

---

## Audit Procedures

### Daily
- Verify trace log integrity (signatures)
- Check replication status
- Review temporary blocks for false positives

### Weekly
- Export and archive to cold storage
- Analyze patterns and anomalies
- Update revocation list if needed

### Monthly
- Full audit of all trace entries
- Compliance report generation
- Key rotation verification

### Annually
- Comprehensive security audit
- Geo-replication drill
- Disaster recovery test

---

**Provenance:** HMV-SOV-20251003-ALL  
**Last Updated:** 2025-10-03  
**Immutable:** Yes (append-only)
