# Scripts

This directory is reserved for optional, reviewed audit helpers.

Future scripts must:
- Default to read-only behavior and require explicit opt-in for changes.
- Never print secrets or collect more data than necessary.
- Fail safely and return meaningful exit codes.
- Document supported OS/runtime versions, permissions, side effects, and rollback.
- Include tests and sample output with sensitive values redacted.
- Never assume hostnames, IPs, gateways, paths, or service names.
## Audit engine

The initial scanner lives in `audit_engine/audit.py`. It is read-only with respect to the target directory and writes reports only when explicit output paths are provided. It uses heuristics, redacts potential secret values, and must not be described as a full SAST tool or proof of production readiness. Run its unit tests with `python -m unittest discover -s tests -v`.
