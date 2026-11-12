# Antigravity IDE Security Rules & Agent System Guidelines

This rule file is automatically loaded by the Antigravity IDE agent whenever working in this repository.

## Non-Negotiable Security Invariants
When implementing, reviewing, or modifying code:
1. **Server-Side Enforcement Only:** Never rely solely on client-side or UI logic for authentication, authorization, or input validation.
2. **Fail Closed:** All access checks must default to DENY. If a policy or database check fails, reject the operation immediately.
3. **Zero Secrets in History or Logs:** Never output or commit real API keys, tokens, or credentials. Always redact sensitive variables from debug output and logs.
4. **Timing-Safe Equality:** Compare all hashes, HMACs, tokens, and credentials using constant-time methods (`hmac.compare_digest` in Python, `crypto.timingSafeEqual` in Node.js).
5. **No Blind Trust in Model Output:** Treat all AI completions, external documents, and user inputs as untrusted data before saving or rendering.

## Prompt Library Reference
When tasked with building or hardening security features in this workspace:
- Reference the specifications located in `security-features-implementation-prompts/`:
  - `01-authentication-and-sessions/`
  - `02-authorization-and-access-control/`
  - `03-input-validation-and-sanitization/`
  - `04-cryptography-and-secrets-management/`
  - `05-api-security-and-rate-limiting/`
  - `06-security-headers-and-cors/`
  - `07-audit-logging-and-monitoring/`
  - `08-cicd-and-supply-chain/`
  - `09-cloud-and-infrastructure-hardening/`
  - `10-ai-and-llm-security/`
  - `11-document-integrity-and-verification/`
- Refer to `security-features-implementation-prompts/AGENT-GUIDE.md` for technology stack conventions and the 4-phase implementation cycle.

## Output Standards for Antigravity Agent
- Deliver clean, modular, production-ready code with strong type hints.
- Always include automated negative tests demonstrating tamper resistance and privilege escalation prevention.

