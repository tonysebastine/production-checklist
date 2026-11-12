# Security Headers & CORS Implementation Prompts

Use this specification to implement Content Security Policy (CSP), strict Cross-Origin Resource Sharing (CORS), HTTP response security headers, and cookie isolation.

---

## 1. Context Setting
```markdown
# Context
We are hardening web application endpoints, API services, and single-page applications for [APPLICATION/SERVICE] running on [FRAMEWORK / REVERSE PROXY (e.g. Next.js, Express, FastAPI, NGINX)]. The application handles browser interactions, authenticated API sessions, and embedded resources that require defense against clickjacking, XSS, and unauthorized cross-origin requests.
```

---

## 2. Objective
```markdown
# Objective
Create a unified security headers and CORS configuration layer that enforces a strict nonce-based Content Security Policy (CSP Level 3), sets resilient transport headers (HSTS), blocks framing/clickjacking, configures strict cross-origin permissions, and enforces hardened cookie attributes.
```

---

## 3. Requirements

### A. HTTP Security Headers
1. **HSTS:** `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`.
2. **MIME Sniffing Defense:** `X-Content-Type-Options: nosniff`.
3. **Clickjacking & Framing:** `X-Frame-Options: DENY` (and `frame-ancestors 'none'` in CSP).
4. **Referrer Policy:** `Referrer-Policy: strict-origin-when-cross-origin` or `no-referrer`.
5. **Permissions Policy:** Restrict dangerous browser APIs:
   `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()`.

### B. Content Security Policy (CSP Level 3)
1. **Nonce Generation:** Generate a unique, cryptographically random 128-bit base64 nonce on every HTTP request.
2. **Directives:**
   - `default-src 'self'`
   - `script-src 'self' 'nonce-{NONCE}'` (no `'unsafe-inline'` or `'unsafe-eval'`)
   - `style-src 'self' 'nonce-{NONCE}'`
   - `img-src 'self' data: https:`
   - `connect-src 'self' [ALLOWED_APIS]`
   - `font-src 'self'`
   - `object-src 'none'`
   - `base-uri 'self'`
   - `form-action 'self'`
   - `frame-ancestors 'none'`
   - `upgrade-insecure-requests`
3. **Report Mode Support:** Allow toggling `Content-Security-Policy-Report-Only` with a report-to / report-uri endpoint for staged deployments.

### C. Enterprise Cross-Origin Resource Sharing (CORS)
1. **No Wildcard Credentials:** Never send `Access-Control-Allow-Origin: *` when `Access-Control-Allow-Credentials: true` is enabled.
2. **Dynamic Origin Validation:** Match request `Origin` header against an explicit configuration array of trusted origins. Only reflect the matched origin.
3. **Preflight Caching:** Return `Access-Control-Max-Age: 86400` to minimize unnecessary OPTIONS roundtrips.
4. **Method & Header Whitelisting:** Expose only permitted HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`) and specific request headers (`Authorization`, `Content-Type`).

### D. Cookie Isolation & Security Flags
1. **Standard Flags:** Always attach `HttpOnly; Secure; SameSite=Strict` (or `Lax` where cross-site top-level navigation requires it).
2. **Cookie Prefixes:** Prefix sensitive session and auth cookies with `__Host-` to enforce path isolation (`Path=/`), secure protocol, and subdomain immunity.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Modular middleware or web server configuration snippets (NGINX/Caddy).
- Helper functions to easily inject request nonces into HTML templates and script tags.
- Automated tests verifying headers across standard, error, and preflight requests.
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. Security headers middleware implementation with dynamic nonce injection.
2. Strict CORS middleware matching against origin allowlists.
3. Production web server configuration (NGINX/Caddy) mirror.
4. Test suite verifying CSP nonces, HSTS attributes, preflight handling, and cookie flags.
```

