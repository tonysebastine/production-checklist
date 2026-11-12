# Authorization & Access Control Implementation Prompts

Use this specification to implement Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC), Multi-Tenant Data Isolation, and Insecure Direct Object Reference (IDOR/BOLA) defenses.

---

## 1. Context Setting
```markdown
# Context
We are implementing a zero-trust authorization and access control layer for [APPLICATION/SERVICE] in [LANGUAGE/FRAMEWORK] with [DATABASE (e.g. PostgreSQL, MySQL)]. The application handles multi-tenant data where strict tenant boundaries and granular user permissions must be enforced unconditionally on every request.
```

---

## 2. Objective
```markdown
# Objective
Create a robust, server-side authorization architecture combining granular permissions (RBAC/ABAC), database-level multi-tenant isolation (PostgreSQL Row-Level Security), and proactive defense against IDOR (Insecure Direct Object References) and BOLA (Broken Object Level Authorization).
```

---

## 3. Requirements

### A. Core Authorization & Principle of Least Privilege
1. **Server-Side Enforcement:** Every sensitive operation, mutation, and query must perform authorization checks exclusively on the server, ignoring client UI state.
2. **Default Deny:** Access to any resource or operation defaults to forbidden unless an explicit policy grants permission.
3. **Roles & Granular Permissions:** Define roles (e.g., Owner, Admin, Member, Viewer) mapped to atomic actions (e.g., `invoice:create`, `invoice:read`, `invoice:delete`, `team:invite`).

### B. Multi-Tenant Isolation & Row-Level Security (RLS)
1. **Tenant Anchor:** Every tenant-scoped entity must include an indexed, immutable `tenant_id` foreign key.
2. **Context Injection:** Derive `tenant_id` exclusively from validated server session/token state; reject or ignore client query parameters or request body tenant identifiers.
3. **Database RLS Policies:**
   - Enable PostgreSQL `ROW LEVEL SECURITY` on all tenant-specific tables.
   - Enforce policies comparing `tenant_id = current_setting('app.current_tenant_id', true)::uuid`.
   - Application connections must set `SET LOCAL app.current_tenant_id = :tenant_id` within transactional scopes.
4. **Superuser Bypass Guard:** Ensure application runtime user is non-superuser to enforce RLS policies unconditionally.

### C. IDOR & BOLA Defenses
1. **Scoped Lookups:** In queries/ORMs, always fetch resources by composite conditions: `WHERE id = :resource_id AND tenant_id = :current_tenant_id`.
2. **Opaque Identifiers:** Prefer UUIDv7 / UUIDv4 or NanoIDs over sequential auto-incrementing integer IDs for all externally accessible resources.
3. **Uniform Error Handling:** Return uniform 404 (Not Found) responses when unauthorized users query resources belonging to other tenants, preventing object enumeration.
4. **Batch Operation Verification:** Ensure batch endpoints validate every item in the requested ID array before executing any partial mutations.

---

## 4. Code Quality & Tooling
```markdown
# Code Quality & Tooling
- Type-safe policy/guard decorators or middleware (e.g. `@RequirePermission('invoice:read')`).
- Clean separation between authentication (identity verification) and authorization (permission verification).
- Automated database migration scripts creating RLS policies and indexes.
```

---

## 5. Output Expected
```markdown
# Output Expected
Provide:
1. SQL migration scripts enabling RLS, creating tenant indices, and setting up policies.
2. Authorization middleware / guard and decorator implementation.
3. Service layer pattern enforcing scoped lookups.
4. Security test suite covering cross-tenant data access attempts, IDOR tampering, and role privilege escalation attacks.
```

