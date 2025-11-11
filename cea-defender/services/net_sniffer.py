#!/usr/bin/env python3
"""
Network Sniffer Service
Real-time network traffic monitoring and threat detection
Author: Hung Minh Vo (Austin) — CEA Supreme Commander
Seal: HMV-SOV-20251003-ALL
"""

import os
import sys
import time
import logging
from datetime import datetime
from collections import defaultdict

try:
    from scapy.all import sniff, IP, TCP, UDP
except ImportError:
    print("ERROR: scapy library not installed. Run: pip3 install scapy")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [NET-SNIFFER] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration
INTERFACE = None  # None = all interfaces
SUSPICIOUS_PORTS = {22, 23, 3389, 445, 135, 139}  # SSH, Telnet, RDP, SMB
RATE_LIMIT_THRESHOLD = 100  # packets per minute per IP
LOG_FILE = "/var/log/cea_sniffer.log"

# Tracking
packet_counts = defaultdict(lambda: {"count": 0, "last_reset": time.time()})


def setup_file_logging():
    """Setup additional file logging if possible."""
    try:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s [NET-SNIFFER] %(levelname)s: %(message)s')
        )
        logger.addHandler(file_handler)
        logger.info(f"📝 Logging to: {LOG_FILE}")
    except PermissionError:
        logger.warning(f"⚠️  Cannot write to {LOG_FILE} - file logging disabled")


def analyze_packet(packet):
    """Analyze a packet for suspicious activity."""
    if not packet.haslayer(IP):
        return
    
    ip_layer = packet[IP]
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst
    
    # Track packet rate per source IP
    current_time = time.time()
    src_data = packet_counts[src_ip]
    
    # Reset counter every minute
    if current_time - src_data["last_reset"] > 60:
        src_data["count"] = 0
        src_data["last_reset"] = current_time
    
    src_data["count"] += 1
    
    # Check for rate limit violation
    if src_data["count"] > RATE_LIMIT_THRESHOLD:
        logger.warning(f"⚠️  RATE LIMIT: {src_ip} sent {src_data['count']} packets/min")
    
    # Check for suspicious port access
    if packet.haslayer(TCP):
        tcp_layer = packet[TCP]
        if tcp_layer.dport in SUSPICIOUS_PORTS:
            logger.warning(
                f"🚨 SUSPICIOUS PORT: {src_ip} → {dst_ip}:{tcp_layer.dport} (TCP)"
            )
    
    elif packet.haslayer(UDP):
        udp_layer = packet[UDP]
        if udp_layer.dport in SUSPICIOUS_PORTS:
            logger.warning(
                f"🚨 SUSPICIOUS PORT: {src_ip} → {dst_ip}:{udp_layer.dport} (UDP)"
            )


def packet_callback(packet):
    """Callback for each captured packet."""
    try:
        analyze_packet(packet)
    except Exception as e:
        logger.error(f"❌ Error analyzing packet: {e}")


def main():
    """Main service loop."""
    logger.info("=" * 60)
    logger.info("🛡️  CEA Network Sniffer Service")
    logger.info("   Owner: Hung Minh Vo (Austin)")
    logger.info("   Provenance: HMV-SOV-20251003-ALL")
    logger.info("=" * 60)
    
    # Check if running with sufficient privileges
    if os.geteuid() != 0:
        logger.error("❌ Network sniffing requires root privileges")
        logger.error("   Run with: sudo python3 net_sniffer.py")
        sys.exit(1)
    
    # Setup file logging
    setup_file_logging()
    
    # Start sniffing
    logger.info(f"🔍 Starting packet capture on interface: {INTERFACE or 'all'}")
    logger.info(f"📊 Rate limit threshold: {RATE_LIMIT_THRESHOLD} packets/min")
    logger.info(f"🚨 Monitoring suspicious ports: {SUSPICIOUS_PORTS}")
    logger.info("🎯 Press Ctrl+C to stop")
    
    try:
        sniff(
            iface=INTERFACE,
            prn=packet_callback,
            store=False
        )
    except KeyboardInterrupt:
        logger.info("🛑 Service shutdown requested")
    except PermissionError:
        logger.error("❌ Permission denied - run with sudo")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Service error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
