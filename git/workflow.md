[Rules index](../README.md) › Git workflow

**Navigation:** Previous: [Testing](../testing/testing.md) · Next: [AI agent prompt](../ai-agents/README.md) · [Table of contents](../README.md#table-of-contents)

# Git workflow and delivery

All work lands on `develop` through a pull request; `main` only receives releases.

The point of this workflow is that every change is reviewed, tested and traceable before it reaches the branch that users depend on.

---

## Branches and pull requests

- `[H]` **MUST** Branch from `develop` (`feature/`, `bugfix/`, `refactor/`, `docs/`, `chore/`) and open the PR against `develop`, never `main`.
  - **Benefit:** `develop` is where changes are integrated and tested together. `main` holds what is released. Branching from `develop` means the branch includes everything already accepted, so the PR shows conflicts early. The prefix tells a reviewer the kind of change before they open it.
  - **Example:** `feature/invoice-refunds`, `bugfix/dues-rounding`, `chore/bump-pest`.

- `[H]` **SHOULD** One concern per PR; merge `develop` into the branch and resolve conflicts before review, keeping `develop`'s side unless asked otherwise.
  - **Benefit:** A PR about one thing can be reviewed and reverted on its own. A mixed PR ("refund fix plus new dashboard") is hard to approve, and reverting it removes both. Merging `develop` before review means the reviewer sees the code as it will land.
  - **Deviate when:** The branch's own change is the conflicting side and you were asked to keep it. State the choice in the PR.

- `[+]` **SHOULD** Keep PRs reviewable (roughly under 400 changed lines where possible).
  - **Benefit:** Review quality drops sharply after a few hundred lines; a reviewer skims and misses the bug. A small PR is reviewed faster, merged sooner, and produces a cleaner history.
  - **Deviate when:** A generated file, a large rename or a mechanical migration is big by nature. Keep the hand-written part small and say what the rest is.

---

## Commits

- `[H]` **MUST** Conventional commit messages: `type(scope): subject` (`feat`, `fix`, `refactor`, `docs`, `chore`, `test`).
  - **Benefit:** A consistent message reads well in `git log` and in release notes, and tools can group commits by type. `fix(billing): round dues to minor units` tells a reader what changed and where without opening the diff.
  - **Example:**
    ```text
    feat(payments): allow partial refunds
    fix(dues): round monthly amount half-up
    test(invoices): cover refund of an already-paid invoice
    ```

- `[H]` **MUST** No force-push to `develop` or `main`; no direct pushes to `main`.
  - **Benefit:** Force-pushing rewrites shared history. Anyone who has pulled `develop` then has a diverged copy, and commits can be silently lost. Keeping `main` pushes indirect means every release goes through a reviewed PR.
  - **Deviate when:** Never on these two branches. On your own feature branch, a force push is allowed when you are the only one using it and you say so.

---

## Writing the PR

- `[H]` **SHOULD** PR descriptions list what changed, migrations to run, build steps (`npm run build`) and what was and wasn't tested, and stay accurate.
  - **Benefit:** The description is what the reviewer and the person deploying read. A list of migrations and build steps prevents a deploy that breaks because a step was forgotten. Stating what was not tested tells the reviewer where to look harder.
  - **Example:**
    ```markdown
    ## Changes
    - Partial refunds on `PaymentService::refund()`

    ## Migrations
    - `php artisan migrate` (adds `refunded_minor` to `payments`)

    ## Build
    - None (no CSS or JS changes)

    ## Tested
    - `pest --filter=PaymentRefund`: 14 passed
    - Not run: full suite (about 20 minutes; run in CI)
    ```
  - **Deviate when:** A PR is a one-line typo fix. A short description is enough, but it should still say what changed.

---

**Related:** [Code quality](../general/code-quality.md) (the honest hand-off) · [Testing](../testing/testing.md) (what the PR must say was tested) · [Summary](../SUMMARY.md)
