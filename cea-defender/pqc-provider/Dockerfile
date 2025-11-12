# PQC Provider Container
# Post-Quantum Cryptography key generation and management
# Author: Hung Minh Vo (Austin) — CEA Supreme Commander
# Seal: HMV-SOV-20251003-ALL

FROM python:3.11-slim

LABEL maintainer="aichmvprimeowner@gmail.com"
LABEL description="Post-Quantum Cryptography Provider for CEA Defender"
LABEL version="1.0.0"
LABEL provenance="HMV-SOV-20251003-ALL"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python PQC libraries
RUN pip install --no-cache-dir \
    pqcrypto \
    cryptography \
    pyyaml

# Create working directory
WORKDIR /app

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create runtime directory for keys
RUN mkdir -p /run/pqc && chmod 755 /run/pqc

# Run as non-root user
RUN useradd -m -u 1000 pqcuser && chown -R pqcuser:pqcuser /app /run/pqc
USER pqcuser

ENTRYPOINT ["/app/entrypoint.sh"]
