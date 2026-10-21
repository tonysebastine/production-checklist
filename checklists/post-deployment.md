# Post-deployment Checklist

- [ ] Confirm deployed commit, artifact digest, configuration, and migration version.
- [ ] Verify liveness and readiness endpoints.
- [ ] Run smoke tests for authentication, critical reads/writes, and integrations.
- [ ] Confirm error rate, latency, saturation, queue depth, and dependency health remain within thresholds.
- [ ] Verify secrets and sensitive personal data are not emitted in logs.
- [ ] Confirm scheduled jobs and queue consumers are running.
- [ ] Verify backups continue after deployment and the latest backup is valid.
- [ ] Review dashboards and alerts during the agreed observation window.
- [ ] Record outcome, anomalies, rollback decision, and follow-up owners.