---
description: Analyze coverage, identify gaps, and generate missing tests toward the target threshold.
---

# Test Coverage

Analyze Python test coverage, identify meaningful gaps, and add focused tests toward a user-defined or risk-justified target.

## Step 1: Detect Test Framework

Use the repository-supported command:

```bash
uv run python -m pytest --cov --cov-report=term-missing
```

## Step 2: Analyze Coverage Report

1. Run the coverage command
2. Parse the output (JSON summary or terminal output)
3. List the lowest-covered files and important uncovered branches
4. For each under-covered file, identify:
   - Untested functions or methods
   - Missing branch coverage (if/else, switch, error paths)
   - Dead code that inflates the denominator

## Step 3: Generate Missing Tests

For each under-covered file, generate tests following this priority:

1. **Happy path** — Core functionality with valid inputs
2. **Error handling** — Invalid inputs, missing data, network failures
3. **Edge cases** — Empty arrays, null/undefined, boundary values (0, -1, MAX_INT)
4. **Branch coverage** — Each if/else, switch case, ternary

### Test Generation Rules

- Place tests adjacent to source: `foo.ts` → `foo.test.ts` (or project convention)
- Use existing test patterns from the project (import style, assertion library, mocking approach)
- Mock external dependencies (database, APIs, file system)
- Each test should be independent — no shared mutable state between tests
- Name tests descriptively: `test_create_user_with_duplicate_email_returns_409`

## Step 4: Verify

1. Run the full test suite — all tests must pass
2. Re-run coverage — verify improvement
3. Repeat only while additional tests cover meaningful behavior and remain in scope

## Step 5: Report

Show before/after comparison:

```
Coverage Report
──────────────────────────────
File                   Before  After
src/services/auth.ts   45%     88%
src/utils/validation.ts 32%    82%
──────────────────────────────
Overall:               67%     84%  PASS:
```

## Focus Areas

- Functions with complex branching (high cyclomatic complexity)
- Error handlers and catch blocks
- Utility functions used across the codebase
- API endpoint handlers (request → response flow)
- Edge cases: null, undefined, empty string, empty array, zero, negative numbers
