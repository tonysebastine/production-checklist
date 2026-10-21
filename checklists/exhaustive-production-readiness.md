# Exhaustive Production-Readiness Audit Checklist

Use this checklist to audit an actual application repository against its implementation, configuration, tests, and deployment architecture. It is a control register, not a substitute for code review, threat modeling, or penetration testing.

## Audit rules

1. Inspect the full repository, including hidden files, workflow definitions, lockfiles, environment examples, route handlers, middleware, schemas, migrations, infrastructure-as-code, containers, tests, and deployment scripts.
2. Search the repository for every control below. Trace relevant code paths rather than relying on filenames or documentation alone.
3. For every finding, record the exact file path, line range or symbol, route/job/schema/configuration, and a concise evidence excerpt. Include test evidence where possible.
4. Use only these statuses: **Implemented**, **Partial**, or **Missing**. Use **N/A** only with a written rationale in the evidence field. When evidence is unavailable, use **Missing — not evidenced** rather than guessing.
5. Never mark a control Implemented solely because a README or checklist says it exists. Verify configuration and behavior; test negative cases.
6. Prioritize by actual impact and exploitability. Critical means likely severe data exposure, account takeover, material data corruption, or major outage. High means substantial security, integrity, or availability risk.
7. Do not assert a specific vulnerability or endpoint is exploitable unless code evidence or a reproducible test supports that conclusion.
8. Redact credentials, personal data, tokens, and sensitive production values from reports. Never copy secrets into issues or audit artifacts.
9. Record assumptions, scope exclusions, repository commit SHA, branch, date, auditor, runtime/framework versions, deployment target, and tests executed.
10. For every Missing or Partial Critical/High control, create a remediation task with owner, severity, acceptance criteria, and target date.

## Required evidence matrix

For every control, produce a row using exactly these columns:

| Category | Requirement | Current Status (Implemented / Partial / Missing) | File(s) / Evidence Found | Priority (Critical / High / Medium / Low) |
|---|---|---|---|---|

In the evidence column, cite exact paths and symbols/line ranges when available. Explain what was found and what remains unverified. If a control is not applicable, state why and identify who approved the exception.

## 1. Security and data protection

| ID | Requirement | Evidence to inspect / verification |
|---|---|---|
| SEC-01 | Row-Level Security (RLS) | Database policies, tenant/user scoping, migration definitions, runtime DB roles; test cross-tenant reads and writes and verify privileged-role behavior. |
| SEC-02 | Server-side validation | All route handlers, DTO/schema validators, query/path/body parsing, size limits, content types, and business invariants; test malformed and boundary inputs. |
| SEC-03 | Secret exposure | Repository history, environment files, client bundles, public/static directories, logs, CI artifacts, build output, and secret scanning; rotate exposed credentials. |
| SEC-04 | Authorization and access control | Middleware and per-action permission checks; test anonymous, ordinary-user, tenant-admin, and privileged access. |
| SEC-05 | IDOR / BOLA | Routes accepting IDs/UUIDs, ownership checks, exports, nested resources, attachments, and bulk operations; test cross-user and cross-tenant object access. |
| SEC-06 | XSS protection | Output encoding, sanitization, template escaping, CSP, rich-text/markdown rendering, DOM sinks, and stored/reflected/DOM XSS tests. |
| SEC-07 | CSRF protection | Cookie authentication, SameSite/Secure/HttpOnly settings, anti-CSRF tokens or origin checks, and state-changing requests from hostile origins. |
| SEC-08 | SSRF protection | Server-side URL fetchers, webhook testers, importers, image/document fetches; enforce scheme/host allowlists, DNS/IP validation, redirect checks, and block internal/metadata ranges. |
| SEC-09 | Secure file uploads | Size limits, magic-byte and MIME checks, extension normalization, random storage names, isolated storage, malware scanning, archive/path traversal protections, and safe download headers. |
| SEC-10 | Signed URLs | Private buckets by default, short expiry, method/object scope, upload constraints, ownership authorization, and no public listing or permanent public object URLs. |
| SEC-11 | Session expiration and revocation | Idle/absolute expiry, refresh rotation, reuse detection, logout revocation, password-change invalidation, cookie flags, and session fixation tests. |
| SEC-12 | Least privilege | IAM policies, database roles, service accounts, container privileges, filesystem permissions, CI token scopes, and production/staging separation. |
| SEC-13 | Security headers | CSP, HSTS where HTTPS is enforced, X-Content-Type-Options, Referrer-Policy, frame protection, Permissions-Policy where appropriate; verify actual responses. |
| SEC-14 | AI safety / prompt injection | LLM integrations, tool permissions, untrusted-content separation, prompt-injection tests, structured output validation, data-loss controls, sandboxing, and human approval for consequential actions. |
| SEC-15 | Dependency vulnerabilities | Package manifests and lockfiles, supported runtimes, automated dependency scans, update policy, SBOM where appropriate, and documented risk exceptions. |

## 2. Data integrity and database architecture

| ID | Requirement | Evidence to inspect / verification |
|---|---|---|
| DB-01 | Transactions | Multi-step mutation flows, transaction boundaries, rollback paths, constraints, and failure-injection tests. |
| DB-02 | Race-condition mitigation | Shared counters/inventory/balances/status transitions; row locks, optimistic versions, atomic updates/upserts, and concurrent-request tests. |
| DB-03 | Idempotency | State-changing APIs, order/payment flows, task submission and webhook handlers; persistent idempotency keys, request fingerprinting, result replay, and expiry policy. |
| DB-04 | Indexing | Schema and query plans; indexes for joins, foreign keys, filters, sorts, and JSON/full-text queries; confirm with EXPLAIN and workload evidence. |
| DB-05 | N+1 query prevention | ORM access patterns, loops that query per item, serialization hooks, eager loading, batching, joins, and query-count tests. |
| DB-06 | Connection pooling | Driver/ORM pool settings, pooler configuration, maximum connection budget across replicas/workers, timeout behavior, and saturation tests. |
| DB-07 | Database migrations | Version-controlled migrations, reproducible clean setup, backup/rollback strategy, backward-compatible expand/contract releases, and migration CI checks. |

## 3. Reliability, resilience, and background processing

| ID | Requirement | Evidence to inspect / verification |
|---|---|---|
| REL-01 | Background jobs | Long-running emails, exports, media processing, imports, AI calls, and external operations; durable queues, worker supervision, and bounded job execution. |
| REL-02 | Timeouts and circuit breakers | Outbound HTTP, database, cache, LLM, and third-party clients; explicit connect/read/total timeouts, cancellation, pool timeouts, and breaker behavior where useful. |
| REL-03 | Retries and backoff | Transient failures only, bounded attempts, exponential backoff with jitter, retry budgets, idempotency, and avoidance of retry storms. |
| REL-04 | Dead-letter queue | Failed-job retention, inspect/replay tools, alerting, operator ownership, and policy against silently discarding jobs. |
| REL-05 | Cache invalidation | Explicit TTLs, mutation-triggered purge/invalidation, versioned keys, tenant-safe cache keys, and stale-data tests. |
| REL-06 | Rate limiting | Per-IP and per-user/account limits on login, password reset, OTP, expensive public APIs, AI calls, and uploads; shared/distributed limits where multiple instances run. |
| REL-07 | Payment webhook verification | Cryptographic signature and timestamp validation, raw-body requirements, replay protection, duplicate event handling, out-of-order events, durable processing, and reconciliation. Mark N/A only if payment/webhooks are absent. |

## 4. Observability, deployment, and infrastructure

| ID | Requirement | Evidence to inspect / verification |
|---|---|---|
| OPS-01 | Structured logging | JSON logs, timestamps, severity, request/trace IDs, actor/tenant identifiers where safe, log levels, and redaction of credentials and personal data. |
| OPS-02 | Error monitoring | Central exception capture, useful stack traces, release/environment tags, sampling, alert routing, and PII scrubbing. |
| OPS-03 | Health and readiness | Separate liveness/readiness endpoints such as /live, /ready, and /healthz with documented semantics; dependency checks should not make liveness restart-loop on transient dependency failures. |
| OPS-04 | Alerting and thresholds | Actionable alerts for error rate, latency percentiles, saturation, queue age/backlog, database capacity, certificate expiry, backup failure, and synthetic checks. |
| OPS-05 | Rollback and zero downtime | Rolling/blue-green or safe restart, graceful shutdown, readiness gating, backward-compatible migrations, artifact/version pinning, rollback triggers, and rehearsed rollback. |
| OPS-06 | Feature flags | Runtime controls for risky features, safe defaults, authorization, audit trail for sensitive toggles, cleanup ownership, and failure behavior if the flag provider is unavailable. |
| OPS-07 | Automated backups and restore tests | Backup schedule, encryption, off-host/isolated copies, PITR where supported, retention, alerting, documented restore procedure, and timed restore drills. |
| OPS-08 | Staging environment | Production-like topology and versions, synthetic/non-production data, secret separation, migration validation, and deployment smoke tests. |
| OPS-09 | Disaster recovery | Defined RPO/RTO, failure scenarios, failover and DNS/runbook steps, dependency inventory, contact ownership, and periodic tabletop/live exercises. |
| OPS-10 | Cost monitoring | Budgets and alerts, quotas, rate limits, AI token/query caps, storage/egress controls, per-tenant attribution where useful, and runaway-cost tests. |
| OPS-11 | Data retention and deletion | Retention schedule by data class, log rotation, soft-delete purge, backup expiry, user deletion/export workflows, legal holds, and verifiable scheduled cleanup. |

## 5. Testing and user experience

| ID | Requirement | Evidence to inspect / verification |
|---|---|---|
| TEST-01 | E2E and contract tests | Core user journeys, API schemas/contracts, auth and authorization negative cases, webhook contracts, migration tests, and CI execution. |
| TEST-02 | Mobile and cross-browser | Responsive viewports, touch/keyboard interaction, supported browser matrix, slow-network performance, and mobile-specific E2E runs. |
| TEST-03 | Accessibility | Semantic HTML, keyboard-only operation, visible focus, labels, contrast, error announcements, screen-reader checks, reduced motion, and automated plus manual WCAG-oriented review. |

## Critical/high deficiency report

For every Missing or Partial item with Critical or High priority, include:

- **Finding ID and title**
- **Status and severity**
- **Evidence:** exact path, line range/symbol, endpoint, job, schema, policy, or workflow
- **Observed behavior:** distinguish proven behavior from inference
- **Risk and impact:** affected assets, trust boundary, attack preconditions, and likely consequence
- **Reproduction/test:** safe steps in a controlled environment, with expected and actual outcomes
- **Remediation:** concrete code/configuration changes
- **Acceptance criteria:** testable proof the issue is fixed
- **Owner, due date, and residual risk**

Do not invent file paths, endpoints, or line numbers. If no application code is present, report that runtime controls cannot be verified and ask for the actual application repository.

## Phased remediation roadmap

### Phase 1 — Immediate triage: security and data integrity

1. Confirm scope, commit SHA, framework, ORM, database, tenancy, authentication, hosting, and sensitive-data inventory.
2. Review exposed secrets and rotate credentials if exposure is confirmed.
3. Add secret and dependency scanning to CI.
4. Fix authorization, tenant isolation, IDOR/BOLA, server-side validation, session controls, upload safety, SSRF/CSRF/XSS, and security headers.
5. Add transactions, constraints, idempotency, and concurrency protection to high-impact mutations.
6. Test cross-tenant access and privilege escalation with negative tests.

**Exit gate:** no unresolved Critical findings; any exception is explicitly approved, time-bound, and has compensating controls.

### Phase 2 — Core resilience and scaling

1. Set connection pool budgets and database/query timeouts.
2. Review query plans, indexing, N+1 behavior, and database load.
3. Add concurrency control and durable idempotency.
4. Introduce queues for long-running tasks, with retries, jitter, DLQ, and replay controls.
5. Configure outbound timeouts and suitable circuit breakers.
6. Define cache TTLs and deterministic invalidation.

**Exit gate:** concurrency/load tests pass; failure/retry behavior is bounded and observable; queue failures are recoverable.

### Phase 3 — Operational excellence and observability

1. Implement structured, redacted logs and request/trace correlation.
2. Add error monitoring, service metrics, traces, dashboards, and alert routing.
3. Implement liveness/readiness and dependency health checks.
4. Configure rate limits for authentication and expensive/public routes.
5. Add staging deployment gates, safe shutdown, health-checked rollout, and rollback.
6. Exercise alerting and rollback procedures.

**Exit gate:** operational alerts and rollback have reproducible test evidence; staging release checks pass.

### Phase 4 — Hardening and compliance

1. Add E2E, contract, accessibility, browser, and mobile tests.
2. Automate backup monitoring and isolated restore drills; validate RPO/RTO.
3. Implement retention, deletion, audit-log, and privacy workflows.
4. Test disaster-recovery failover and document runbooks.
5. Configure provider budgets, quotas, and AI/API usage caps.
6. Maintain SBOM/dependency review, access reviews, risk exceptions, evidence, and ownership.

**Exit gate:** restore/DR tests meet targets; retention and cost controls are verified; core journeys pass; outstanding risks are accepted by accountable owners.

## Implementation stub guidance

Implementation examples must be tailored only after identifying the real stack. Do not assume TypeScript, Zod, PostgreSQL, Prisma, Supabase, AWS, or a particular host without repository evidence.

For the top three urgent gaps, provide tested, stack-specific patches or snippets for:

1. Server-side validation plus authorization and tenant scoping.
2. Database transaction/RLS or equivalent isolation, with concurrency and cross-tenant tests.
3. Secret scanning and dependency scanning in CI, using reviewed action versions and correct permissions.

Each stub must identify its target file, required dependencies/configuration, failure behavior, tests, and deployment caveats. Label pseudocode clearly and never present it as a verified fix.

## Final report structure

1. Executive summary and scope/limitations.
2. Repository and technology inventory with inspected commit SHA.
3. Full evidence matrix containing every control ID above.
4. Critical/high findings with precise file and endpoint evidence.
5. Four-phase remediation plan with owners, sequencing, estimates, and exit gates.
6. Three stack-specific implementation stubs or patches.
7. Tests and commands executed, results, and unverified areas.
8. Residual risks, assumptions, N/A decisions, and next actions.
