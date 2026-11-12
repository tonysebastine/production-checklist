# API Security & Rate Limiting Implementation Prompts

Use this specification to implement distributed sliding-window rate limiting, SSRF egress protections, webhook HMAC verification, and anti-abuse controls.

---

## 1. Context Setting
```markdown
# Context
We are implementing API security boundaries, distributed rate limiting, and egress request controls for [APPLICATION/API] built in [LANGUAGE/FRAMEWORK] deployed behind [REVERSE PROXY / CDN] with [REDIS / DISTRIBUTED CACHE]. The API handles public endpoints, authenticated customer traffic, third-party outbound webhooks, and URL fetching features.
```

---

## 2. Objective
```markdown
# Objective
Create an API defense layer that stops credential brute-forcing and resource exhaustion using Redis-backed sliding-window rate limiters, eliminates Server-Side Request Forgery (SSRF) and DNS rebinding attacks on outbound HTTP clients, and secures webhook integrations via HMAC-SHA256 signatures.
```

---

## 3. Requirements

### A. Distributed Sliding-Window Rate Limiting
1. **Algorithm:** Implement atomic sliding-window rate limiting using Redis sorted sets (`ZSET`) or optimized Lua scripts.
2. **Tiered Limits:**
   - Public IP tier: e.g., 100 requests / minute.
   - Authenticated User / API Token tier: e.g., 1000 requests / minute.
   - Sensitive endpoints (`/auth/login`, `/auth/reset-password`, heavy exports): Strict limits (e.g. 5 requests / minute).
3. **HTTP 429 Response:** Return standard headers (`RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, `Retry-After`) and a structured JSON error body.

### B. Server-Side Request Forgery (SSRF) Egress Controls
1. **Scheme Restrictions:** Permit only `http://` and `https://`; forbid `file://`, `gopher://`, `ftp://`, etc.
2. **DNS Resolution & Subnet Blocking:**
   - Resolve hostname to all associated IP addresses before initiating connection.
   - Deny connection if any IP falls within loopback (`127.0.0.0/8`, `::1`), private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), or cloud metadata (`169.254.169.254`, `fd00::/8`).
3. **DNS Rebinding Prevention:** Connect directly to the verified IP address; do not re-resolve the hostname when initiating the TCP/TLS socket.
4. **Redirect Inspection:** Enforce maximum redirect limit (max 3), running IP validation checks on every redirect target.
5. **Resource Limits:** Enforce strict 5-second socket/read timeouts and maximum response body size caps (e.g., 5MB).

### C. Webhook HMAC Security
1. **Inbound Webhook Verification:**
   - Read raw request body bytes before JSON parsing.
   - Calculate HMAC-SHA256 of `${timestamp}.${raw_body}` using a shared secret.
   - Enforce timestamp freshness (reject events older than 300 seconds to stop replay attacks).
   - Use timing-safe string comparison (`hmac.compare_digest`).
2. **Outbound Webhook Delivery:**
   - Sign outbound payloads with HMAC-SHA256 and attach `X-Signature` and `X-Timestamp` headers.
   - Implement exponential backoff retry schedules with jitter for delivery failures.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Asynchronous non-blocking Redis and HTTP client implementations.
- Robust custom exceptions for RateLimitExceeded, SSRFBlockedHost, and InvalidWebhookSignature.
- Security tests verifying sliding window precision and SSRF payload blocking.
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. Redis-backed sliding-window rate limiting middleware.
2. SSRF-safe HTTP client wrapper.
3. Inbound webhook verification middleware and outbound delivery service.
4. Test suite verifying rate-limit cutoffs, cloud metadata SSRF blocking, and webhook replay rejection.
```

