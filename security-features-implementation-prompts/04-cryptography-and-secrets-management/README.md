# Cryptography & Secrets Management Implementation Prompts

Use this specification to implement field-level envelope encryption, cryptographic hashing, secrets management, and secure key lifecycle operations.

---

## 1. Context Setting
```markdown
# Context
We are implementing cryptographic operations and enterprise secrets management for [APPLICATION/SERVICE] in [LANGUAGE/FRAMEWORK] interacting with [KMS / SECRET MANAGER (e.g. AWS KMS, GCP KMS, HashiCorp Vault)]. The application stores sensitive customer PII, API tokens, and confidential financial records requiring military-grade encryption at rest and in transit.
```

---

## 2. Objective
```markdown
# Objective
Create a secure cryptography service supporting field-level envelope encryption (AES-256-GCM), cryptographically secure random number generation (CSPRNG), and a zero-leakage secrets loader that fetches, validates, and rotates credentials dynamically.
```

---

## 3. Requirements

### A. Cryptographic Algorithms & Primitives
1. **Symmetric Encryption:** Use AES-256-GCM or ChaCha20-Poly1305 with authenticated encryption with associated data (AEAD).
2. **IV / Nonce Handling:** Generate a unique, non-repeating 96-bit (12-byte) initialization vector (IV) for every encryption operation using a CSPRNG. Never reuse IVs.
3. **Key Derivation:** Use HKDF (RFC 5869) or Argon2id for password-derived keys; never hash passwords or keys with unsalted SHA-256 or MD5.
4. **Asymmetric & Signatures:** Use Ed25519 or ECDSA (P-256 / P-384) with SHA-256 for digital signatures.

### B. Envelope Encryption Pattern
1. **Data Encryption Key (DEK):** Generate an ephemeral 256-bit DEK per sensitive record.
2. **Master Key (KEK):** Encrypt the DEK using a Key Encryption Key managed by a cloud KMS (AWS KMS, GCP KMS, Azure Key Vault, or Vault).
3. **Serialized Format:** Store encrypted records with the serialized format:
   `v1:{base64(encrypted_dek)}:{base64(iv)}:{base64(auth_tag)}:{base64(ciphertext)}`.
4. **Decryption:** Decrypt the DEK via KMS, then decrypt the ciphertext using the authenticated DEK. Fail immediately on authentication tag mismatch.

### C. Zero-Leakage Secrets Loader & Management
1. **Dynamic Secrets Fetching:** Fetch secrets at startup from a secure secret store (AWS Secrets Manager, GCP Secret Manager, Vault) rather than static files.
2. **Schema Verification:** Parse secrets against a strict typed schema; crash immediately if mandatory secrets are missing or malformed.
3. **Log & Crash Redaction:** Automatically scrub, mask, and redact loaded secrets from process environment tables, debug logs, exception stack traces, and APM tools.
4. **Zero-Downtime Rotation:** Support dynamic secret reload / rotation via webhooks or background polling without restarting services.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Modern cryptographic libraries (e.g., Python `cryptography`, Node.js `node:crypto`, Go `crypto/aes`).
- Constant-time operations for signature and tag validation (`hmac.compare_digest`).
- Complete error encapsulation preventing cryptographic oracle leakage.
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. Field-level envelope encryption service (`encrypt`, `decrypt`, `re_encrypt`).
2. Secrets loader module with schema validation and log-redaction filters.
3. Automated test suite verifying cipher uniqueness across identical plaintexts, authentication tag tamper rejection, and secret redaction.
```

