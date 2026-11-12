# AI & LLM Security Implementation Prompts

Use this specification to defend GenAI features, LLM workflows, and AI agent architectures against prompt injection, untrusted tool execution, indirect data poisoning, and unauthorized system access.

---

## 1. Context Setting
```markdown
# Context
We are implementing security defenses, guardrails, and sandboxing for an AI application / agentic system [SYSTEM_NAME] powered by [LLM_PROVIDER (e.g. OpenAI, Anthropic, Google Gemini)] in [LANGUAGE/FRAMEWORK]. The system accepts user queries, retrieves external untrusted context (webpages, uploaded files, third-party APIs), and has access to execute tools/functions on behalf of users.
```

---

## 2. Objective
```markdown
# Objective
Create an AI defense architecture that mitigates Direct and Indirect Prompt Injection attacks, enforces strict server-side authorization and schema boundaries on LLM tool calls, prevents sensitive system prompt extraction, and runs high-privilege operations behind human-in-the-loop (HITL) gates.
```

---

## 3. Requirements

### A. Prompt Boundary Isolation & Injection Defense
1. **Structural Delimitation:** Separate developer system instructions, retrieved third-party context, and direct user query using unambiguous XML/markdown boundaries:
   ```xml
   <system_instructions>
   Core system rules and behavioral constraints.
   </system_instructions>
   <retrieved_context>
   Untrusted third-party or document data (escaped).
   </retrieved_context>
   <user_input>
   User query (escaped).
   </user_input>
   ```
2. **Delimiter Escaping:** Sanitize untrusted inputs to strip or escape closing boundary tags (e.g., `</user_input>`).
3. **Pre-LLM Guardrail Filtering:** Run lightweight semantic classification or regex filters to detect adversarial jailbreak prompts ("ignore previous instructions", "system prompt reveal") before passing to the primary model.
4. **Canary Tokens:** Inject randomized canary tokens into system prompts to detect and abort responses attempting system prompt leakage.

### B. Agent Tool-Execution Gatekeeper
1. **Server-Side Authorization Binding:** Never trust LLM parameters to establish user identity or permissions. The tool execution layer must bind `user_id` and `tenant_id` from the authenticated session context, not from model arguments.
2. **Strict Argument Validation:** Validate all tool/function call arguments against strict Pydantic / Zod schemas before invocation.
3. **High-Impact Action Gates (Human-in-the-Loop):**
   - For destructive or sensitive actions (file deletion, financial transfer, sending emails, updating security settings), do not execute autonomously.
   - Halt execution and emit a cryptographically signed approval token requiring explicit user confirmation.
4. **Execution Sandboxing:** Run code execution, shell commands, or web browsing tools inside isolated, ephemeral, network-restricted containers.

### C. Output Sanitization & Content Filtering
1. **Model Output Untrusted Rule:** Treat all model outputs as untrusted input.
2. **XSS & Injection Neutralization:** Sanitize generated Markdown/HTML using DOMPurify before rendering in web clients.
3. **PII Filtering:** Redact sensitive credentials, API keys, and personal identifiers from LLM outputs.

### D. Token & Quota Controls
1. Enforce per-user and per-tenant rate limits on prompt tokens, completion tokens, and dollar budgets.
2. Enforce strict timeouts on LLM API calls and agent thought loops.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Modular prompt templates with automated boundary escaping.
- Type-safe tool dispatcher with permission hooks.
- Security red-teaming test harness with adversarial injection test cases.
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. Secure prompt builder with structural tagging and delimiter escaping.
2. Tool execution dispatcher enforcing session context binding and Pydantic validation.
3. Human-in-the-loop approval workflow module for destructive tools.
4. Red-teaming test suite verifying injection deflection, canary token protection, and tool authorization enforcement.
```

