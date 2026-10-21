# Monitoring and Alerting Checklist

- [ ] Logs are structured and include request/trace IDs, service, environment, and severity.
- [ ] Tokens, passwords, session cookies, payment data, and sensitive personal data are redacted.
- [ ] Exceptions are captured centrally with release and environment context.
- [ ] Metrics cover request rate, error rate, latency percentiles, saturation, and dependency health.
- [ ] Alerts have severity, owner, runbook, and actionable thresholds.
- [ ] Queue age/depth, retries, dead-letter volume, and scheduled-job failures are monitored.
- [ ] Alerts are tested and routed to a monitored destination.
- [ ] Dashboards separate production from staging and support release comparisons.
- [ ] Log retention, access, and deletion policies are implemented.