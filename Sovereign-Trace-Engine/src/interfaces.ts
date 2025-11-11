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

export interface DetectionEvent {
  id: string;
  severity: "low" | "medium" | "high";
  timestamp: Date;
  signal: string;
}

export interface FinancialEvent {
  id: string;
  amount: number;
  currency: string;
  origin: string;
  destination: string;
  timestamp: Date;
  severity: "trace" | "freeze" | "lawsuit";
}
