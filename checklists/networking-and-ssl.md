# Networking and TLS Checklist

- [ ] Public ports and ingress routes are inventoried and justified.
- [ ] TLS certificates are valid, renewed automatically, and monitored before expiry.
- [ ] TLS termination and origin encryption are documented.
- [ ] Enable HSTS only after confirming relevant subdomains support HTTPS.
- [ ] Reverse proxy trusts forwarded headers only from known proxy hops.
- [ ] Admin panels and internal services are not unintentionally public.
- [ ] Egress rules restrict sensitive workloads where feasible.
- [ ] DNS, firewall, NAT, and load-balancer changes have rollback instructions.
- [ ] External/internal reachability tests run from appropriate network vantage points.