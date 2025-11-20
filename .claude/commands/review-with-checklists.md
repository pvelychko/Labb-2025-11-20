---
description: Perform thorough review using guidelines and checklists (no sub-agents)
argument-hint: [Additional Context]
---

# Review Current Implementation (v2)

## Variables
ADDITIONAL_CONTEXT: $ARGUMENTS

## Instructions
- **Follow project guidelines** (CLAUDE.md, AGENTS.md, README.md)
- **Follow critical rules and guardrails** (`docs/checklists/CRITICAL-RULES-AND-GUARDRAILS.md`)
- **Follow relevant development guidelines**:
   - For Development tasks: `docs/guidelines/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md`
   - For UI/UX tasks: `docs/guidelines/UX-UI-GUIDELINES.md`
   - See also other guidelines in `docs/guidelines/` as needed
- Non-modifying analysis only
- Use review checklists in `docs/checklists/` for systematic assessment
- No sub-agents (direct review approach)

## Workflow

### Phase 1: Context Analysis
1. Run `git status --porcelain` and `git diff` to identify changes
2. Run `git log -10 --oneline` to understand recent evolution
3. Use `tree -d -L 3` and `git ls-files | head -250` for codebase overview
4. Identify review scope (code, architecture, UI/UX based on changes)
5. Consider ADDITIONAL_CONTEXT if specified

**Gate**: Scope determined, relevant files identified

### Phase 2: Review Execution

Perform applicable reviews using checklists:

#### Code Review
Reference: `docs/checklists/CODE-REVIEW-CHECKLIST.md`
Guidelines: `docs/guidelines/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md`

Assess:
- Correctness, readability, best practices, performance
- Security (input validation, injection prevention, auth/authz, data protection, OWASP Top 10)
- Maintainability (organization, testability, documentation, technical debt)
- Regression prevention, operational concerns

#### Architecture Review
Reference: `docs/checklists/ARCHITECTURAL-REVIEW-CHECKLIST.md`
Guidelines: `docs/guidelines/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md`

Assess:
- CUPID principles (Composable, Unix philosophy, Predictable, Idiomatic, Domain-aligned)
- DDD patterns (bounded contexts, aggregates, domain events)
- Pattern adherence (clean architecture, service architecture, API design, data architecture)
- Anti-patterns, performance, scalability, resilience, security architecture

#### UI/UX Review (when applicable)
Reference: `docs/checklists/UI-UX-REVIEW-CHECKLIST.md`
Guidelines: `docs/guidelines/UX-UI-GUIDELINES.md`

Assess:
- Visual quality (layout, typography, color/contrast, responsive)
- Usability (5-second clarity, touch targets, cognitive load, task efficiency)
- Platform conventions (iOS HIG, Material Design, web standards)
- Accessibility (WCAG 2.2), performance, interaction patterns

**Gate**: All applicable reviews complete

### Phase 3: Analysis & Findings

1. Categorize findings by priority:
   - 🚨 CRITICAL: Security vulnerabilities, data loss risks, broken functionality, blocking issues
   - ⚠️ HIGH: Performance issues, maintainability concerns, minor security issues, significant tech debt
   - 💡 SUGGESTIONS: Improvements, optimizations, enhancements

2. Identify obsolete/temporary files and code requiring cleanup
3. Check for unmotivated complexity, over-engineering, or duplication
4. Verify adherence to project guidelines and patterns

**Gate**: Findings categorized and validated

## Report

Generate concise markdown report at `docs/temp/review-report-[date].md`:

```markdown
# Review Report - [Date]

## Summary
[2-3 sentence overview of review scope and overall assessment]

## 🚨 CRITICAL ISSUES
[Each issue: Title, Impact, Location, Fix Required]

## ⚠️ HIGH PRIORITY
[Each issue: Title, Impact, Location, Recommendation]

## 💡 SUGGESTIONS
[Brief list of improvements]

## Cleanup Required
- [Obsolete/temporary files to remove]
- [Dead code to remove]

## Compliance
- Guidelines adherence: [Assessment]
- Architecture patterns: [Assessment]
- Security best practices: [Assessment]
- [UI/UX if applicable]: [Assessment]

## Next Steps
1. [Prioritized action items]
```

Store report and notify user of location.
