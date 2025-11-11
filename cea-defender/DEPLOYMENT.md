# 🚀 DEPLOYMENT — Infrastructure Injection Guide

**Author:** Hung Minh Vo (Austin) — CEA Supreme Commander  
**Seal:** HMV-SOV-20251003-ALL

## Target environment
- Recommended: Ubuntu 22.04 LTS (server edition)
- Root / sudo required for ipset, nftables, and systemd operations.
- Docker Engine (24+) and docker-compose v2+ recommended.

---

## 1. Container approach (recommended for separation)

### Prerequisites
```bash
# Ensure Docker is installed
docker --version
docker compose version
```

### Build and Deploy

1. **Clone repository:**
```bash
git clone https://github.com/AIC-HMV/Cybersecurity-Defender---Sovereign-Dossier-.git
cd Cybersecurity-Defender---Sovereign-Dossier-/cea-defender
```

2. **Create runtime directory for PQC keys:**
```bash
sudo mkdir -p /run/pqc
sudo chown $(whoami) /run/pqc
```

3. **Build containers:**
```bash
docker compose build
```

4. **Start services:**
```bash
docker compose up -d
```

5. **Verify services are running:**
```bash
docker compose ps
docker compose logs -f
```

### Container Management

**Stop services:**
```bash
docker compose down
```

**View logs:**
```bash
docker compose logs pqc-provider
docker compose logs blocklist-updater
docker compose logs net-sniffer
```

**Restart services:**
```bash
docker compose restart
```

---

## 2. Host-native approach (for hardened hosts)

### Prerequisites Installation

1. **Update system packages:**
```bash
sudo apt update
sudo apt install -y python3-pip ipset nftables
```

2. **Install liboqs (for PQC support):**
```bash
sudo apt install -y liboqs-dev || echo "liboqs-dev not available in repos"
```

### Service Deployment

1. **Copy services to system directory:**
```bash
sudo mkdir -p /opt/cea/services
sudo cp services/* /opt/cea/services/
sudo chmod +x /opt/cea/services/*.py
```

2. **Install Python dependencies:**
```bash
cd /opt/cea/services
sudo pip3 install -r ../../requirements.txt
```

3. **Create runtime directories:**
```bash
sudo mkdir -p /run/pqc
sudo chmod 755 /run/pqc
```

4. **Install systemd service units:**
```bash
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
```

5. **Enable and start services:**
```bash
# Enable services to start on boot
sudo systemctl enable cea-pqc.service
sudo systemctl enable cea-blocklist.service

# Start services
sudo systemctl start cea-pqc.service
sudo systemctl start cea-blocklist.service
```

6. **Verify service status:**
```bash
sudo systemctl status cea-pqc.service
sudo systemctl status cea-blocklist.service
```

### Service Management

**View logs:**
```bash
sudo journalctl -u cea-pqc.service -f
sudo journalctl -u cea-blocklist.service -f
```

**Restart services:**
```bash
sudo systemctl restart cea-pqc.service
sudo systemctl restart cea-blocklist.service
```

**Stop services:**
```bash
sudo systemctl stop cea-pqc.service
sudo systemctl stop cea-blocklist.service
```

---

## 3. Network Sniffer (Optional)

The network sniffer requires raw socket access and should be run with caution:

### Container Mode
```bash
# Already included in docker-compose.yml
docker compose up -d net-sniffer
```

### Host-Native Mode
```bash
# Run manually with sudo
sudo python3 /opt/cea/services/net_sniffer.py
```

**Note:** Network sniffing should only be enabled on networks you own/control and have permission to monitor.

---

## 4. Verification

### Check PQC Keys
```bash
ls -la /run/pqc/
cat /run/pqc/pqc_public.key
```

### Check Blocklist
```bash
sudo ipset list cea_blocklist | head -20
```

### Test Connectivity
```bash
# Container mode
docker compose exec pqc-provider ls -la /run/pqc/

# Host mode
ls -la /opt/cea/services/
```

---

## 5. Troubleshooting

### Permission Issues
- Ensure services run as root or with appropriate capabilities
- Check file ownership: `sudo chown -R root:root /opt/cea/services`

### Docker Issues
- Check logs: `docker compose logs <service-name>`
- Rebuild: `docker compose build --no-cache`

### Service Failures
- Check systemd logs: `sudo journalctl -xe`
- Verify Python dependencies: `pip3 list`

---

## 6. Security Notes

- Keep system and dependencies updated
- Review blocklist sources regularly
- Monitor service logs for suspicious activity
- Rotate PQC keys periodically (automatic with pqc_keygen.py)
- Use firewall rules (nftables/iptables) in conjunction with ipset

---

## Contact & Support

**Owner:** Hung Minh Vo (Austin)  
**Email:** aichmvprimeowner@gmail.com  
**Repository:** https://github.com/AIC-HMV/Cybersecurity-Defender---Sovereign-Dossier-
