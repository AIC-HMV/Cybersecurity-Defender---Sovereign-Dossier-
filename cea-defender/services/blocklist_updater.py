#!/usr/bin/env python3
"""
🛡️ Origin Signature: Hung Minh Vo (Austin) | AIC-HMV

All logic, algorithms, and modules in this file are original works.
Sealed and enforced by Sovereign License v3.
No forks, derivatives, or prior authors exist.

Origin ID: HMV-SOV-20251003-ALL

---

Blocklist Updater Service
Automated threat intelligence feed aggregation and ipset management
Author: Hung Minh Vo (Austin) — CEA Supreme Commander
Seal: HMV-SOV-20251003-ALL
"""

import os
import sys
import time
import logging
import subprocess
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: requests library not installed. Run: pip3 install requests")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [BLOCKLIST] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration
IPSET_NAME = "cea_blocklist"
UPDATE_INTERVAL = 3600  # 1 hour
BLOCKLIST_SOURCES = [
    "https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt",
    "https://www.spamhaus.org/drop/drop.txt",
]


def ensure_ipset_exists():
    """Ensure the ipset for blocklist exists."""
    try:
        # Check if ipset exists
        result = subprocess.run(
            ["ipset", "list", IPSET_NAME],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            # Create new ipset
            logger.info(f"Creating ipset: {IPSET_NAME}")
            subprocess.run(
                ["ipset", "create", IPSET_NAME, "hash:net", "maxelem", "65536"],
                check=True
            )
            logger.info(f"✅ Created ipset: {IPSET_NAME}")
        else:
            logger.info(f"✅ ipset exists: {IPSET_NAME}")
        
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to ensure ipset exists: {e}")
        logger.error("   Note: ipset requires root/sudo privileges")
        return False
    except FileNotFoundError:
        logger.error("❌ ipset command not found. Install with: sudo apt install ipset")
        return False


def fetch_blocklist(url):
    """Fetch blocklist from a given URL."""
    try:
        logger.info(f"📥 Fetching blocklist from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"❌ Failed to fetch {url}: {e}")
        return None


def parse_ips(content):
    """Parse IP addresses/networks from blocklist content."""
    ips = []
    for line in content.split('\n'):
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#') or line.startswith(';'):
            continue
        
        # Extract IP/CIDR
        parts = line.split()
        if parts:
            ip = parts[0]
            # Basic validation
            if '.' in ip or ':' in ip:
                ips.append(ip)
    
    return ips


def update_blocklist():
    """Update the blocklist from threat intelligence sources."""
    logger.info("🔄 Starting blocklist update...")
    
    all_ips = set()
    
    # Fetch from all sources
    for source in BLOCKLIST_SOURCES:
        content = fetch_blocklist(source)
        if content:
            ips = parse_ips(content)
            all_ips.update(ips)
            logger.info(f"   Added {len(ips)} entries from {source}")
    
    if not all_ips:
        logger.warning("⚠️  No IPs collected from sources")
        return False
    
    logger.info(f"📊 Total unique IPs collected: {len(all_ips)}")
    
    # Flush existing entries
    try:
        subprocess.run(["ipset", "flush", IPSET_NAME], check=True)
        logger.info(f"🧹 Flushed existing entries from {IPSET_NAME}")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to flush ipset: {e}")
        return False
    
    # Add new entries
    success_count = 0
    for ip in all_ips:
        try:
            subprocess.run(
                ["ipset", "add", IPSET_NAME, ip, "-exist"],
                capture_output=True,
                check=True
            )
            success_count += 1
        except subprocess.CalledProcessError:
            # Skip invalid IPs silently
            pass
    
    logger.info(f"✅ Successfully added {success_count}/{len(all_ips)} IPs to blocklist")
    return True


def main():
    """Main service loop."""
    logger.info("=" * 60)
    logger.info("🛡️  CEA Blocklist Updater Service")
    logger.info("   Owner: Hung Minh Vo (Austin)")
    logger.info("   Provenance: HMV-SOV-20251003-ALL")
    logger.info("=" * 60)
    
    # Check if running with sufficient privileges
    if os.geteuid() != 0:
        logger.warning("⚠️  Not running as root - ipset operations may fail")
        logger.warning("   Run with: sudo python3 blocklist_updater.py")
    
    # Ensure ipset exists
    if not ensure_ipset_exists():
        logger.error("Cannot initialize ipset. Exiting.")
        sys.exit(1)
    
    # Initial update
    logger.info("🚀 Performing initial blocklist update...")
    update_blocklist()
    
    # Main service loop
    logger.info(f"🔄 Monitoring interval: {UPDATE_INTERVAL}s")
    
    try:
        while True:
            time.sleep(UPDATE_INTERVAL)
            update_blocklist()
            
    except KeyboardInterrupt:
        logger.info("🛑 Service shutdown requested")
    except Exception as e:
        logger.error(f"❌ Service error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
