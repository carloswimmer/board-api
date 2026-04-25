# TDD Plan - board-api (FastAPI + Strawberry)

## Goal
Apply Test-Driven Development across the API rebuild to ensure SPEC parity and prevent regressions.

## Why here (after item 3)
We already have:
- SPEC -> tests matrix (3.1)
- fixture strategy (3.2)

So we are ready to execute strict TDD before implementing data model/resolvers.

---

## TDD Rules (mandatory)

1. Always start with a failing test (RED).
2. Implement the minimum code to pass (GREEN).
3. Refactor without changing behavior (REFACTOR).
4. One behavior per test cycle.
5. Never batch multiple features before getting green.
6. Keep commits small and aligned to TDD slices.

---

## Test Layers

### Unit tests
Focus:
- enum/status mapping
- validation helpers
- auth guards
- ownership checks
- toggle-like transaction logic (isolated)

### Integration tests (GraphQL)
Focus:
- schema contract
- query/mutation behavior
- auth/permission errors
- pagination/sorting/filtering
- error code mapping in `errors[].extensions.code`

---

## Execution Strategy by Vertical Slice

For each slice:
1. Write happy-path integration test (fails first).
2. Write key error-path test(s) from SPEC.
3. Add minimum implementation to pass.
4. Add/adjust unit tests for internal logic.
5. Refactor safely.
6. Commit.

---

## Slice Order (TDD)

1. `issues` query (filter/search/sort/group + comments count)
2. `issue` query
3. `createIssue`, `updateIssue`, `deleteIssue`
4. `issueComments` query (limit/offset/order)
5. `createComment`, `updateComment`, `deleteComment` (auth + ownership)
6. `issueInteractions`
7. `toggleIssueLike` (transaction consistency)

---

## Test Case Pattern (template)

Given:
- explicit seed fixtures
- explicit auth context (anon/authenticated)

When:
- execute GraphQL operation with defined input

Then:
- assert `data` shape and values
- assert DB side-effects (when mutation)
- assert error code/message for negative cases

---

## Definition of Done per slice

A slice is done only if:
- all tests for that slice are green
- at least one happy-path and one error-path covered
- no fixture leakage between tests
- lint/type checks are green
- commit created with isolated scope

---

## Suggested commit style

- `test: add failing tests for <slice>`
- `feat: implement <slice> to satisfy tests`
- `refactor: clean <slice> without behavior changes`

(or a single commit per slice if preferred, but keep scope strict)

---

## Guardrails

- Do not implement a resolver without at least one failing test.
- Do not move to next slice with failing tests in current slice.
- Do not mix unrelated slices in one commit.
- Keep UTC behavior and error semantics aligned with SPEC.