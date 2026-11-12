# Security Features Implementation Prompts

This directory provides structured, actionable AI prompts designed to guide developers and engineering teams when implementing core security controls, features, and verification systems across modern applications and infrastructure.

## Prompt Structure
Each area includes prompt templates covering:
1. **Requirements & Threat Modeling** – Scoping threats, trust boundaries, and attack vectors.
2. **Implementation & Code Generation** – Concrete code, configuration patterns, and defensive implementations.
3. **Validation & Automated Testing** – Test cases, penetration testing checklists, and CI/CD validation.

---

## Documentation & Agent Guides
- [**Antigravity IDE Workflow Guide (`ANTIGRAVITY-IDE-GUIDE.md`)**](ANTIGRAVITY-IDE-GUIDE.md): How to use slash commands (`/plan`, `/goal`, `/grill-me`), workspace rules, and prompts inside Antigravity IDE.
- [**Agent Execution Protocol (`AGENT-GUIDE.md`)**](AGENT-GUIDE.md): System instructions, security invariants, technology matrices, and execution lifecycle for AI agents implementing these prompts.
- [**Antigravity Workspace Rules (`.gemini/rules/security-rules.md`)**](../.gemini/rules/security-rules.md): Native rule file automatically enforced by Antigravity IDE in this workspace.
- [**Prompt Authoring Template**](../templates/security-feature-prompt-template.md): Standard template to author new security prompts for AI coding agents.

## Security Domains & Implementation Areas

| Area Directory | Scope & Implementation Topics | Prompt Guide |
|---|---|---|
| [`01-authentication-and-sessions/`](01-authentication-and-sessions/) | MFA, passkeys/WebAuthn, OAuth2/OIDC, password hashing (Argon2id), session lifecycle, JWT revocation | [README](01-authentication-and-sessions/README.md) |
| [`02-authorization-and-access-control/`](02-authorization-and-access-control/) | RBAC, ABAC, multi-tenant row-level security (RLS), IDOR/BOLA prevention, API gatekeepers | [README](02-authorization-and-access-control/README.md) |
| [`03-input-validation-and-sanitization/`](03-input-validation-and-sanitization/) | Schema validation, SQLi/NoSQLi prevention, XSS mitigation, file upload verification & sandbox | [README](03-input-validation-and-sanitization/README.md) |
| [`04-cryptography-and-secrets-management/`](04-cryptography-and-secrets-management/) | Encryption at rest (AES-GCM/KMS), TLS/HSTS in transit, envelope encryption, secrets rotation, vault integration | [README](04-cryptography-and-secrets-management/README.md) |
| [`05-api-security-and-rate-limiting/`](05-api-security-and-rate-limiting/) | Token-bucket/sliding-window rate limiting, DDoS defense, webhook HMAC verification, SSRF controls | [README](05-api-security-and-rate-limiting/README.md) |
| [`06-security-headers-and-cors/`](06-security-headers-and-cors/) | Content Security Policy (CSP), strict CORS, HSTS, frame options, cookie security flags | [README](06-security-headers-and-cors/README.md) |
| [`07-audit-logging-and-monitoring/`](07-audit-logging-and-monitoring/) | Tamper-evident audit logs, PII masking/redaction, SIEM integration, alerting on suspicious activity | [README](07-audit-logging-and-monitoring/README.md) |
| [`08-cicd-and-supply-chain/`](08-cicd-and-supply-chain/) | SAST/DAST, dependency vulnerability scanning, secrets scanning (pre-commit/CI), signed builds/SBOM | [README](08-cicd-and-supply-chain/README.md) |
| [`09-cloud-and-infrastructure-hardening/`](09-cloud-and-infrastructure-hardening/) | Container security, least-privilege IAM, network isolation, VPC egress rules, Kubernetes hardening | [README](09-cloud-and-infrastructure-hardening/README.md) |
| [`10-ai-and-llm-security/`](10-ai-and-llm-security/) | Prompt injection defense, indirect injection mitigation, tool-use sandbox, data leakage prevention | [README](10-ai-and-llm-security/README.md) |
| [`11-document-integrity-and-verification/`](11-document-integrity-and-verification/) | Tamper-evident invoice & document validation, SHA-256 / HMAC hash anchoring, QR verification backend | [README](11-document-integrity-and-verification/README.md) |

---

## How to Use These Prompts
- Select the folder matching your target feature area.
- Copy the implementation prompt into your AI coding assistant (e.g. Antigravity, Claude Code, GitHub Copilot).
- Fill in the placeholders (e.g., `[FRAMEWORK]`, `[LANGUAGE]`, `[DATABASE]`, `[REQUIREMENTS]`).
- Run the generated verification checklist and automated tests prior to production merge.

