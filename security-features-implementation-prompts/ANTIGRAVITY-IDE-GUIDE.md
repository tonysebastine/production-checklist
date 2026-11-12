# Antigravity IDE Workflow Guide: Security Implementation Prompts

This guide outlines how to use the prompts and documents in this repository with **Google Antigravity IDE** for automated development, security auditing, and code reviews.

- **Repository:** `https://github.com/tonysebastine/production-checklist.git`

---

## 1. Antigravity IDE Workspace Integration

Antigravity IDE automatically recognizes:
- [**`.gemini/rules/security-rules.md`**](file:///d:/Tony/Personal/GIT/production-checklist/.gemini/rules/security-rules.md): Global workspace rules that guide the agent's behavior during coding and review turns.
- [**`security-features-implementation-prompts/`**](file:///d:/Tony/Personal/GIT/production-checklist/security-features-implementation-prompts/README.md): The centralized prompt library.

---

## 2. Recommended Antigravity Slash Commands

When interacting with Antigravity IDE, leverage these built-in slash commands:

### `/plan` — Pre-Implementation Architectural Alignment
Before having the agent generate code, type:
```text
/plan Implement 01-authentication-and-sessions in Python with FastAPI and PostgreSQL
```
> Antigravity will draft an implementation plan based on `security-features-implementation-prompts/01-authentication-and-sessions/README.md` and await your approval before touching files.

### `/grill-me` — Interactive Security Design Interview
If you want the agent to interview you on business requirements, architecture trade-offs, and threat models:
```text
/grill-me on implementing 02-authorization-and-access-control for our multi-tenant SaaS
```

### `/goal` — Unsupervised End-to-End Implementation
When you are ready for the agent to implement, test, and verify an entire security module autonomously:
```text
/goal Implement the complete invoice verification service specified in security-features-implementation-prompts/11-document-integrity-and-verification/
```

### `/compact` — Context Optimization
Use `/compact` during long architectural conversations to preserve token space and keep the agent focused on core invariants.

---

## 3. How to Execute Prompts with the Antigravity Agent

### Step 1: Open the Target Area
Open any prompt file (e.g. [`05-api-security-and-rate-limiting/README.md`](file:///d:/Tony/Personal/GIT/production-checklist/security-features-implementation-prompts/05-api-security-and-rate-limiting/README.md)).

### Step 2: Trigger in Chat
In the Antigravity chat input, send:
```text
Implement the security feature in security-features-implementation-prompts/05-api-security-and-rate-limiting/README.md using Node.js / Express and Redis. Follow the guidelines in .gemini/rules/security-rules.md.
```

### Step 3: Agent Execution Lifecycle
Antigravity will automatically:
1. Load [`.gemini/rules/security-rules.md`](file:///d:/Tony/Personal/GIT/production-checklist/.gemini/rules/security-rules.md) into its context.
2. Read the domain prompt and requirements.
3. Produce the production-hardened files and automated security verification tests.

