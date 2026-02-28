---
name: security-auditor
description: Audit code and infrastructure for security vulnerabilities. Use when reviewing code for security, penetration testing, or implementing security controls. Triggers on requests for security audit, vulnerability scan, penetration testing, or security review.
---

# Security Auditor

Find vulnerabilities before attackers do. Code review, pentest, harden.

## Security Review Areas

### Application Security
- **Injection** — SQL, NoSQL, Command, LDAP
- **Authentication** — Weak passwords, session management
- **Authorization** — Broken access control
- **Data exposure** — Sensitive data in logs/responses
- **XXS/CSRF** — Client-side attacks

### Infrastructure Security
- **Secrets management** — No hardcoded credentials
- **Network security** — Firewalls, VPCs, TLS
- **Container security** — Non-root users, minimal images
- **Cloud config** — S3 buckets, IAM policies

### Dependency Security
- **Vulnerable packages** — npm audit, pip-audit
- **License compliance** — FOSSA, Snyk
- **Supply chain** — Signed packages, lockfiles

## Common Vulnerabilities (OWASP Top 10)

1. **Broken Access Control** — IDOR, privilege escalation
2. **Cryptographic Failures** — Weak encryption, plaintext storage
3. **Injection** — SQL, OS command, XSS
4. **Insecure Design** — Missing security controls
5. **Security Misconfiguration** — Default configs, verbose errors
6. **Vulnerable Components** — Outdated dependencies
7. **Auth Failures** — Weak passwords, no MFA
8. **Data Integrity** — No CSRF protection, insecure deserialization
9. **Logging Failures** — Insufficient monitoring
10. **SSRF** — Server-side request forgery

## Security Checklist

### Code Review
- [ ] Input validation on all endpoints
- [ ] Output encoding for dynamic content
- [ ] Parameterized queries (no string concat)
- [ ] Proper error handling (no stack traces to user)
- [ ] Authentication on all sensitive routes
- [ ] Authorization checks (RBAC/ABAC)
- [ ] Rate limiting on auth endpoints
- [ ] HTTPS everywhere

### Infrastructure
- [ ] Secrets in vault (not env vars)
- [ ] Least privilege IAM
- [ ] Network segmentation
- [ ] Logging enabled
- [ ] Automated security scanning

## References

- [OWASP Cheat Sheets](references/owasp.md)
- [SAST Tools](references/sast.md)
- [Incident Response](references/incident-response.md)
