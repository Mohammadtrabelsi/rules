[Rules index](../README.md) › General › Code quality

**Navigation:** Previous: [How to read these rules](how-to-read.md) · Next: [Layering and patterns](../architecture/layering-and-patterns.md) · [Table of contents](../README.md#table-of-contents)

# Code quality

A change is done only when format, static analysis and the relevant tests pass. (Testing rules: see [`../testing/testing.md`](../testing/testing.md).)

This page covers how code is written (style), how it is checked (tooling), and how work is handed back (hand-off and docs). Every rule holds in any language; the tool names are examples, and [Stack mapping](../stacks/README.md) lists the equivalents.

---

## Style

### Language style

- `[H]` **MUST** Use explicit types and the language's strict mode wherever the language offers them: typed function parameters and return values, strict null handling, and no implicit conversions that change a value's meaning. Keep the types on public interfaces accurate.
  - **Benefit:** Types make the code self-describing and let the analyzer find whole classes of bugs before runtime. Explicit return types show a reader what a function promises without reading its body.
  - **Example:**
    ```text
    function gross_total(subtotal_minor: integer, tax_minor: integer) -> integer
        return subtotal_minor + tax_minor
    ```
  - **Deviate when:** A generated file or a third-party stub forces a different shape. Keep the deviation inside that file.

- `[H]` **MUST** Use descriptive names (`is_registered_for_discounts`, not `check()`). Add a comment only where the logic is not obvious from the code.
  - **Benefit:** A name that says what the function answers removes the need to open it. Reviewers can judge a call site without reading the body.
  - **Deviate when:** A name that is the domain's own term (for example, a legal or accounting word) is more precise than a descriptive one. Use the domain term and say what it means in one line.

- `[+]` **SHOULD** Keep functions small, use early returns, and leave no dead code or commented-out code.
  - **Benefit:** Early returns keep the happy path at the left margin and make each guard obvious. Commented-out code looks like it might matter, so people hesitate to delete it, and it rots. Version control already keeps the old version.
  - **Example:**
    ```text
    function can_refund(payment) -> boolean
        if payment.is_refunded:
            return false
        return payment.amount_minor > 0
    ```

---

## Tooling

- `[H]` **MUST** Run the project's formatter and static analyzer on the changed files before committing, and fix every new finding instead of growing the baseline. Examples: Prettier and ESLint or Biome for JavaScript and TypeScript; Black or Ruff with mypy for Python; gofmt and golangci-lint for Go; RuboCop for Ruby; `dotnet format` with Roslyn analyzers for C#. See [Stack mapping](../stacks/README.md).
  - **Benefit:** The formatter removes formatting debates from review, so diffs contain only meaningful changes. The analyzer catches type and null mistakes early. A baseline that only shrinks keeps the existing debt visible and stops new debt from hiding in it.
  - **Example:** run the formatter on the changed files only (most tools accept a list of paths), then run the analyzer and check that its finding count did not rise.
  - **Deviate when:** The project sets its own analyzer level. Use that level, and never lower it to pass.

---

## Hand-off and docs

- `[H]` **MUST** Be honest in the hand-off: say exactly which tests, the formatter and the analyzer ran, and which could not run and why. Name any migration, dependency install or build step still needed.
  - **Benefit:** The person receiving the work knows what has been verified and what has not. A silent skip looks like a pass until it fails in production. Naming the migration and build steps stops the change from appearing to work locally while the database or assets are stale.
  - **Example of a good hand-off:** "Ran the formatter (clean), the analyzer (0 new findings), and `pytest -k refund` (12 passed). Did not run the browser suite because no browser is available here. Needs the database migration and the asset build (`npm run build`)."

- `[H]` **SHOULD** Do not create documentation files unless asked. When the project keeps a reference document, keep it current in the same change.
  - **Benefit:** Extra markdown files go stale quickly, and stale docs mislead more than missing docs. Keeping the existing reference current means one trusted source.
  - **Deviate when:** The person asks for documentation, or the project already maintains a reference that a change makes wrong. Then update that reference in the same change.

---

**Related:** [Testing](../testing/testing.md) (the tests this hand-off must name) · [Git workflow](../git/workflow.md) (the pull request that carries the hand-off) · [Stack mapping](../stacks/README.md) · [Summary](../SUMMARY.md)
