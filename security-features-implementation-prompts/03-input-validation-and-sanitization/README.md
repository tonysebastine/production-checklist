# Input Validation & Sanitization Implementation Prompts

Use this specification to implement schema validation, SQL/NoSQL injection prevention, XSS mitigation, and secure file upload handling.

---

## 1. Context Setting
```markdown
# Context
We are implementing comprehensive input validation, output encoding, and upload processing defenses for [APPLICATION/SERVICE] built with [LANGUAGE/FRAMEWORK] and storing data in [DATABASE/STORAGE]. The service accepts user-supplied JSON payloads, query strings, rich text, and file uploads that could be weaponized for injection or malicious code execution.
```

---

## 2. Objective
```markdown
# Objective
Create a resilient input validation and content sanitization layer that blocks SQL/NoSQL/Command injection, eliminates Cross-Site Scripting (XSS), strips unauthorized properties, and processes user file uploads through a secure, sandbox-isolated pipeline.
```

---

## 3. Requirements

### A. Deep Schema Validation & Payload Scrubbing
1. **Strict Schemas:** Validate all query parameters, route variables, and request bodies against strict schemas (Pydantic / Zod / Joi).
2. **Whitelist Property Filtering:** Enforce strict property allowlists. Reject or strip unknown attributes from payloads (`strip` or `strict` schema modes) to eliminate mass assignment vulnerabilities.
3. **Boundary Constraints:** Enforce tight constraints on string length (min/max), integer ranges, regex patterns, and maximum array element counts.
4. **Payload Size Caps:** Reject payloads exceeding size limits (e.g., 1MB for JSON, 10MB for multipart files) at the gateway or middleware level.
5. **Control Character Sanitization:** Strip null bytes (`\0`) and normalize UTF-8 characters across all incoming string fields.

### B. Injection Defenses
1. **SQL / NoSQL Injection:**
   - Use prepared statements / parameterized queries exclusively across all database operations.
   - Forbid raw SQL string interpolation or dynamic column concatenation.
   - Sanitize and cast dynamic sort/order-by fields against an explicit programmatic allowlist.
2. **Command / OS Injection:**
   - Eliminate shell execution where possible; use array-argument APIs (`subprocess.run(["cmd", "arg"])` with `shell=False`).
   - If shell execution is unavoidable, restrict commands to hardcoded binaries with validated inputs.

### C. Cross-Site Scripting (XSS) Defenses
1. **Context-Aware Output Encoding:** Ensure output is encoded properly for its context (HTML body, attributes, JavaScript variables, URIs).
2. **Rich Text / HTML Sanitization:** If rich text or HTML is supported, sanitize inputs using DOMPurify or sanitize-html configured with a restrictive tag and attribute allowlist (stripping `<script>`, `<iframe>`, `onload`, `javascript:` URIs).

### D. Secure File Upload Pipeline
1. **Magic-Byte Signature Verification:** Read the initial 512 bytes of uploaded files to verify file signatures (magic numbers) against permitted MIME types, ignoring the client-supplied `Content-Type` header or extension.
2. **Filename Normalization:** Discard user-supplied filenames; generate cryptographically secure UUIDv4 filenames and append extensions derived strictly from the verified MIME type.
3. **Image Re-Encoding & EXIF Scrubbing:** Process uploaded images through an image pipeline (Pillow/Sharp) to strip all EXIF/metadata and re-encode pixel data, neutralizing polyglot payloads.
4. **Storage Isolation:** Store uploads in isolated object storage buckets configured without public execute permissions, served with `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Modern typed schemas and clean middleware hooks.
- Defensive file processing utilities with streaming upload support to minimize memory footprint.
- Unit and fuzz tests simulating malicious injection payloads and disguised executables.
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. Reusable schema validation middleware and error formatting handlers.
2. Secure file upload processing pipeline with magic-byte verification and metadata stripping.
3. Sanitization helper functions for rich text and dynamic parameters.
4. Security test suite covering SQLi, NoSQLi, XSS vectors, and disguised executable file upload attempts.
```

