# Audit Logging & Monitoring Implementation Prompts

Use this specification to implement structured security event telemetry, automatic PII redaction, immutable audit trails, and security monitoring triggers.

---

## 1. Context Setting
```markdown
# Context
We are implementing security telemetry, compliance audit logging, and suspicious activity detection for [APPLICATION/SERVICE] in [LANGUAGE/FRAMEWORK] delivering logs to [SIEM / LOG STORE (e.g. Datadog, CloudWatch, PostgreSQL, Elasticsearch)]. The application must satisfy SOC 2, ISO 27001, and HIPAA audit requirements for tracking privileged access and data mutations.
```

---

## 2. Objective
```markdown
# Objective
Create a tamper-evident audit logging and security monitoring subsystem that records high-fidelity security events across authentication, authorization, and data access workflows, scrubs PII/secrets automatically, and alerts on anomalous patterns in real time.
```

---

## 3. Requirements

### A. Structured Security Event Schema
1. **Event Fields:** Standardize all security logs in JSON format with fields:
   - `timestamp`: ISO 8601 UTC timestamp.
   - `event_id`: Unique UUIDv4.
   - `event_type`: Categorized enum (e.g., `auth.login.success`, `auth.mfa.failed`, `access.denied`, `data.export`).
   - `severity`: `INFO`, `WARNING`, `CRITICAL`.
   - `actor`: `{ user_id, session_id, role, ip_address, user_agent }`.
   - `target`: `{ resource_type, resource_id, tenant_id }`.
   - `status`: `SUCCESS` or `FAILURE`.
   - `metadata`: Key-value map of contextual data.

### B. Core Security Events Scope
1. **Authentication:** Login success/failure, logout, MFA prompts/failures, password resets, token refresh.
2. **Access & Authorization:** Unauthorized resource attempts (HTTP 403), role escalations, permission grants/revocations.
3. **Data Operations:** Bulk customer record exports, sensitive PII reads, data deletion operations.
4. **Administrative & Config:** Creation/revocation of API keys, changes to security policies, webhook endpoint modifications.

### C. Automatic PII & Secret Redaction
1. **Scrubbing Pipeline:** Intercept and recursively scrub log objects before serialization.
2. **Key Masking:** Automatically replace values of keys matching `password`, `token`, `secret`, `authorization`, `credit_card`, `cvv`, `ssn`, `api_key` with `[REDACTED]`.
3. **Regex Pattern Scrubbing:** Scrub credit card numbers, JWT patterns (`ey...`), and high-entropy API key formats appearing inside string messages.

### D. Immutability & Tamper Resistance
1. **Append-Only Guarantees:** Ensure log destinations prevent modification or deletion. If writing to database tables, use database rules or triggers disallowing `UPDATE` and `DELETE`.
2. **Hash-Chaining (Optional):** Maintain a running SHA-256 hash linking each event to the prior event record for cryptographically verifiable audit trails.

### E. Real-Time Alert Triggers
1. Alert immediately on:
   - 5+ failed login attempts for a single account or IP within 60 seconds.
   - Any access attempt with a mismatched `tenant_id`.
   - Creation of new superadmin/owner credentials.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Asynchronous, non-blocking logger to prevent latency impact on user requests.
- Async context propagation (AsyncLocalStorage / contextvars) for automatic actor/request ID injection.
- Security unit tests verifying redaction efficacy and append-only constraints.
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. Structured audit logger service with automated PII masking pipeline.
2. Append-only audit log storage schema (SQL migration with triggers or cloud destination).
3. Context-propagation middleware capturing IP, User-Agent, and Actor ID.
4. Test suite verifying that secrets are never logged in plaintext and that table updates are rejected.
```

