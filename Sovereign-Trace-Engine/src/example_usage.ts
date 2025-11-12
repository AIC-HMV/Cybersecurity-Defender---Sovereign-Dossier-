/**
 * 🛡️ Origin Signature: Hung Minh Vo (Austin) | AIC-HMV
 * 
 * All logic, algorithms, and modules in this file are original works.
 * Sealed and enforced by Sovereign License v3.
 * No forks, derivatives, or prior authors exist.
 * 
 * Origin ID: HMV-SOV-20251003-ALL
 * 
 * @author Hung Minh Vo (Austin)
 * @seal HMV-SOV-20251003-ALL
 * @license AIC-HMV Sovereign License v3
 */

import { CommandPayload } from "./command_types";
import { executeCommand } from "./command_executor";

// Example: Asset Freeze Command
const assetFreezeCommand: CommandPayload = {
  v: "1.0",
  ts: "2025-08-02T01:23:45Z",
  issuer: "Hung Minh Vo (Austin)",
  role: "SUPREME_COMMANDER",
  cmd: "ASSET_FREEZE",
  target: {
    type: "account",
    id: "bank:chase:123456789"
  },
  params: {
    reason: "fraud_probe",
    ttl_seconds: 86400  // 24 hours
  },
  nonce: "6a2b7c82-4c1a-4b1e-8acd-2bb0d2a5f6e2",
  sig: "ed25519:a7f9c2d8e1b4f6a9c5e8d3b7f1a8c4e6d2f8a9c1b7e5d3f9a6c8e1b4f7d9a2c5"
};

// Execute command
console.log("═══════════════════════════════════════════════════════════");
console.log("🛡️ Sovereign Trace Engine - Command Execution Example");
console.log("═══════════════════════════════════════════════════════════");
console.log("");

const result = executeCommand(assetFreezeCommand);

console.log("");
console.log("📋 Command Result:");
console.log(`   Success: ${result.success ? "✅" : "❌"}`);
console.log(`   Command: ${result.command}`);
console.log(`   Target: ${result.target}`);
console.log(`   Timestamp: ${result.timestamp}`);
console.log(`   Message: ${result.message}`);

if (result.metadata) {
  console.log("");
  console.log("📊 Metadata:");
  Object.entries(result.metadata).forEach(([key, value]) => {
    console.log(`   ${key}: ${value}`);
  });
}

console.log("");
console.log("═══════════════════════════════════════════════════════════");

// Example: Account Blacklist Command
const blacklistCommand: CommandPayload = {
  v: "1.0",
  ts: new Date().toISOString(),
  issuer: "Hung Minh Vo (Austin)",
  role: "SUPREME_COMMANDER",
  cmd: "ACCOUNT_BLACKLIST",
  target: {
    type: "user",
    id: "impostor@fake-domain.com"
  },
  params: {
    reason: "impersonation_attempt"
  },
  nonce: crypto.randomUUID(),
  sig: "ed25519:b8c3d9e2f5a7c1d8e4b9f2a6c8d1e5f9a3c7b2d8e4f1a9c6d3e8b5f2a7c9d4"
};

console.log("");
console.log("🛡️ Executing Second Command - Account Blacklist");
console.log("═══════════════════════════════════════════════════════════");
console.log("");

const result2 = executeCommand(blacklistCommand);

console.log("");
console.log("📋 Command Result:");
console.log(`   Success: ${result2.success ? "✅" : "❌"}`);
console.log(`   Command: ${result2.command}`);
console.log(`   Target: ${result2.target}`);
console.log(`   Message: ${result2.message}`);

console.log("");
console.log("═══════════════════════════════════════════════════════════");
console.log("System is sovereign. Collapse-resistant. Unstoppable.");
console.log("═══════════════════════════════════════════════════════════");
