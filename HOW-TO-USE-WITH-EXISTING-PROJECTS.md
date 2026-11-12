# How to Use This Repository with Your Existing Projects in Antigravity IDE

Repository URL: `https://github.com/tonysebastine/production-checklist.git`

This guide details the three most effective patterns for applying these security checklists, prompts, and rules to your existing projects using **Google Antigravity IDE**.

---

## Pattern 1: Multi-Root Workspace in Antigravity IDE (Recommended)

In Antigravity IDE, you can add multiple project roots into a single workspace session. This allows the AI agent to read prompts from `production-checklist` and directly implement or audit code in your target project without duplicating files.

### Steps:
1. Open Antigravity IDE.
2. In the top menu, go to **File** &rarr; **Add Folder to Workspace...**
3. Select your existing application repository (e.g. `D:\Tony\Personal\GIT\my-saas-app`).
4. Ensure `production-checklist` is also in the workspace.
5. In chat, address the agent directly:
   ```text
   Review our existing FastAPI routes in my-saas-app/ against the specifications in production-checklist/security-features-implementation-prompts/05-api-security-and-rate-limiting/README.md and implement the missing Redis sliding-window rate limiters.
   ```

---

## Pattern 2: Copy the Rules and Prompts into Your Target Project

If you want your target project to be completely self-contained with persistent Antigravity IDE behavior:

### Steps:
1. Copy the `.gemini/` rule folder to your target project root:
   ```powershell
   Copy-Item -Path "D:\Tony\Personal\GIT\production-checklist\.gemini" -Destination "D:\Tony\Personal\GIT\my-saas-app\" -Recurse
   ```
2. (Optional) Copy specific prompt folders that apply to that project:
   ```powershell
   Copy-Item -Path "D:\Tony\Personal\GIT\production-checklist\security-features-implementation-prompts\11-document-integrity-and-verification" -Destination "D:\Tony\Personal\GIT\my-saas-app\docs\security\" -Recurse
   ```
3. Open your project in Antigravity IDE. The agent will automatically detect `.gemini/rules/security-rules.md` and enforce all security invariants across all coding sessions.

---

## Pattern 3: Use as a Git Submodule

If you manage multiple repositories and want a single source of truth that updates whenever you improve checklists or prompts:

### Steps:
1. Open a terminal in your existing project:
   ```bash
   cd /path/to/my-saas-app
   git submodule add https://github.com/tonysebastine/production-checklist.git security-checklist
   git submodule update --init --recursive
   ```
2. Add a rule link in your project's `.gemini/rules/` pointing to the submodule:
   ```markdown
   # Project Security Invariants
   Refer to `security-checklist/security-features-implementation-prompts/` for security feature implementations.
   Follow the rules defined in `security-checklist/.gemini/rules/security-rules.md`.
   ```

---

## Typical Antigravity IDE Workflows for Existing Projects

### 1. Gap Analysis & Security Audit
Ask the agent to compare your existing codebase against a specific checklist or prompt:
```text
Audit my existing user authentication service in src/auth/ against production-checklist/security-features-implementation-prompts/01-authentication-and-sessions/README.md. Create a markdown report detailing any gaps in password hashing parameters, session rotation, or timing attack defenses.
```

### 2. Guided Interactive Implementation (`/plan`)
Use the `/plan` slash command to plan how to apply a security feature into your existing database schema and routing layer:
```text
/plan Implement 02-authorization-and-access-control (PostgreSQL Row-Level Security) on our existing tenancy schema in my-saas-app/db/migrations/
```

### 3. Adding Missing Security Tests
Ask the agent to generate security tests using the prompt's test specifications:
```text
Read the Section 3 test requirements from production-checklist/security-features-implementation-prompts/03-input-validation-and-sanitization/README.md and write a Pytest suite under tests/security/test_input_validation.py for our existing API endpoints.
```

