# Command Execution System

**Author:** Hung Minh Vo (Commander, AIC-HMV)  
**Seal:** HMV-SOV-20251003-ALL

## Overview

The Sovereign Trace Engine now includes a robust command execution system that allows authorized users to execute high-privilege operations with cryptographic verification and audit trails.

## Command Structure

All commands follow a standardized JSON format:

```json
{
  "v": "1.0",
  "ts": "2025-08-02T01:23:45Z",
  "issuer": "Hung Minh Vo (Austin)",
  "role": "SUPREME_COMMANDER",
  "cmd": "ASSET_FREEZE",
  "target": {
    "type": "account",
    "id": "bank:chase:123456789"
  },
  "params": {
    "reason": "fraud_probe",
    "ttl_seconds": 86400
  },
  "nonce": "6a2b7c82-4c1a-4b1e-8acd-2bb0d2a5f6e2",
  "sig": "ed25519:signature_here"
}
```

## Fields

### Required Fields

- **v** (string): Command protocol version (currently "1.0")
- **ts** (string): ISO 8601 timestamp of command creation
- **issuer** (string): Full name of the person issuing the command
- **role** (string): Authority level - `SUPREME_COMMANDER`, `OPERATOR`, or `OBSERVER`
- **cmd** (string): Command type to execute
- **target** (object): Target of the command
  - **type** (string): Type of target (account, user, system, etc.)
  - **id** (string): Unique identifier for the target
- **params** (object): Command-specific parameters
- **nonce** (string): Unique UUID to prevent replay attacks
- **sig** (string): Cryptographic signature (Ed25519 or similar)

## Supported Commands

### ASSET_FREEZE
Freezes financial assets or accounts.

**Parameters:**
- `reason` (string): Justification for freeze
- `ttl_seconds` (number, optional): Duration in seconds (omit for indefinite)

**Example:**
```json
{
  "cmd": "ASSET_FREEZE",
  "target": { "type": "account", "id": "bank:chase:123456789" },
  "params": { "reason": "fraud_probe", "ttl_seconds": 86400 }
}
```

### ASSET_UNFREEZE
Removes freeze from previously frozen assets.

**Parameters:**
- None required

**Example:**
```json
{
  "cmd": "ASSET_UNFREEZE",
  "target": { "type": "account", "id": "bank:chase:123456789" },
  "params": {}
}
```

### ACCOUNT_BLACKLIST
Permanently blacklists an account or user.

**Parameters:**
- `reason` (string): Justification for blacklist

**Example:**
```json
{
  "cmd": "ACCOUNT_BLACKLIST",
  "target": { "type": "user", "id": "impostor@fake-domain.com" },
  "params": { "reason": "impersonation_attempt" }
}
```

### IDENTITY_VERIFY
Initiates identity verification process.

**Parameters:**
- None required

**Example:**
```json
{
  "cmd": "IDENTITY_VERIFY",
  "target": { "type": "user", "id": "user@example.com" },
  "params": {}
}
```

### TRACE_AUDIT
Performs comprehensive audit of trace logs.

**Parameters:**
- `start_date` (string, optional): Start of audit period
- `end_date` (string, optional): End of audit period

**Example:**
```json
{
  "cmd": "TRACE_AUDIT",
  "target": { "type": "system", "id": "trace-logs" },
  "params": { "start_date": "2025-01-01", "end_date": "2025-12-31" }
}
```

## Roles & Permissions

### SUPREME_COMMANDER
- **Access:** All commands
- **Authority:** Highest level
- **Restrictions:** None
- **Audit:** All actions logged with high-priority flag

### OPERATOR
- **Access:** ASSET_UNFREEZE, IDENTITY_VERIFY, TRACE_AUDIT
- **Authority:** Medium level
- **Restrictions:** Cannot freeze assets or blacklist
- **Audit:** All actions logged

### OBSERVER
- **Access:** TRACE_AUDIT (read-only)
- **Authority:** Lowest level
- **Restrictions:** Cannot modify any state
- **Audit:** View access logged

## Security Features

### Signature Verification
All commands must be cryptographically signed with Ed25519 or equivalent:
- Private key held by authorized issuer
- Public key registered in system
- Signature verified before execution
- Invalid signatures rejected immediately

### Replay Attack Prevention
- Each command requires unique UUID nonce
- Nonces tracked in immutable log
- Duplicate nonces rejected
- Timestamp validation (max 5 minute clock skew)

### Audit Trail
All commands logged with:
- Full command payload
- Execution result
- Timestamp
- Issuer identity
- Signature verification status

## Usage Example

```typescript
import { CommandPayload } from "./command_types";
import { executeCommand } from "./command_executor";

const command: CommandPayload = {
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
    ttl_seconds: 86400
  },
  nonce: "6a2b7c82-4c1a-4b1e-8acd-2bb0d2a5f6e2",
  sig: "ed25519:a7f9c2d8e1b4f6a9c5e8d3b7f1a8c4e6..."
};

const result = executeCommand(command);

if (result.success) {
  console.log("✅ Command executed successfully");
  console.log(`   Message: ${result.message}`);
} else {
  console.log("❌ Command execution failed");
  console.log(`   Error: ${result.message}`);
}
```

## Error Handling

### Validation Errors
Commands are validated before execution:
- Missing required fields → Rejected
- Invalid timestamp format → Rejected
- Unknown command type → Rejected
- Invalid target specification → Rejected
- Malformed nonce → Rejected

### Signature Errors
- Missing signature → Rejected
- Invalid signature → Rejected
- Signature verification failure → Rejected
- Public key not found → Rejected

### Execution Errors
- Insufficient permissions → Rejected
- Target not found → Logged and reported
- System unavailable → Retry mechanism
- Timeout → Logged and reported

## Integration

The command system integrates with:
- **Trace Engine** - All commands logged
- **Financial Hooks** - Asset operations monitored
- **Defense Autocode** - Blacklist enforcement
- **Enforcement** - Lawsuit protocols

## Best Practices

1. **Always use fresh nonces** - Never reuse UUIDs
2. **Verify timestamps** - Check clock synchronization
3. **Secure private keys** - Use hardware security modules
4. **Log all operations** - Maintain complete audit trail
5. **Review permissions** - Regularly audit role assignments
6. **Test signatures** - Verify cryptographic implementation
7. **Monitor execution** - Real-time alerting on failures

## Future Enhancements

- Multi-signature requirement for critical operations
- Time-locked commands (execute at future timestamp)
- Batch command execution
- Command templates for common operations
- Automated response to threat patterns
- Integration with external authentication systems

---

**Sovereign Seal:** HMV-SOV-20251003-ALL  
**System Status:** Operational  
**Security Level:** Maximum

System is sovereign. Collapse-resistant. Unstoppable.
