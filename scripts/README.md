# Scripts

This directory is reserved for optional, reviewed audit helpers.

Future scripts must:
- Default to read-only behavior and require explicit opt-in for changes.
- Never print secrets or collect more data than necessary.
- Fail safely and return meaningful exit codes.
- Document supported OS/runtime versions, permissions, side effects, and rollback.
- Include tests and sample output with sensitive values redacted.
- Never assume hostnames, IPs, gateways, paths, or service names.