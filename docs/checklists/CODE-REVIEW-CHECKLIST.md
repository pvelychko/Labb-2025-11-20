# Code Review Checklist

Concise, actionable checklist for thorough code reviews.

**Prerequisites**: Review project guidelines at `docs/guidelines/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md`

## Pre-Review
- [ ] Understand code's purpose and context
- [ ] Review changed files (`git diff` or equivalent)
- [ ] Check project guidelines (CLAUDE.md, coding standards)

## Code Quality

### Correctness & Logic
- [ ] No bugs or logical errors
- [ ] Edge cases handled (null/undefined, empty arrays, boundary conditions)
- [ ] Error handling comprehensive (try/catch, error propagation, user-friendly messages)
- [ ] Async operations handled correctly (promises, race conditions, error handling)
- [ ] Business logic correct and complete

### Readability & Clarity
- [ ] Code is simple, clear, self-documenting
- [ ] Naming is descriptive, consistent, follows conventions
- [ ] Functions/methods focused, reasonably sized
- [ ] Complex logic explained with comments where needed
- [ ] Magic numbers/strings replaced with named constants

### Best Practices
- [ ] Language/framework idioms followed
- [ ] DRY principle applied pragmatically
- [ ] SOLID/CUPID principles respected (see guidelines)
- [ ] No code duplication without justification
- [ ] Appropriate design patterns used
- [ ] No anti-patterns (god objects, circular dependencies, tight coupling)

### Performance
- [ ] No obvious performance issues (N+1 queries, inefficient algorithms)
- [ ] Appropriate data structures used
- [ ] Resource usage reasonable (memory, CPU, network)
- [ ] Caching applied where beneficial
- [ ] Database queries optimized (indexes, pagination)

## Security

### Input Validation & Sanitization
- [ ] All user input validated and sanitized
- [ ] Type checking and bounds checking applied
- [ ] Whitelisting used over blacklisting where possible
- [ ] File uploads validated (type, size, content)

### Injection Prevention
- [ ] SQL injection prevented (prepared statements, parameterized queries, ORM)
- [ ] Command injection prevented (avoid shell execution, input validation)
- [ ] XSS prevented (output encoding, CSP headers, DOM sanitization)
- [ ] Path traversal prevented (path validation, no user-controlled file paths)
- [ ] Template injection prevented

### Authentication & Authorization
- [ ] Authentication checks present and correct
- [ ] Authorization enforced at all access points
- [ ] Session management secure (timeout, invalidation, secure cookies)
- [ ] Password handling secure (hashing, no plaintext storage, strong algorithms)
- [ ] Multi-factor authentication supported where required

### Data Protection
- [ ] Sensitive data encrypted in transit (HTTPS/TLS)
- [ ] Sensitive data encrypted at rest where required
- [ ] No secrets, API keys, credentials in code
- [ ] No sensitive data in logs (passwords, tokens, PII)
- [ ] Secrets managed via environment variables or secret management service
- [ ] PII handling compliant with regulations (GDPR, CCPA)

### Dependencies & Supply Chain
- [ ] Dependencies up-to-date and vulnerability-free
- [ ] Minimal dependency footprint (no unnecessary packages)
- [ ] Dependencies from trusted sources
- [ ] Lock files committed (package-lock.json, Pipfile.lock, etc.)

### Secure Coding
- [ ] HTTPS enforced, no mixed content
- [ ] CORS configured correctly (not `*` in production)
- [ ] Security headers set (CSP, X-Frame-Options, HSTS, etc.)
- [ ] Rate limiting implemented for public APIs
- [ ] CSRF protection enabled for state-changing operations
- [ ] Safe deserialization (no eval, pickle, etc. on untrusted data)

### OWASP Top 10 Coverage
- [ ] Broken access control prevented
- [ ] Cryptographic failures addressed
- [ ] Injection vulnerabilities prevented
- [ ] Insecure design patterns avoided
- [ ] Security misconfiguration addressed
- [ ] Vulnerable/outdated components identified
- [ ] Identification/authentication failures prevented
- [ ] Software/data integrity failures prevented
- [ ] Security logging/monitoring failures addressed
- [ ] SSRF vulnerabilities prevented

## Maintainability

### Code Organization
- [ ] Separation of concerns clear
- [ ] Responsibilities well-distributed (no god objects)
- [ ] Layer boundaries respected (no improper dependencies)
- [ ] Module/package structure logical
- [ ] Files/classes reasonably sized

### Testability
- [ ] Code testable (dependency injection, pure functions where possible)
- [ ] Test coverage adequate (critical paths, edge cases)
- [ ] Tests pass and are meaningful
- [ ] Tests are maintainable and readable
- [ ] Mock/stub usage appropriate

### Documentation
- [ ] Public APIs documented
- [ ] Complex algorithms explained
- [ ] Assumptions and constraints documented
- [ ] Breaking changes noted
- [ ] No obsolete comments or TODOs without context

### Configuration & Dependencies
- [ ] No hardcoded values (use config/env vars/constants)
- [ ] Dependencies version-pinned or ranged appropriately
- [ ] Feature flags used for risky changes
- [ ] Database migrations reversible

### Technical Debt
- [ ] No new technical debt without explicit acknowledgment
- [ ] Workarounds documented with reason and follow-up plan
- [ ] Deprecated code usage avoided
- [ ] Code complexity reasonable (cyclomatic complexity, nesting depth)

## Additional Checks

### Regression Prevention
- [ ] Existing functionality still works
- [ ] Tests updated/added for changes
- [ ] Integration points validated
- [ ] Backward compatibility maintained or migration path clear

### Operational Concerns
- [ ] Logging appropriate (level, content, no sensitive data)
- [ ] Monitoring/observability supported (metrics, traces)
- [ ] Error messages actionable and user-friendly
- [ ] Graceful degradation for failures
- [ ] Resource cleanup (connections, files, memory)

### Deployment & Rollback
- [ ] Database migrations safe and reversible
- [ ] Feature flags for risky changes
- [ ] No breaking API changes without versioning
- [ ] Deployment risks identified

## Review Priorities

### 🚨 CRITICAL (Must Fix)
- Security vulnerabilities
- Data loss/corruption risks
- Breaking changes/regressions
- Critical bugs
- Authentication/authorization bypasses

### ⚠️ HIGH (Should Fix)
- Performance issues
- Maintainability concerns
- Minor security issues
- Incorrect error handling
- Significant technical debt

### 💡 SUGGESTIONS (Consider)
- Code style improvements
- Refactoring opportunities
- Documentation enhancements
- Test coverage gaps
- Performance optimizations

## Final Checks
- [ ] All concerns categorized by priority
- [ ] Specific, actionable feedback provided
- [ ] Code examples/suggestions included where helpful
- [ ] 'Why' explained for each recommendation
