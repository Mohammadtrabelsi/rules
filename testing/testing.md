[Rules index](../README.md) › Testing

**Navigation:** Previous: [Security](../security/security.md) · Next: [Git workflow](../git/workflow.md) · [Table of contents](../README.md#table-of-contents)

# Testing

A test is the only proof that a behaviour works and keeps working. These rules make sure the proof exists for every change and that nobody quietly removes it.

---

## What to test

- `[H]` **MUST** Automated tests for every behaviour or logic change, covering failure paths and authorization. Prefer tests that run the real request through routing, middleware, authorization and the database, over tests that only call one function. Skip tests for pure copy or styling changes.
  - **Benefit:** A test that runs the real request catches wiring mistakes that unit tests miss. Covering failure paths (invalid input, missing permission, a locked record) is where most real bugs live. Test data factories or fixtures build realistic data in one line and stay correct as the schema changes.
  - **Example:**
    ```text
    test "a resident cannot refund a payment":
        resident = create user with role "resident"
        payment  = create payment

        request as resident: POST /payments/{payment.id}/refund
        expect: status 403
        expect: payment.is_refunded == false
    ```
  - **Deviate when:** The change is pure copy or CSS with no logic. A test for a colour is noise; check it in the browser instead.

- `[H]` **SHOULD** Add a test that fails on missing translations for new menu entries and pages (see [Translations](../i18n/translations.md)).
  - **Benefit:** An automated check finds untranslated keys on every run, in every locale, without anyone remembering to look. It replaces a manual review that would be skipped under deadline.

---

## Integrity of the suite

- `[H]` **MUST** Never delete or skip a test to get green. Fix the code, or update an out-of-date expectation and say so.
  - **Benefit:** A test that was skipped to make a build pass hides the failure it was written to catch. Deleting it removes the warning. If the expectation is genuinely out of date, updating it with a note keeps the record honest about why the behaviour changed.
  - **Deviate when:** The test covers a feature being removed in the same change. Delete it together with the feature, and say so in the hand-off.

- `[H]` **MUST** Run the narrowest relevant tests before handing back, and state exactly which ran and which could not run and why.
  - **Benefit:** Running the full suite on every small change is slow; running only the test you wrote can miss a neighbour that broke. The narrowest relevant set (the changed feature and its direct callers) gives fast feedback, and stating what ran lets the reviewer decide whether more is needed.
  - **Example:** run the test runner's filter for the feature (for example `pytest -k refund`, `npm test -- refund` or `dotnet test --filter Refund`), then the folder that holds its neighbours.

- `[H]` **SHOULD** Test runs write JUnit XML reports (read by almost every CI system) and use readable test names, so a reviewer can read what the suite promises without reading the code.
  - **Benefit:** JUnit XML lets CI dashboards show failures per test. Readable names turn the test list into a specification.
  - **Example:** write the report to a `test-reports/` folder that CI uploads as an artifact.

---

## Self-check before finishing

Run these before handing back a change. Each line checks one rule from the category pages. Every command that says "must be empty" should return no output. The variables are set per project; the values for common stacks are in [Stack mapping](../stacks/README.md#self-check-settings-per-stack).

```bash
# Export these per project (values per stack: see the stack mapping).
: "${TEMPLATES:?}" "${HANDLERS:?}" "${DATA_ACCESS_RE:?}"
status=0
grep -rn '<script' "$TEMPLATES" | grep -v 'src=' && status=1   # must be empty
grep -rn '<style' "$TEMPLATES" && status=1                     # must be empty
grep -rn ' style=' "$TEMPLATES" && status=1                    # must be empty
grep -rnE '[[:space:]]on(click|change|submit|input|keydown)=' "$TEMPLATES" && status=1   # must be empty
grep -rn '<table' "$TEMPLATES" && status=1                     # lists must use cards
grep -rnE "$DATA_ACCESS_RE" $HANDLERS && status=1              # must be empty; $HANDLERS unquoted on purpose (lists, globs)
# run the project's missing-translation check: no missing keys
[ "$status" -eq 0 ]
```

| Check | Rule it enforces | Why the check is worth running |
|---|---|---|
| `<script` in templates | [No inline scripts](../frontend/views-and-components.md#no-inline-scripts-or-handlers) | Keeps a strict Content-Security-Policy possible |
| `<style` and `style=` in templates | [No inline styles](../frontend/views-and-components.md#no-inline-styles) | Styles stay in one place and survive themes |
| `on…=` handlers | [No inline scripts](../frontend/views-and-components.md#no-inline-scripts-or-handlers) | Native handlers miss re-renders |
| `<table` in templates | [Cards instead of tables](../frontend/views-and-components.md#cards-instead-of-tables) | Tables overflow on phones |
| Data access in handlers | [No queries in controllers or UI components](../architecture/layering-and-patterns.md#no-queries-in-controllers-or-ui-components) | Business rules stay in services |
| Missing translation keys | [Locale coverage](../i18n/translations.md#locale-coverage) | Users otherwise see raw keys |

A grep is a fast first pass, not a proof. A match can be a false positive, such as a `<table` inside a print template that is excluded on purpose. Read each match before you decide.

---

**Related:** [Code quality](../general/code-quality.md) (the formatter and analyzer, the other checks before hand-off) · [Git workflow](../git/workflow.md) · [Stack mapping](../stacks/README.md) · [Summary](../SUMMARY.md)
