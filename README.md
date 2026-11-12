# Production Checklist

A practical, technology-agnostic production-readiness checklist for applications, APIs, databases, infrastructure, and operations.

> This repository is a checklist and starter framework, not a guarantee of security or compliance. Validate controls against the real architecture and threat model.

## How to use
1. Copy the relevant checklist into a release/change record.
2. Mark each control **Pass**, **Fail**, **N/A**, or **Not Verified**.
3. Record evidence, owner, severity, and due date for each gap.
4. Never mark a control Pass without current evidence.
5. Run destructive checks only in an authorized environment with an approved rollback plan.

## Checklists
- [Pre-deployment](checklists/pre-deployment.md)
- [Post-deployment](checklists/post-deployment.md)
- [Security hardening](checklists/security-hardening.md)
- [Exhaustive production-readiness audit](checklists/exhaustive-production-readiness.md)
- [Server health](checklists/server-health.md)
- [Backup and restore](checklists/backup-and-restore.md)
- [Database reliability](checklists/database.md)
- [Networking and TLS](checklists/networking-and-ssl.md)
- [Monitoring and alerting](checklists/monitoring-and-alerting.md)
- [Rollback and disaster recovery](checklists/rollback-and-disaster-recovery.md)

## Security Feature Implementation Prompts
Ready-to-use AI prompts to implement, harden, and test production security features:
- [Security Features Implementation Prompts Overview](security-features-implementation-prompts/README.md)
  - [01 - Authentication & Sessions](security-features-implementation-prompts/01-authentication-and-sessions/README.md)
  - [02 - Authorization & Access Control](security-features-implementation-prompts/02-authorization-and-access-control/README.md)
  - [03 - Input Validation & Sanitization](security-features-implementation-prompts/03-input-validation-and-sanitization/README.md)
  - [04 - Cryptography & Secrets Management](security-features-implementation-prompts/04-cryptography-and-secrets-management/README.md)
  - [05 - API Security & Rate Limiting](security-features-implementation-prompts/05-api-security-and-rate-limiting/README.md)
  - [06 - Security Headers & CORS](security-features-implementation-prompts/06-security-headers-and-cors/README.md)
  - [07 - Audit Logging & Monitoring](security-features-implementation-prompts/07-audit-logging-and-monitoring/README.md)
  - [08 - CI/CD & Supply Chain Security](security-features-implementation-prompts/08-cicd-and-supply-chain/README.md)
  - [09 - Cloud & Infrastructure Hardening](security-features-implementation-prompts/09-cloud-and-infrastructure-hardening/README.md)
  - [10 - AI & LLM Security](security-features-implementation-prompts/10-ai-and-llm-security/README.md)
  - [11 - Document Integrity & Verification](security-features-implementation-prompts/11-document-integrity-and-verification/README.md)

## Templates
- [Release readiness](templates/release-checklist.md)
- [Incident report](templates/incident-report.md)
- [Change record](templates/change-record.md)

## Status definitions
| Status | Meaning |
|---|---|
| Pass | Verified with reproducible evidence |
| Fail | Control is absent, broken, or insufficient |
| N/A | Not applicable; rationale recorded |
| Not Verified | Evidence is missing or verification is incomplete |

## Priority definitions
- **Critical:** risk of sensitive-data exposure, takeover, major data loss, or outage.
- **High:** serious security, integrity, or availability risk requiring prompt remediation.
- **Medium:** meaningful operational or defense-in-depth gap.
- **Low:** improvement with limited immediate risk.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).