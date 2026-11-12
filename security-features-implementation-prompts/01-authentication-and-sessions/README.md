# Authentication & Sessions Implementation Prompts

Use this specification to implement resilient, standards-compliant authentication workflows, password security, multi-factor authentication (MFA), and secure session/token lifecycles.

---

## 1. Context Setting
```markdown
# Context
We are implementing an enterprise-grade authentication and session management layer for [APPLICATION/SERVICE] in [LANGUAGE/FRAMEWORK] with [DATABASE/CACHE (e.g., PostgreSQL, Redis)]. The system must protect against credential stuffing, brute-force attacks, session hijacking, token theft, and user enumeration, strictly adhering to OWASP ASVS v4.0 (Level 2/3) and NIST SP 800-63B standards.
```

---

## 2. Objective
```markdown
# Objective
Create a hardened authentication service and session lifecycle manager that handles user registration, password hashing with Argon2id, multi-factor authentication (TOTP + encrypted recovery codes), session/refresh token rotation with token family reuse detection, and proactive revocation across devices.
```

---

## 3. Requirements

### A. Password Security & Account Protection
1. **Password Hashing:** Hash passwords using Argon2id (`memory_cost=65536` [64MB], `time_cost=3`, `parallelism=1`) with a unique cryptographically random 16-byte salt per user. Fall back to bcrypt (`cost=12`) or PBKDF2 (`iterations=600000`) only if environment constraints apply.
2. **Password Validation:** Enforce minimum length of 12+ characters, check against common breach corpuses / dictionary attacks, and avoid arbitrary character composition rules that degrade entropy.
3. **Timing Attack Neutralization:** Ensure failed authentication attempts run in constant time regardless of whether the email/username exists.

### B. Multi-Factor Authentication (MFA / TOTP)
1. **Secret Generation:** Generate cryptographically secure base32 secrets (RFC 6238). Encrypt secrets at rest in storage.
2. **Setup & QR Code:** Provide provisioning URI `otpauth://totp/{issuer}:{email}?secret={secret}&issuer={issuer}` and high-contrast QR code generation.
3. **Validation & Anti-Replay:** Verify 6-digit TOTP code within a ±1 step drift window (30s). Record the last validated timestep in Redis/DB to block replay attacks.
4. **Recovery Codes:** Generate 10 single-use, 10-character alphanumeric backup codes. Store only hashed versions (SHA-256 or bcrypt) in the database.

### C. Session & Refresh Token Lifecycle
1. **Cookie-Based Sessions:** Store session identifiers in cookies with `HttpOnly; Secure; SameSite=Strict; Path=/` and `__Host-` prefix. Rotate session ID upon privilege changes or login.
2. **JWT & Refresh Token Rotation:**
   - Access token: Short-lived (5–15 minutes).
   - Refresh token: Cryptographically secure random opaque string (7–30 days) stored as a hash alongside a `family_id` and `is_revoked` flag.
   - On refresh: Invalidate current refresh token, issue a new access token and new refresh token in the same family.
   - **Reuse Detection:** If an already-used refresh token is presented, immediately revoke the entire token family (flagging token theft) and alert the user.
3. **Revocation & Logout:** Provide `/logout` (current session) and `/logout-all-devices` (invalidates all user sessions/tokens).

### D. Brute-Force & Lockout Defenses
1. Implement rate limiting: Max 5 failed attempts per IP and per username within a 15-minute sliding window.
2. Apply exponential backoff or temporary account lockout with secure self-service unlock.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Modern typed code (e.g., Python 3.10+ type hints / TypeScript strict mode / Go).
- Robust schema validation for payloads (Pydantic / Zod).
- Separation of concerns: Controller/Router -> Service Layer -> Repository/Data Access.
- Comprehensive security unit and integration tests.
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. Complete data models / schemas (User, Session, MFACredential, RefreshTokenFamily).
2. Production-ready implementation of the authentication and session service with all endpoints:
   - `POST /auth/register`
   - `POST /auth/login`
   - `POST /auth/mfa/setup` & `POST /auth/mfa/verify`
   - `POST /auth/refresh`
   - `POST /auth/logout` & `POST /auth/logout-all`
3. Integration test suite demonstrating timing attack prevention, TOTP replay mitigation, and token reuse family revocation.
```

