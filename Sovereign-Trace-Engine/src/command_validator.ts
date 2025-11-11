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

import { CommandPayload, CommandResult, CommandValidator } from "./command_types";

export function validateCommand(cmd: CommandPayload): CommandValidator {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Validate version
  if (!cmd.v || cmd.v !== "1.0") {
    errors.push("Invalid or missing command version");
  }

  // Validate timestamp
  if (!cmd.ts || !isValidISO8601(cmd.ts)) {
    errors.push("Invalid or missing timestamp");
  }

  // Validate issuer
  if (!cmd.issuer || cmd.issuer.trim() === "") {
    errors.push("Missing issuer");
  }

  // Validate role
  if (!cmd.role || !["SUPREME_COMMANDER", "OPERATOR", "OBSERVER"].includes(cmd.role)) {
    errors.push("Invalid or missing role");
  }

  // Validate command
  if (!cmd.cmd || cmd.cmd.trim() === "") {
    errors.push("Missing command");
  }

  // Validate target
  if (!cmd.target || !cmd.target.type || !cmd.target.id) {
    errors.push("Invalid target specification");
  }

  // Validate nonce
  if (!cmd.nonce || !isValidUUID(cmd.nonce)) {
    errors.push("Invalid or missing nonce");
  }

  // Validate signature
  if (!cmd.sig || cmd.sig.trim() === "") {
    errors.push("Missing signature");
  }

  // Warnings for SUPREME_COMMANDER actions
  if (cmd.role === "SUPREME_COMMANDER") {
    warnings.push("SUPREME_COMMANDER action detected - high privilege operation");
  }

  return {
    isValid: errors.length === 0,
    errors,
    warnings
  };
}

function isValidISO8601(timestamp: string): boolean {
  const iso8601Regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$/;
  return iso8601Regex.test(timestamp);
}

function isValidUUID(uuid: string): boolean {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
}

export function verifySignature(cmd: CommandPayload, publicKey?: string): boolean {
  // Signature verification would be implemented here with actual cryptographic verification
  // For now, this is a placeholder that checks signature format
  if (!cmd.sig || cmd.sig.length < 64) {
    return false;
  }
  
  console.log(`[SIGNATURE VERIFY] Command: ${cmd.cmd} | Issuer: ${cmd.issuer}`);
  console.log(`[SIGNATURE VERIFY] Signature present: ${cmd.sig.substring(0, 16)}...`);
  
  // In production, this would use Ed25519 or similar to verify
  // against the issuer's public key
  return true;
}
