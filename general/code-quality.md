[Rules index](../README.md) › General › Code quality

**Navigation:** Previous: [How to read these rules](how-to-read.md) · Next: [Layering and patterns](../architecture/layering-and-patterns.md) · [Table of contents](../README.md#table-of-contents)

# Code quality

A change is done only when format, static analysis and the relevant tests pass. (Testing rules: see [`../testing/testing.md`](../testing/testing.md).)

This page covers how code is written (style), how it is checked (tooling), and how work is handed back (hand-off and docs).

---

## Style

### PHP 8.4 style

- `[H]` **MUST** PHP 8.4 style: strict types, explicit return and parameter types, constructor property promotion, curly braces on every control structure, generic PHPDoc for collections (`Collection<int, User>`), `@property` annotations on models and components.
  - **Benefit:** Types make the code self-describing and let PHPStan find whole classes of bugs before runtime. Braces on every `if` prevent the classic bug where a second line added later sits outside the condition.
  - **Example:**
    ```php
    declare(strict_types=1);

    final class InvoiceTotals
    {
        public function __construct(
            private readonly int $subtotalMinor,
            private readonly int $taxMinor,
        ) {}

        public function grossMinor(): int
        {
            return $this->subtotalMinor + $this->taxMinor;
        }
    }
    ```
  - **Deviate when:** Almost never. A generated file or a third-party stub may force a different shape; keep the deviation inside that file.

- `[H]` **MUST** Descriptive names (`isRegisteredForDiscounts`, not `discount()`); PHPDoc only where logic is not obvious.
  - **Benefit:** A name that says what the method answers removes the need to open it. Reviewers can judge a call site without reading the body.
  - **Deviate when:** A name that is the domain's own term (for example, a legal or accounting word) is more precise than a descriptive one. Use the domain term and say what it means in one PHPDoc line.

- `[+]` **SHOULD** Small functions, early returns, no dead code, no commented-out code.
  - **Benefit:** Early returns keep the happy path at the left margin and make each guard obvious. Commented-out code looks like it might matter, so people hesitate to delete it, and it rots. Version control already keeps the old version.
  - **Example:**
    ```php
    public function canRefund(Payment $payment): bool
    {
        if ($payment->isRefunded()) {
            return false;
        }

        return $payment->amountMinor > 0;
    }
    ```

---

## Tooling

- `[H]` **MUST** Run `vendor/bin/pint --dirty` and PHPStan/Larastan (level 5 or the project's level) before committing; fix new errors instead of growing the baseline.
  - **Benefit:** Pint removes formatting debates from review, so diffs contain only meaningful changes. PHPStan catches type and null mistakes early. A baseline that only shrinks keeps the existing debt visible and stops new debt from hiding in it.
  - **Example:** `vendor/bin/pint --dirty` formats only files changed in the working tree. Then run `vendor/bin/phpstan analyse`, and check that the error count did not rise.
  - **Deviate when:** The project sets its own PHPStan level. Use that level, and never lower it to pass.

---

## Hand-off and docs

- `[H]` **MUST** Be honest in the hand-off: say exactly which tests, Pint and PHPStan ran, and which could not run and why. Mention any `php artisan migrate` or `npm run build` needed.
  - **Benefit:** The person receiving the work knows what has been verified and what has not. A silent skip looks like a pass until it fails in production. Naming the `migrate` and `npm run build` steps stops the change from appearing to work locally while the database or assets are stale.
  - **Example of a good hand-off:** "Ran `pint --dirty` (clean), PHPStan (0 new errors), and `InvoiceRefundTest` (12 passed). Did not run the browser suite because Chromium is not available here. Needs `php artisan migrate` and `npm run build`."

- `[H]` **SHOULD** Don't create documentation files unless asked; when docs exist, keep the generated codebase reference current.
  - **Benefit:** Extra markdown files go stale quickly, and stale docs mislead more than missing docs. Keeping the existing reference current means one trusted source.
  - **Deviate when:** The person asks for documentation, or the project already maintains a reference that a change makes wrong. Then update that reference in the same change.

---

**Related:** [Testing](../testing/testing.md) (the tests this hand-off must name) · [Git workflow](../git/workflow.md) (the PR that carries the hand-off) · [Summary](../SUMMARY.md)
