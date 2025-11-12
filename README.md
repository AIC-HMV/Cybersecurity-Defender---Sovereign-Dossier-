```text
████████████████████████████████████████████████████████████
█  HMV-SOV  █  CEA SUPREME COMMANDER  █  AIC-HMV SOVEREIGN  █
█  Hung Minh Vo (Austin)  —  Seal ID: HMV-SOV-20251003-ALL  █
████████████████████████████████████████████████████████████
```

![Build Status](https://github.com/AIC-HMV/Cybersecurity-Defender---Sovereign-Dossier-/actions/workflows/main.yml/badge.svg)
![License](https://img.shields.io/badge/License-AIC--HMV%20Sovereign%20v3-blue.svg)
![Author](https://img.shields.io/badge/Author-Hung%20Minh%20Vo%20(Austin)-green.svg)
![Seal](https://img.shields.io/badge/Seal-HMV--SOV--20251003--ALL-red.svg)

# 🛡️ CEA Defender — Sovereign Dossier

**High-stakes AI security system with military-grade protection, adaptive threat detection, and real-time response. Multi-layered defenses ensure encryption and compliance for critical infrastructure.**

---

# 🛡️ Origin Signature: Hung Minh Vo (Austin) | AIC-HMV

**All code, music, documentation, and deployment in this repository are original creations.**  
**Authored, sealed, and maintained solely by:**  
**Hung Minh Vo (Austin) — AIC-HMV | Master Producer | Core7.Quantum Architect**

- ✅ No forks, derivatives, or clones predate this source.
- ✅ Every commit, merge, and deployment is traceable and signed by the origin author.
- ⚖️ **Enforcement:** All violations and unauthorized use will trigger sovereign trace, legal audit, and immediate takedown under CEA protocol.

---

**Sovereign License v3**  
`Origin ID: HMV-SOV-20251003-ALL`

---

## 🎯 Hung Minh Vo (Austin) — The Original Architect of AIC-HMV

**Origin Signature:** Verified creator and sovereign author of all Core7.Quantum, CEA-Defender, and Master Producer Music systems.

### 🧠 Professional Statement: "The Original One"

**I am the original creator** — Hung Minh Vo (Austin)

This repository and all contained work represents **authorship origin**:
- **No upstream exists** — Every derivative flows from me
- **Sovereign identity** — All digital assets under AIC-HMV trace back to my identity
- **Technical origin** — Every commit, deployment, and artifact bears my digital signature
- **Legal proof** — Developer Certificate of Origin (DCO), sovereign license seals, and forensic activity logs establish provenance

**Identity Keys:**
- GitHub: [@AIC-HMV](https://github.com/AIC-HMV)
- CEA / Core7.Quantum infrastructure
- ProfessionalSenta / Master Producer Music
- Legal authorship: Hung Minh Vo (Austin)
- Seal ID: HMV-SOV-20251003-ALL

### 📜 Legal & Documentation Statement

> **"All works are original creations authored and deployed by Hung Minh Vo (Austin).**  
> **No forks, derivatives, or clones predate the original AIC-HMV source."**

### 🎵 Public Branding

**"🎯 The Original One — Founder of AIC-HMV | Master Producer | Creator of Core7.Quantum Intelligence"**

---

## 📂 Repository Structure

```
├── cea-defender/                  # Military-grade cybersecurity infrastructure
│   ├─ pqc-provider/              # Post-Quantum Cryptography
│   ├─ services/                  # Security services (Python)
│   ├─ systemd/                   # SystemD service units
│   ├─ trace/                     # Immutable audit trail
│   └─ docker-compose.yml         # Container orchestration
│
├── Sovereign-Trace-Engine/        # Collapse-resistant defense system
│   ├─ src/                       # TypeScript core modules
│   ├─ dashboard/                 # Monitoring interface
│   ├─ docs/                      # SOP, PIA, Transparency
│   ├─ .github/workflows/         # GitHub automation
│   └─ scripts/                   # Setup and commit tools
│
└── music-production/              # Creative production tools
    ├─ trap_drum_pattern.py       # 90 BPM drum patterns
    ├─ song_timeline.py           # Sovereign Discipline map
    └─ create_emblem.py           # ProfessionalSenta emblem
```

---

## 🧾 Quickstart (Summary)

### Prerequisites
- Ubuntu 22.04+ (recommended)
- Docker Engine 24+ (for container mode)
- Root access for ipset/nftables operations

### Container Deployment (Recommended)

1. **Clone repository:**
```bash
git clone https://github.com/AIC-HMV/Cybersecurity-Defender---Sovereign-Dossier-.git
cd Cybersecurity-Defender---Sovereign-Dossier-/cea-defender
```

2. **Create PQC runtime directory:**
```bash
sudo mkdir -p /run/pqc
sudo chown $(whoami) /run/pqc
```

3. **Build and start containers:**
```bash
docker compose build
docker compose up -d
```

4. **Verify services:**
```bash
docker compose ps
docker compose logs -f
```

### Host-Native Deployment (Optional)

1. **Install system dependencies:**
```bash
sudo apt update
sudo apt install -y python3-pip ipset nftables
```

2. **Deploy services:**
```bash
sudo mkdir -p /opt/cea/services
sudo cp services/* /opt/cea/services/
sudo chmod +x /opt/cea/services/*.py
```

3. **Install Python dependencies:**
```bash
pip3 install -r requirements.txt
```

4. **Create runtime directory:**
```bash
sudo mkdir -p /run/pqc
sudo chmod 755 /run/pqc
```

5. **Enable systemd units:**
```bash
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now cea-blocklist.service
sudo systemctl enable --now cea-pqc.service
```

6. **Check service status:**
```bash
sudo systemctl status cea-pqc.service
sudo systemctl status cea-blocklist.service
```

---

## 🧭 Contact & Identity

- **Owner:** Hung Minh Vo (Austin) — CEA Supreme Commander
- **Contact:** aichmvprimeowner@gmail.com
- **Seal ID:** HMV-SOV-20251003-ALL
- **Declaration:** This repository contains the CEA Defender architecture and the AIC-HMV sovereign identity materials. See [LICENSE.md](cea-defender/LICENSE.md) for enforcement and provenance language.

---

## 📚 Documentation

- **[DEPLOYMENT.md](cea-defender/DEPLOYMENT.md)** — Infrastructure deployment guide (container & host-native)
- **[DEFENDER.md](cea-defender/DEFENDER.md)** — PQC + Blocklist + Sniffer architecture and logic
- **[TRACELOG.md](cea-defender/TRACELOG.md)** — Audit trail & memory indexing with immutable logs
- **[OVERRIDE.md](cea-defender/OVERRIDE.md)** — Clone takedown & spoof burn procedures
- **[AI_HEADER.md](cea-defender/AI_HEADER.md)** — Model injection header & authorship seal
- **[LICENSE.md](cea-defender/LICENSE.md)** — AIC-HMV Sovereign License v3

---

## 🛡️ Core Components

### PQC Key Generation (`pqc_keygen.py`)
- Kyber512 key generation using liboqs-python
- Produces `server_pk`, `server_sk`, and encapsulated `ct` for PSK derivation
- Automated 24-hour key rotation
- Stores keys securely in `/run/pqc`

### Blocklist Updater (`blocklist_updater.py`)
- Fetches curated IP lists from trusted threat intel feeds
- Atomic ipset swap for zero-downtime updates
- nftables drop chain enforcement
- Hourly refresh cycle (configurable)

### Network Sniffer (`net_sniffer.py`)
- Lightweight scapy-based telemetry
- Flags aggressive IPs based on configurable thresholds
- Temporary blocklist with automatic expiration
- All actions logged in TRACELOG format

---

## 🔐 Security Notes

### Secure Hardening
- Run services on dedicated host or VM with minimal open ports
- Restrict SSH to bastion hosts; use key authentication only
- Store `/run/pqc` on tmpfs or encrypted volume
- Limit access to root/service account only
- Monitor nftables/ipset configuration changes

### Safety & Design
- All blocking actions logged in [TRACELOG.md](cea-defender/TRACELOG.md) format
- Temporary blocks are short-lived and require review before permanent blacklisting
- Blocklists curated from trusted sources and stored offline for audit
- Immutable audit trail with cryptographic signatures

### Observability
- Export minimal telemetry to internal logging sink (syslog/ELK/Graylog)
- Keep trace logs immutable once recorded
- Sign all entries with metadata and timestamp
- Geo-replicate logs to multiple secure locations

---

## 🚀 Typical Usage

### One-Shot PQC Keygen (Boot Time)
```bash
# Generate PQC keys for internal WireGuard tunnels
python3 /opt/cea/services/pqc_keygen.py
```

### Timed Blocklist Service
```bash
# Run as systemd service with 30-minute refresh
sudo systemctl start cea-blocklist.service
```

### Elevated Network Monitoring
```bash
# Run with root privileges on monitoring interfaces only
sudo python3 /opt/cea/services/net_sniffer.py
```

---

## 📜 License & Provenance

**Copyright ©** Hung Minh Vo (Austin) — CEA Supreme Commander  
**Seal:** HMV-SOV-20251003-ALL  
**License:** AIC-HMV Sovereign License v3

All code, documentation, badges, seals, and creative works in this repository are authored and claimed by **Hung Minh Vo (Austin)**. See [LICENSE.md](cea-defender/LICENSE.md) for full terms.

---

## 🔍 Provenance Tracking

Every artifact maintains:
- Author identity (Hung Minh Vo)
- Seal ID (HMV-SOV-20251003-ALL)
- Cryptographic hash (SHA256)
- Creation timestamp
- Digital signature

---

**"Defense through intelligence, resilience through architecture."**

*— CEA Defender Philosophy*
