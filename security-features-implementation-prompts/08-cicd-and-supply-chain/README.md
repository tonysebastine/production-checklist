# CI/CD & Software Supply Chain Security Implementation Prompts

Use this specification to implement automated vulnerability scanning (SAST/DAST), dependency auditing (SCA), secret detection, signed artifacts, and Software Bill of Materials (SBOM) generation.

---

## 1. Context Setting
```markdown
# Context
We are implementing a shift-left DevSecOps and supply chain security framework for [PROJECT/REPOSITORY] using [CI PLATFORM (e.g., GitHub Actions, GitLab CI)] and [LANGUAGE/PACKAGE MANAGER (e.g. npm, pip, cargo, go mod)]. The goal is to detect vulnerabilities, secrets, and policy violations early in the developer workflow prior to code merge or production deployment.
```

---

## 2. Objective
```markdown
# Objective
Create an automated security pipeline that enforces pre-commit secret scanning, conducts dependency vulnerability audits (SCA), runs static code analysis (SAST), generates CycloneDX Software Bills of Materials (SBOMs), and signs deployment artifacts cryptographically.
```

---

## 3. Requirements

### A. Secret Scanning & Leak Prevention
1. **Developer Workstation (Pre-Commit):** Configure git hooks using Gitleaks or detect-secrets to scan staged files locally before commit.
2. **CI Pipeline Gate:** Scan full PR git diffs and commit histories for high-entropy strings, private keys, AWS/GCP tokens, and third-party API credentials.
3. **Fail Policy:** Fail CI checks immediately upon discovering valid secret patterns; prevent branch merge.

### B. Software Composition Analysis (SCA) & Dependency Auditing
1. **Automated Auditing:** Scan lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`) on every push using Trivy, OSV-Scanner, or Snyk.
2. **Severity Gate:** Block merges if dependencies contain unpatched vulnerabilities with CVSS >= 7.0 (High / Critical).
3. **Lockfile Integrity:** Enforce reproducible installs in CI (e.g. `npm ci`, `pip install --require-hashes`, `cargo --frozen`).

### C. Static Application Security Testing (SAST)
1. **Rule-Based Code Scanning:** Integrate Semgrep or CodeQL scanning for OWASP Top 10 vulnerabilities (SQLi, XSS, SSRF, insecure deserialization).
2. **Custom Policy Rules:** Include custom repository rules to forbid patterns like direct string concatenation in queries or `subprocess.run(shell=True)`.

### D. Software Bill of Materials (SBOM) & Artifact Signing
1. **SBOM Generation:** Produce a machine-readable SBOM in CycloneDX or SPDX format during build stage and publish as an immutable pipeline artifact.
2. **Cryptographic Signing:** Sign container images and release binaries using Sigstore / Cosign with keyless OIDC authentication.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Modular, well-commented CI workflow configuration files.
- Clear error reporting in PR review comments with actionable remediation steps.
- Safe secret handling within CI jobs (zero echo or exposure in build logs).
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. Complete CI workflow definition (`.github/workflows/security.yml` or GitLab equivalent).
2. Local pre-commit hook configuration file (`.pre-commit-config.yaml` or Husky hook).
3. Semgrep custom rule configuration for project-specific security boundaries.
4. Step-by-step instructions for developer remediation and secret revocation.
```

