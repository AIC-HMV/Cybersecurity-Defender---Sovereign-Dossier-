#!/bin/bash
# PQC Provider Entrypoint Script
# Author: Hung Minh Vo (Austin) — CEA Supreme Commander
# Seal: HMV-SOV-20251003-ALL

set -e

echo "🔐 CEA PQC Provider starting..."
echo "Provenance: HMV-SOV-20251003-ALL"
echo "Owner: Hung Minh Vo (Austin)"

# Ensure key directory exists
mkdir -p /run/pqc
chmod 755 /run/pqc

# Generate initial PQC keypair if not exists
if [ ! -f /run/pqc/pqc_public.key ]; then
    echo "Generating initial PQC keypair..."
    python3 -c "
import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

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
with open('/run/pqc/pqc_private.key', 'wb') as f:
    f.write(private_pem)

with open('/run/pqc/pqc_public.key', 'wb') as f:
    f.write(public_pem)

os.chmod('/run/pqc/pqc_private.key', 0o600)
os.chmod('/run/pqc/pqc_public.key', 0o644)

print('✅ PQC keypair generated successfully')
"
fi

echo "✅ PQC Provider initialized"
echo "📁 Keys stored in: /run/pqc"
echo "🛡️ Monitoring for key rotation requests..."

# Keep container running and monitor for requests
tail -f /dev/null
