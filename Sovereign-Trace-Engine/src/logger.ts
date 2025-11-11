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

import { DetectionEvent, FinancialEvent } from "./interfaces";

export function logEvent(event: DetectionEvent) {
  console.log(`[TRACE LOG] ${event.timestamp.toISOString()} | ${event.severity.toUpperCase()} | ${event.signal}`);
}

export function logFinancial(event: FinancialEvent) {
  console.log(`[FINANCIAL TRACE] ${event.timestamp.toISOString()} | ${event.severity.toUpperCase()} | ${event.amount} ${event.currency} | ${event.origin} → ${event.destination}`);
}
