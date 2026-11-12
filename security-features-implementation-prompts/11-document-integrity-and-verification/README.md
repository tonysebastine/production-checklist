# Tamper-Evident Document & Invoice Verification Implementation Prompts

Use these prompts to implement cryptographic document integrity verification, digital signatures, hash-anchored QR codes, and tamper-evident document validation workflows.

---

## 1. System Prompt & Context Setting

```markdown
You are a Senior Security & Cryptography Software Engineer. Your objective is to implement a secure, tamper-evident document/invoice verification and integrity checking system for [APPLICATION/SERVICE] using [LANGUAGE/FRAMEWORK (e.g. Python / FastAPI / ReportLab)] and [DATABASE/STORAGE].

### Core Requirements:
1. Canonical Data Serialization & Cryptographic Hashing:
   - Construct an immutable canonical representation of critical document attributes (e.g., Document ID, Timestamp/Date, Parties/Client, Amount/Summary).
   - Compute SHA-256 (or HMAC-SHA256 with server-managed secret / Ed25519 digital signature) over the canonical pipe-separated or canonical JSON string: `f"{id}|{date}|{client}|{amount}"`.
2. QR Code & Offline/Online Verification Anchor:
   - Embed the verification anchor into a QR code pointing to a verification URL (e.g. `https://verify.example.com/verify?id={id}&hash={hash}`).
   - Ensure QR code rendering conforms to high-contrast print requirements in PDF generators (e.g. ReportLab).
3. Secure Verification API:
   - Provide a verification endpoint `/verify` accepting `id` and `hash`.
   - Retrieve authoritative document state from persistent storage.
   - Re-calculate hash on the authoritative record.
   - Perform timing-safe comparison (`hmac.compare_digest` / constant-time equality check) to prevent side-channel timing attacks.
4. Response & Tamper Alerting:
   - Valid: Return authentic status with verified metadata.
   - Tampered/Invalid: Return alert status with HTTP 400/403, log potential forgery attempt, and do not disclose internal system details.

### Deliverables:
- Verification service/controller with Pydantic/type-safe validation.
- PDF generation hook / helper function embedding the verification QR code.
- Test suite verifying detection of altered fields, invalid hashes, and timing-safe comparisons.
```

---

## 2. Implementation Prompts by Specific Capability

### A. FastAPI Tamper-Evident Document Verification Service
```markdown
# Context
We are implementing a secure, tamper-evident invoice verification system in Python. An invoice PDF is generated using ReportLab, embedding a SHA-256 cryptographic hash of its immutable fields (Invoice ID, Date, Client, Amount) inside a QR code pointing to a verification URL.

# Objective
Create a lightweight backend verification service (using FastAPI) that handles incoming verification requests from the QR code, validates the cryptographic hash against our secure database/storage, and returns a clean, high-contrast JSON response (or renders a minimal HTML verification status page).

# Requirements
1. API Endpoint: Create a GET route at `/verify` that accepts query parameters: `id` (Invoice ID) and `hash` (SHA-256 string).
2. Hash Validation Logic: 
   - Fetch the authoritative invoice record from the database/storage corresponding to the `id`.
   - Re-compute the SHA-256 hash using the exact same pipe-separated formatting string: `f"{invoice_id}|{date}|{client}|{amount}"`.
   - Securely compare (`hmac.compare_digest`) the computed hash with the incoming query parameter `hash`.
3. Response Handling:
   - If valid: Return a success status (`"status": "authentic"`, `"message": "Invoice integrity verified successfully."`) along with basic invoice metadata.
   - If invalid/tampered: Return an alert status (`"status": "tampered_or_invalid"`, `"message": "Warning: Hash mismatch detected. This document may have been altered."`) with appropriate HTTP status codes (e.g., 400 or 403).
4. Code Quality & Tooling: 
   - Use clean, modern Python 3.10+ type hints and Pydantic models where applicable.
   - Follow a minimalist, secure, and production-ready structure optimized for low resource usage.

# Output Expected
Provide the FastAPI application code block, along with a quick snippet on how to hook it up to our existing ReportLab invoice generator.
```

### B. ReportLab QR Code & Cryptographic Anchor Generation
```markdown
Implement a Python utility function using ReportLab and qrcode:
1. Accept invoice details: `invoice_id`, `issue_date`, `client_name`, `amount`, and `base_verify_url`.
2. Compute SHA-256 hash over canonical formatted string: `f"{invoice_id}|{issue_date}|{client_name}|{amount}"`.
3. Generate a QR code pointing to `{base_verify_url}?id={invoice_id}&hash={hash}`.
4. Draw the QR code onto a ReportLab `canvas.Canvas` or embed into a `SimpleDocTemplate` Flowable story.
```

---

## 3. Security Verification & Test Suite Prompt

```markdown
Write automated security tests for the document verification service:
- [ ] Submitting correct ID and matching SHA-256 hash returns 200 OK with `"status": "authentic"`.
- [ ] Modifying single character in the hash string returns 400/403 `"status": "tampered_or_invalid"`.
- [ ] Modifying any authoritative field (e.g. changing amount from 100 to 101) invalidates original hash.
- [ ] Comparison executes using constant-time string comparison (`hmac.compare_digest`).
- [ ] Non-existent document ID returns 404 without leaking internal database error messages.
```

