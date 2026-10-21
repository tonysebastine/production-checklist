# Security Hardening Checklist

## Identity and authorization
- [ ] Enforce least privilege for users, services, database roles, cloud IAM, and CI tokens.
- [ ] Check authorization server-side on every sensitive operation.
- [ ] Test IDOR/BOLA with at least two users and two tenants.
- [ ] Require MFA for privileged access where supported.
- [ ] Define session inactivity, absolute lifetime, rotation, and revocation behavior.

## Application and API
- [ ] Validate payloads server-side against schemas, size limits, and business rules.
- [ ] Encode output by context; sanitize intentionally supported rich text.
- [ ] Use CSRF defenses for cookie-authenticated state changes.
- [ ] Apply SSRF controls: scheme/host allowlists, redirect restrictions, and private/link-local IP blocking.
- [ ] Apply per-IP and per-account limits to login, reset, signup, and expensive endpoints.
- [ ] Configure CSP, HSTS, X-Content-Type-Options, frame restrictions, and Referrer-Policy.
- [ ] Verify webhook signatures against raw request bodies and deduplicate events.
- [ ] Validate uploads by content signature; isolate storage and processing.
- [ ] Use short-lived signed URLs for private object access where applicable.

## Data, secrets, and AI
- [ ] Enable and test database RLS or equivalent tenant isolation where appropriate.
- [ ] Separate runtime and migration database credentials.
- [ ] Rotate exposed credentials and remove them from active artifacts/history where appropriate.
- [ ] Enable secret scanning and dependency scanning in CI.
- [ ] Define data classification, retention, deletion, and audit-log access policies.
- [ ] Treat prompts, retrieved documents, and tool output as untrusted.
- [ ] Keep authorization outside model decisions; validate tool arguments and outputs.
- [ ] Restrict AI tools, network egress, filesystem access, and execution privileges.
- [ ] Set provider spend/token limits without logging secrets.