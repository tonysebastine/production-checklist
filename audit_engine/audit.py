#!/usr/bin/env python3
"""Read-only heuristic repository audit; matches are clues, not proof."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from typing import Any

SKIP = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", "dist", "build", "coverage", ".next", "vendor", "target"}
SUFFIXES = {".py",".js",".jsx",".ts",".tsx",".mjs",".cjs",".go",".rs",".java",".kt",".php",".rb",".cs",".sql",".prisma",".toml",".yaml",".yml",".json",".xml",".html",".htm",".css",".md",".sh",".bash",".conf",".ini",".env",".tf",".hcl",".properties"}
MAX_BYTES = 1_000_000
# Each regex is only a search hint. A hit is marked Partial pending manual verification.
RAW = [
("SEC-01","Security & Data Protection","Row-Level Security (RLS)","Critical",r"row level security|enable row level security|create policy|tenant_id|organization_id"),
("SEC-02","Security & Data Protection","Server-side validation","Critical",r"zod|joi|yup|pydantic|marshmallow|validate|validator|safeparse|requestmodel"),
("SEC-03","Security & Data Protection","Secret exposure prevention","Critical",r"gitleaks|trufflehog|detect-secrets|secret.scan|\\.env"),
("SEC-04","Security & Data Protection","Authorization and access control","Critical",r"authorize|authorization|permission|requireauth|isadmin|rbac|accesscontrol"),
("SEC-05","Security & Data Protection","IDOR / BOLA protection","Critical",r"owner_id|user_id|tenant_id|authorize.*resource|canaccess|checkownership"),
("SEC-06","Security & Data Protection","XSS protection","Critical",r"content-security-policy|helmet|dompurify|sanitizehtml|escapehtml|autoescape"),
("SEC-07","Security & Data Protection","CSRF protection","High",r"csrf|sameSite|samesite|csrf_token|origin.check"),
("SEC-08","Security & Data Protection","SSRF protection","High",r"allowlist|allow.list|block.private.ip|isprivate|ssrf|safe.url|url.validation"),
("SEC-09","Security & Data Protection","Secure file uploads","High",r"magic.byte|filetype|content.type|clamav|malware|max.file.size|upload.limit"),
("SEC-10","Security & Data Protection","Short-lived signed URLs","High",r"presigned|pre.signed|signed.url|expiresin|expiration"),
("SEC-11","Security & Data Protection","Session expiration and revocation","High",r"refresh.token|session.expiry|session.timeout|revoketoken|rotation|idle.timeout"),
("SEC-12","Security & Data Protection","Least privilege","High",r"least.privilege|readOnlyRootFilesystem|runAsNonRoot|bypassrls|iam.role|permissions:"),
("SEC-13","Security & Data Protection","Security headers","High",r"content-security-policy|strict-transport-security|x-content-type-options|referrer-policy|x-frame-options|permissions-policy"),
("SEC-14","Security & Data Protection","AI safety and prompt injection","High",r"prompt.injection|guardrail|structured.output|tool.allowlist|sandbox|output.schema"),
("SEC-15","Security & Data Protection","Dependency vulnerability scanning","High",r"dependabot|pip-audit|npm audit|osv-scanner|snyk|dependency-review"),
("DB-01","Data Integrity & Database Architecture","Database transactions","Critical",r"transaction|begin|commit|rollback|atomic"),
("DB-02","Data Integrity & Database Architecture","Race-condition mitigation","High",r"for update|optimistic.lock|version column|upsert|serializable|compare.and.swap"),
("DB-03","Data Integrity & Database Architecture","Idempotency","High",r"idempotency.key|idempotent|deduplication|event.id"),
("DB-04","Data Integrity & Database Architecture","Database indexing","Medium",r"create index|@@index|@@unique|gin index|btree|index concurrently"),
("DB-05","Data Integrity & Database Architecture","N+1 query prevention","Medium",r"eager.load|include:|selectinload|prefetch_related|dataloader|joinedload"),
("DB-06","Data Integrity & Database Architecture","Connection pooling","High",r"pool.size|max.connections|pgbouncer|connection.pool|pool_timeout|pool.max"),
("DB-07","Data Integrity & Database Architecture","Versioned database migrations","High",r"alembic|prisma migrate|flyway|liquibase|migration"),
("REL-01","Reliability & Background Processing","Background job queue","Medium",r"celery|bullmq|sidekiq|rq.queue|background.task|worker"),
("REL-02","Reliability & Background Processing","Timeouts and circuit breakers","High",r"timeout|circuit.breaker|AbortSignal.timeout|connect_timeout|read_timeout"),
("REL-03","Reliability & Background Processing","Retry with exponential backoff and jitter","Medium",r"exponential.backoff|backoff|jitter|max.retries|retry.delay"),
("REL-04","Reliability & Background Processing","Dead-letter queue","Medium",r"dead.letter|dlq|failed.jobs|retry.queue"),
("REL-05","Reliability & Background Processing","Cache invalidation","Medium",r"cache.invalidate|invalidate.cache|ttl|expire|purge.cache"),
("REL-06","Reliability & Background Processing","Rate limiting","High",r"rate.limit|slowapi|ratelimit|throttle|limit_req|token.bucket"),
("REL-07","Reliability & Background Processing","Payment webhook verification","High",r"webhook.signature|constructevent|signature.verification|event.id|stripe-signature"),
("OPS-01","Observability, Deployment & Infrastructure","Structured logging","Medium",r"structlog|json.logger|winston|pino|logging.getlogger|trace.id|request.id"),
("OPS-02","Observability, Deployment & Infrastructure","Centralized error monitoring","Medium",r"sentry|opentelemetry|datadog|captureexception|error.monitoring"),
("OPS-03","Observability, Deployment & Infrastructure","Health and readiness probes","High",r"/healthz|/ready|/live|readinessprobe|livenessprobe|health.check"),
("OPS-04","Observability, Deployment & Infrastructure","Alerting and thresholds","High",r"alertmanager|alert.rule|pagerduty|error.budget|latency.threshold|prometheus"),
("OPS-05","Observability, Deployment & Infrastructure","Rollback and zero-downtime deployment","High",r"rolling.update|blue.green|rollback|graceful.shutdown|maxunavailable|deployment.strategy"),
("OPS-06","Observability, Deployment & Infrastructure","Feature flags","Low",r"feature.flag|launchdarkly|unleash|flipper"),
("OPS-07","Observability, Deployment & Infrastructure","Automated backups and restore tests","High",r"point.in.time.recovery|pitr|pg_dump|pgbackrest|restore.test|backup.schedule"),
("OPS-08","Observability, Deployment & Infrastructure","Staging environment","Medium",r"staging|pre.production|environment: staging|deploy.preview"),
("OPS-09","Observability, Deployment & Infrastructure","Disaster recovery plan","High",r"disaster.recovery|rto|rpo|failover|recovery.exercise"),
("OPS-10","Observability, Deployment & Infrastructure","Cost monitoring and usage caps","Medium",r"budget.alert|cost.limit|usage.cap|token.limit|quota|billing.alert"),
("OPS-11","Observability, Deployment & Infrastructure","Data retention and deletion","High",r"retention.policy|data.retention|scheduled.deletion|purge.old|log.rotation|soft.delete"),
("TEST-01","Testing & User Experience","E2E and contract tests","High",r"playwright|cypress|pytest|jest|vitest|contract.test|newman|e2e"),
("TEST-02","Testing & User Experience","Mobile and cross-browser compatibility","Medium",r"viewport|mobile.test|cross.browser|webkit|firefox|device.scale.factor"),
("TEST-03","Testing & User Experience","Accessibility","Medium",r"axe-core|accessibility|aria-label|wcag|lighthouse"),
]
CONTROLS = [{"id":i,"category":c,"requirement":r,"priority":p,"pattern":re.compile(rx,re.I)} for i,c,r,p,rx in RAW]
SECRET_RULES = [
 ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
 ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
 ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
 ("generic-secret-assignment", re.compile(r"""(?i)\b(?:api[_-]?key|secret|access[_-]?token|auth[_-]?token|password)\b\s*[:=]\s*["']?([A-Za-z0-9_./+=-]{20,})""")),
]
PLACEHOLDERS = {"changeme","change_me","replace_me","your_secret_here","example","placeholder","redacted"}

def read_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink() or any(p in SKIP for p in path.parts):
            continue
        if path.suffix.lower() not in SUFFIXES and path.name.lower() not in {".env.example",".env.sample",".env.template","dockerfile"}:
            continue
        try:
            if path.stat().st_size <= MAX_BYTES:
                yield path, path.read_text(encoding="utf-8",errors="replace")
        except OSError:
            continue

def audit(target: Path) -> dict[str, Any]:
    root = target.resolve()
    if not root.is_dir():
        raise ValueError(f"Target is not a directory: {root}")
    files = list(read_files(root))
    corpus = [(p.relative_to(root).as_posix(), txt) for p,txt in files]
    controls = []
    for ctl in CONTROLS:
        evidence = []
        for rel, txt in corpus:
            for n,line in enumerate(txt.splitlines(),1):
                if ctl["pattern"].search(line):
                    evidence.append({"path":rel,"line":n})
                    if len(evidence) == 5: break
            if len(evidence) == 5: break
        controls.append({
            "id":ctl["id"],"category":ctl["category"],"requirement":ctl["requirement"],
            "status":"Partial" if evidence else "Missing","priority":ctl["priority"],
            "evidence":evidence,
            "note":"Heuristic match only; manual review and tests required." if evidence else "No matching evidence found; this does not prove the control is absent."
        })
    secrets = []
    for path,txt in files:
        rel = path.relative_to(root).as_posix()
        for n,line in enumerate(txt.splitlines(),1):
            for rule,pat in SECRET_RULES:
                m = pat.search(line)
                if not m: continue
                value = (m.group(1) if m.lastindex else m.group(0)).strip("\"' ")
                if value.lower() in PLACEHOLDERS or "your_" in value.lower() or "example" in value.lower():
                    continue
                secrets.append({"id":f"SECRET-{len(secrets)+1:03d}","rule":rule,"path":rel,"line":n,"severity":"Critical","message":"Potential secret pattern detected; value redacted. Verify and rotate if exposed."})
                break
    return {
        "schema_version":1,"target":str(root),"scanner":"production-checklist heuristic scanner",
        "limitations":["Static heuristics only; no semantic analysis, runtime testing, or proof of exploitability.","A keyword match is not proof that a control is implemented; no match is not proof of absence.","Text files over 1 MB and common generated/vendor directories are skipped.","Potential secret values are intentionally redacted."],
        "inventory":{"text_files_scanned":len(files),"files":[p.relative_to(root).as_posix() for p,_ in files]},
        "summary":{"controls_total":len(controls),"implemented":0,"partial":sum(c["status"]=="Partial" for c in controls),"missing":sum(c["status"]=="Missing" for c in controls),"potential_secrets":len(secrets)},
        "controls":controls,"potential_secrets":secrets
    }

def to_markdown(result: dict[str, Any]) -> str:
    s=result["summary"]
    lines=["# Automated Production-Readiness Heuristic Report","",f"- Target: {result['target']}",f"- Text files scanned: {result['inventory']['text_files_scanned']}",f"- Controls evaluated: {s['controls_total']}",f"- Heuristic matches (Partial): {s['partial']}",f"- No evidence matched (Missing): {s['missing']}",f"- Potential secret patterns: {s['potential_secrets']}","",
    "> Heuristic triage only, not a security certification. Matches require manual verification; no match does not prove absence.","",
    "| Category | Requirement | Current Status (Implemented / Partial / Missing) | File(s) / Evidence Found | Priority (Critical / High / Medium / Low) |","|---|---|---|---|---|"]
    for c in result["controls"]:
        ev="; ".join(f"{x['path']}:{x['line']}" for x in c["evidence"]) or "No heuristic evidence matched"
        lines.append(f"| {c['category']} | {c['requirement']} | {c['status']} | {ev} — {c['note']} | {c['priority']} |")
    lines.extend(["","## Potential secret detections",""])
    if result["potential_secrets"]:
        lines.extend(["| ID | Rule | Location | Severity |","|---|---|---|---|"])
        for x in result["potential_secrets"]: lines.append(f"| {x['id']} | {x['rule']} | {x['path']}:{x['line']} | {x['severity']} |")
        lines.append("Secret values are not included. Verify securely and rotate confirmed exposed credentials.")
    else: lines.append("No configured secret patterns detected. This does not guarantee that no secrets exist.")
    lines.extend(["","## Limitations",""]+[f"- {x}" for x in result["limitations"]])
    return "\n".join(lines)+"\n"

def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target",nargs="?",default=".",help="Repository directory to scan")
    parser.add_argument("--json",dest="json_path",help="Write JSON report to this path")
    parser.add_argument("--markdown",dest="markdown_path",help="Write Markdown report to this path")
    parser.add_argument("--fail-on-secrets",action="store_true",help="Exit 2 if potential secrets are detected")
    args=parser.parse_args(argv)
    try: result=audit(Path(args.target))
    except (OSError,ValueError) as exc:
        print(f"Audit error: {exc}",file=sys.stderr); return 1
    report=to_markdown(result)
    if args.json_path: Path(args.json_path).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    if args.markdown_path: Path(args.markdown_path).write_text(report,encoding="utf-8")
    if not args.json_path and not args.markdown_path: print(report,end="")
    print(f"Scanned {result['inventory']['text_files_scanned']} text files; {result['summary']['controls_total']} controls; {result['summary']['potential_secrets']} potential secret pattern(s).",file=sys.stderr)
    return 2 if args.fail_on_secrets and result["potential_secrets"] else 0

if __name__ == "__main__": raise SystemExit(main())
