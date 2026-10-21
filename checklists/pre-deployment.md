# Pre-deployment Checklist

## Release and change control
- [ ] Scope, owner, approver, maintenance window, and customer impact are documented.
- [ ] Release record identifies the exact source revision and artifact.
- [ ] Release notes and known limitations are published.
- [ ] Rollback criteria, steps, and authorized decision-maker are explicit.
- [ ] Configuration and schema changes remain compatible with the rollback version.

## Security and privacy
- [ ] Every externally reachable mutation endpoint validates input server-side.
- [ ] Server-side authorization is enforced for every object and action.
- [ ] Tenant/user scoping is enforced in queries; database RLS is enabled where appropriate.
- [ ] Secrets are absent from source, logs, artifacts, client bundles, and public files.
- [ ] Authentication, session expiry/revocation, CSRF, XSS, SSRF, and rate limits are tested as applicable.
- [ ] Security headers and TLS settings are verified against the deployment topology.
- [ ] Dependencies and images are scanned; critical/high findings have approved dispositions.
- [ ] Uploads and outbound URL fetches have strict type, size, and target restrictions.
- [ ] AI inputs are untrusted; model outputs are validated before privileged actions.

## Data integrity
- [ ] Migrations are version-controlled, reproducible, and tested with representative data.
- [ ] Multi-step mutations use transactions or documented compensating actions.
- [ ] Concurrency and duplicate-request behavior are tested.
- [ ] Indexes and query plans cover high-volume access patterns.
- [ ] Backup freshness and restore-test evidence are current.

## Testing and operations
- [ ] Unit, integration, contract, and critical E2E tests pass.
- [ ] Accessibility and supported mobile/browser viewports are checked.
- [ ] Logs, metrics, traces, alerts, and dashboards are ready.
- [ ] Health/readiness checks reflect actual dependencies.
- [ ] Capacity, timeout, retry, and rate-limit behavior are tested.
- [ ] Staging is representative enough for the release.