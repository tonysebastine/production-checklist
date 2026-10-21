# Database Reliability Checklist

- [ ] Schema changes use version-controlled migrations.
- [ ] High-risk migrations are tested with production-like data volume and rollback/forward-fix plans.
- [ ] Multi-step writes use transactions and explicit error handling.
- [ ] Counters, inventory, balances, and state transitions use atomic updates, locks, or optimistic concurrency.
- [ ] Idempotency/deduplication protects retried mutations and webhook processing.
- [ ] Foreign keys and frequently filtered/sorted columns have appropriate indexes.
- [ ] Query plans and slow-query metrics are reviewed; N+1 patterns are tested.
- [ ] Connection pools and maximum connection budgets are configured for all replicas/workers.
- [ ] Runtime database roles have least privilege; migration roles are separate.
- [ ] Tenant isolation is tested; RLS is used where supported and appropriate.
- [ ] Query, statement, lock, and idle-transaction timeouts are configured.
- [ ] Backup/PITR and restore tests meet RPO/RTO.