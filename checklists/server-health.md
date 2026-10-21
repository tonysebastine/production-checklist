# Server Health Checklist

- [ ] CPU, memory, disk, inode, file descriptor, and network saturation are monitored.
- [ ] OS and runtime security updates have a defined cadence.
- [ ] SSH/admin access is restricted, logged, and protected against brute force.
- [ ] Firewall rules are documented and reviewed; unused ports are closed.
- [ ] Services run as non-root users where feasible.
- [ ] systemd/container restart policies and resource limits are configured.
- [ ] Logs rotate and have disk-use limits.
- [ ] Time synchronization is healthy.
- [ ] Health checks distinguish process liveness from dependency readiness.
- [ ] Capacity thresholds and on-call escalation paths are documented.