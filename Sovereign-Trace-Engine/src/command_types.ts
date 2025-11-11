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

export interface CommandPayload {
  v: string;
  ts: string;
  issuer: string;
  role: "SUPREME_COMMANDER" | "OPERATOR" | "OBSERVER";
  cmd: string;
  target: {
    type: string;
    id: string;
  };
  params: {
    reason?: string;
    ttl_seconds?: number;
    [key: string]: any;
  };
  nonce: string;
  sig: string;
}

export interface CommandResult {
  success: boolean;
  command: string;
  target: string;
  timestamp: string;
  message: string;
  metadata?: any;
}

export interface CommandValidator {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}
