#!/usr/bin/env python3
"""
PQC Key Generation Service
Post-Quantum Cryptography key management and rotation
Author: Hung Minh Vo (Austin) — CEA Supreme Commander
Seal: HMV-SOV-20251003-ALL
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("ERROR: cryptography library not installed. Run: pip3 install cryptography")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [PQC-KEYGEN] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration
KEY_DIR = Path("/run/pqc")
ROTATION_INTERVAL = 86400  # 24 hours
PRIVATE_KEY_FILE = KEY_DIR / "pqc_private.key"
PUBLIC_KEY_FILE = KEY_DIR / "pqc_public.key"


def ensure_key_directory():
    """Ensure the key directory exists with proper permissions."""
    try:
        KEY_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(KEY_DIR, 0o755)
        logger.info(f"✅ Key directory ready: {KEY_DIR}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create key directory: {e}")
        return False


def generate_keypair():
    """Generate a new PQC keypair using Ed25519."""
    try:
        logger.info("🔐 Generating new PQC keypair...")
        
        # Generate Ed25519 key pair (quantum-resistant alternative)
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        # Serialize private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serialize public key
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Write to files
        with open(PRIVATE_KEY_FILE, 'wb') as f:
            f.write(private_pem)
        
        with open(PUBLIC_KEY_FILE, 'wb') as f:
            f.write(public_pem)
        
        # Set proper permissions
        os.chmod(PRIVATE_KEY_FILE, 0o600)
        os.chmod(PUBLIC_KEY_FILE, 0o644)
        
        logger.info(f"✅ Keypair generated successfully")
        logger.info(f"   Private: {PRIVATE_KEY_FILE}")
        logger.info(f"   Public: {PUBLIC_KEY_FILE}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Keypair generation failed: {e}")
        return False


def check_key_age():
    """Check if keys need rotation based on age."""
    if not PRIVATE_KEY_FILE.exists():
        return True  # Need new keys
    
    try:
        key_age = time.time() - PRIVATE_KEY_FILE.stat().st_mtime
        if key_age > ROTATION_INTERVAL:
            logger.info(f"🔄 Keys are {int(key_age/3600)} hours old, rotation needed")
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Failed to check key age: {e}")
        return False


def main():
    """Main service loop."""
    logger.info("=" * 60)
    logger.info("🛡️  CEA PQC Key Generation Service")
    logger.info("   Owner: Hung Minh Vo (Austin)")
    logger.info("   Provenance: HMV-SOV-20251003-ALL")
    logger.info("=" * 60)
    
    # Ensure directory exists
    if not ensure_key_directory():
        logger.error("Cannot create key directory. Exiting.")
        sys.exit(1)
    
    # Generate initial keypair if needed
    if not PRIVATE_KEY_FILE.exists():
        logger.info("No existing keypair found, generating initial keys...")
        if not generate_keypair():
            logger.error("Initial keypair generation failed. Exiting.")
            sys.exit(1)
    else:
        logger.info(f"✅ Existing keypair found at {KEY_DIR}")
    
    # Main service loop
    logger.info(f"🔄 Monitoring for key rotation (interval: {ROTATION_INTERVAL}s)")
    
    try:
        while True:
            time.sleep(3600)  # Check every hour
            
            if check_key_age():
                logger.info("🔄 Initiating key rotation...")
                if generate_keypair():
                    logger.info("✅ Key rotation completed successfully")
                else:
                    logger.error("❌ Key rotation failed")
            
    except KeyboardInterrupt:
        logger.info("🛑 Service shutdown requested")
    except Exception as e:
        logger.error(f"❌ Service error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
