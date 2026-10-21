# Backup and Restore Checklist

- [ ] Identify data, configuration, keys, and artifacts requiring backup.
- [ ] Define RPO/RTO and retention by data class.
- [ ] Backups are encrypted in transit and at rest.
- [ ] Backup credentials are separate from production runtime credentials.
- [ ] At least one copy is isolated or immutable where feasible.
- [ ] Monitor backup age, duration, size, and failure status.
- [ ] Restore into an isolated environment on a defined schedule.
- [ ] Validate restored application consistency, permissions, and encryption keys.
- [ ] Document point-in-time recovery and recovery ordering.
- [ ] Record restore-test evidence, elapsed time, issues, and corrective actions.