# CLAUDE.md - AI Coding Agent Rules, Operating Procedures, Guidelines and Core Project Memory

This file provides guidance to AI coding agents when working with code in this project.


---


## Project Overview

**Gilded Rose Refactoring Kata** - A legacy code refactoring exercise featuring an inventory management system for an inn. The system automatically updates item quality and sell-by dates each day according to specific business rules that vary by item type.

### Tech Stack
- Python 3.x
- pytest (testing framework)
- Approval testing support (TextTest)

### Key Files
- `python/gilded_rose.py` - Main implementation (legacy code to be refactored)
- `python/tests/` - Test suites
- `business-rules.md` - Comprehensive business rules documentation
- `GildedRoseRequirements.md` - Original requirements specification


---


## Business Rules
_Fully read @business-rules.md for comprehensive business rules._


---


## CRITICAL AND FOUNDATIONAL RULES
_Fully read and understand_ @../docs/guidelines/CRITICAL-RULES-AND-GUARDRAILS.md


---


## Critical Development, UI/UX, and Architecture Guidelines and Standards
_Fully read and understand_ @../docs/guidelines/DEVELOPMENT-ARCHITECTURE-GUIDELINES.md

See also:
- _`../docs/guidelines/UI-UX-GUIDELINES.md`_ when doing UX/UI related work
- _`../docs/guidelines/WEB-DEV-GUIDELINES.md`_ when doing web development work


## Critical Documentation Resources
- **GildedRoseRequirements.md** - Original kata requirements and background
- **business-rules.md** - Detailed business rules with examples and edge cases
- **README.md** - Kata overview and learning resources


---


## Project-Specific Constraints

### IMMUTABLE CODE (Do Not Modify)
- **Item class** (`name`, `sell_in`, `quality` fields) - Belongs to the goblin who doesn't believe in shared code ownership
- **items property** - Must not be altered

### What You CAN Do
- Modify the `update_quality()` method
- Add new classes, methods, or helper functions
- Refactor internal logic and structure
- Add comprehensive tests


---


## Kata Goals & Best Practices

### Primary Objectives
1. **Refactor** the legacy `update_quality()` method for clarity and maintainability
2. **Maintain** all existing functionality (tests must pass)
3. **Add** the Conjured items feature
4. **Practice** incremental refactoring with frequent test runs

### Refactoring Guidelines
- Take small, incremental steps
- Run tests after each change
- Don't rewrite from scratch - refactor incrementally
- Use design patterns where appropriate (Strategy, Polymorphism, etc.)
- Keep business logic clear and separated by item type


---


## Testing Strategy

### Available Test Approaches
1. **Unit Tests**: `tests/test_gilded_rose.py`
2. **Approval Tests**: `tests/test_gilded_rose_approvals.py`
3. **TextTest**: See `texttests/README.md`

### Testing Best Practices
- Write tests BEFORE refactoring if coverage is insufficient
- Use approval tests to lock in current behavior
- Verify all item types and edge cases
- Test quality boundaries (0 and 50)
- Test sell-in transitions (before/after sell date)


---


## Useful Tools and MCP Servers

### Context7 MCP - Library and Framework Documentation Lookup (https://github.com/upstash/context7)
Context7 MCP pulls up-to-date, version-specific documentation and code examples straight from the source.

### Fetch (https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
A Model Context Protocol server that provides web content fetching capabilities

### Code Analysis and Style (Analysis, Linting and Formatting)

**Automatically use the IDE's built-in diagnostics tool to check for analysis, linting and type errors:**
- Run `mcp__ide_getDiagnostics` to check all files for diagnostics
- Fix any linting or type errors before considering the task complete
- Do this for any file you create or modify


---


## Common Refactoring Patterns

### Suggested Approaches
1. **Extract Method** - Break down the complex update_quality() method
2. **Strategy Pattern** - Create separate strategies for each item type
3. **Polymorphism** - Use inheritance or composition for item-specific behavior
4. **Guard Clauses** - Replace nested conditionals with early returns
5. **Item Type Classes** - Create wrapper classes for business logic without modifying Item

### Anti-Patterns to Avoid
- Long, nested if-else chains
- Magic numbers (use named constants)
- Duplicated logic across item types
- Mixing concerns (calculation vs. state updates)
