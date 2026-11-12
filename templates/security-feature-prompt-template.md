# Prompt Template: Security Feature Implementation

Use this standard template when drafting new security feature implementation prompts for AI agents.

---

```markdown
# Context
[Describe the business domain, architecture, current tech stack, and the security problem being solved. Mention specific standards such as OWASP ASVS, NIST SP 800-63B, SOC 2, or HIPAA where relevant.]

# Objective
[State the exact deliverable the AI agent must construct, refactor, or harden. Be explicit about expected layers: middleware, service, repository, or infrastructure definition.]

# Requirements
1. **Security Invariants & Boundary Enforcement:**
   - [Define what must never fail or be bypassed: e.g., server-side checks, least privilege, zero client trust.]
2. **Cryptographic & Protocol Standards:**
   - [Specify exact algorithms, key sizes, primitives, or RFC standards (e.g. AES-256-GCM, Argon2id, RFC 6238 TOTP, SHA-256).]
3. **Data Integrity & Timing Defense:**
   - [Specify constant-time comparison (e.g. hmac.compare_digest), anti-replay windows, nonce tracking.]
4. **Error Handling & Information Disclosure:**
   - [Specify uniform error codes, preventing user enumeration or internal stack trace leakage.]

# Code Quality & Tooling
- [Specify language version, typing requirements (e.g. Python 3.10+ types, TypeScript strict mode), validation libraries (Pydantic, Zod), and architectural layers.]

# Output Expected
Provide:
1. Complete data models / schemas.
2. Production-ready implementation with defensive error handling.
3. Automated unit and integration test suite demonstrating positive flows and negative security attack scenarios.
```

