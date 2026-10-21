# Rollback and Disaster Recovery Checklist

- [ ] Define service-level objectives, RPO, RTO, and incident command roles.
- [ ] Document recovery for application, database, object storage, DNS, and identity-provider outages.
- [ ] Maintain known-good deployable artifacts and configuration versions.
- [ ] Confirm schema/data changes are rollback-compatible or have a forward-fix plan.
- [ ] Test rollback without relying on the failed deployment path.
- [ ] Document host/region failover prerequisites, DNS behavior, and dependencies.
- [ ] Test restoration and failover periodically; record actual RTO/RPO.
- [ ] Maintain emergency contacts and provider escalation paths.
- [ ] Complete post-incident reviews with owners and due dates.