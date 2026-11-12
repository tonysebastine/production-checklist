# Cloud & Infrastructure Hardening Implementation Prompts

Use this specification to implement container hardening, least-privilege cloud IAM, network boundary security, and immutable infrastructure configurations.

---

## 1. Context Setting
```markdown
# Context
We are implementing cloud infrastructure security, container runtime hardening, and network boundary controls for [APPLICATION/WORKLOAD] deployed to [CLOUD PROVIDER (AWS / GCP / Azure)] or [KUBERNETES] using [INFRASTRUCTURE TOOL (Terraform, OpenTofu, Docker)]. The production environment must withstand container escape attempts, minimize attack surfaces, and isolate databases and services in private subnets.
```

---

## 2. Objective
```markdown
# Objective
Create production-grade, hardened container specifications (Dockerfiles) and Infrastructure-as-Code definitions (Terraform) enforcing non-root execution, read-only root filesystems, zero-wildcard least-privilege IAM policies, and private VPC network segmentation.
```

---

## 3. Requirements

### A. Production Container Image Hardening (Dockerfile)
1. **Multi-Stage Builds:** Segregate build dependencies, compilers, and SDKs from the runtime stage.
2. **Minimal Base Image:** Use Google Distroless, Alpine, or Wolfi as the production base image to minimize installed binaries and CVE surface.
3. **Non-Root User:** Explicitly create and run under a dedicated non-root UID/GID (e.g. `USER 10001:10001`).
4. **Read-Only Root Filesystem:** Run container with a read-only root filesystem; configure explicit `tmpfs` mounts only for necessary scratch directories.
5. **Drop Linux Capabilities:** Drop `ALL` Linux capabilities, adding back only what is strictly required (e.g. `NET_BIND_SERVICE`).
6. **Healthchecks:** Include native `HEALTHCHECK` directives.

### B. Cloud IAM & Least Privilege
1. **Zero Wildcard Permissions:** Eliminate `*` from IAM policy actions and resource ARNs.
2. **Short-Lived Workload Identities:** Utilize OIDC federation (e.g. AWS IAM Roles for Service Accounts - IRSA, GCP Workload Identity Federation) rather than long-lived static API access keys.
3. **Role Separation:** Separate CI/CD deployment roles from application runtime service roles.

### C. Network Segmentation & VPC Security
1. **Private Subnet Placement:** Deploy databases, caches, and application services strictly into private subnets with no public IP allocation.
2. **Strict Security Groups / Firewalls:**
   - Public Ingress: Only load balancer / reverse proxy receives incoming traffic on ports 80/443.
   - Application Ingress: Only accepts connections from the load balancer security group.
   - Database Ingress: Only accepts connections from the application tier security group.
   - Default Deny: Deny all unmatched ingress and restrict outbound egress to approved endpoints.

### D. Kubernetes Security Hardening (if applicable)
1. **Pod Security Standards:** Enforce the `restricted` Pod Security Standard via admission controllers.
2. **Resource Quotas:** Specify explicit CPU and memory `requests` and `limits` to prevent denial-of-service / resource starvation.
3. **Network Policies:** Implement Kubernetes NetworkPolicies enforcing default-deny egress/ingress per namespace.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Linted Dockerfiles compliant with Hadolint rules.
- Terraform modules evaluated against Checkov / tfsec security scanners.
- Clear variable definitions and outputs without hardcoded secrets.
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. Multi-stage hardened `Dockerfile` adhering to non-root and minimal-privilege standards.
2. Terraform module setting up VPC subnets, security groups, and least-privilege IAM roles.
3. Kubernetes manifest (Deployment, Service, NetworkPolicy) adhering to the restricted security profile.
4. Validation test commands (Hadolint, Trivy, Checkov).
```

