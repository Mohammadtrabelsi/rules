[Rules index](../README.md) › Git workflow

**Navigation:** Previous: [Testing](../testing/testing.md) · Next: [AI agent prompt](../ai-agents/README.md) · [Table of contents](../README.md#table-of-contents)

# Git workflow and delivery

All work lands on the integration branch (`develop`, or the project's equivalent) through a pull request. The release branch (`main`, or the project's equivalent) receives only releases.

The point of this workflow is that every change is reviewed, tested and traceable before it reaches the branch that users depend on.

---

## Branches and pull requests

- `[H]` **MUST** Branch from the integration branch with a prefix that names the kind of change (`feature/`, `bugfix/`, `refactor/`, `docs/`, `chore/`). Open the pull request against the integration branch, never against the release branch.
  - **Benefit:** The integration branch is where changes are combined and tested together. The release branch holds what is released. Branching from the integration branch means the branch includes everything already accepted, so the pull request shows conflicts early. The prefix tells a reviewer the kind of change before they open it.
  - **Example:** `feature/invoice-refunds`, `bugfix/dues-rounding`, `chore/bump-test-runner`.

- `[H]` **SHOULD** One concern per pull request. Merge the integration branch into the branch and resolve conflicts before review, keeping the integration branch's side unless asked otherwise.
  - **Benefit:** A pull request about one thing can be reviewed and reverted on its own. A mixed pull request ("refund fix plus new dashboard") is hard to approve, and reverting it removes both. Merging the integration branch before review means the reviewer sees the code as it will land.
  - **Deviate when:** The branch's own change is the conflicting side and you were asked to keep it. State the choice in the pull request.

- `[+]` **SHOULD** Keep pull requests reviewable, roughly under 400 changed lines where possible.
  - **Benefit:** Review quality drops sharply after a few hundred lines; a reviewer skims and misses the bug. A small pull request is reviewed faster, merged sooner, and produces a cleaner history.
  - **Deviate when:** A generated file, a large rename or a mechanical migration is big by nature. Keep the hand-written part small and say what the rest is.

---

## Commits

- `[H]` **MUST** Conventional commit messages: `type(scope): subject`, with a type such as `feat`, `fix`, `refactor`, `docs`, `chore` or `test`.
  - **Benefit:** A consistent message reads well in the history and in release notes, and tools can group commits by type. `fix(billing): round dues to minor units` tells a reader what changed and where without opening the diff.
  - **Example:**
    ```text
    feat(payments): allow partial refunds
    fix(dues): round monthly amount half-up
    test(invoices): cover refund of an already-paid invoice
    ```

- `[H]` **MUST** No force-push to the integration or release branch, and no direct pushes to the release branch.
  - **Benefit:** Force-pushing rewrites shared history. Anyone who has pulled the integration branch then has a diverged copy, and commits can be silently lost. Keeping release pushes indirect means every release goes through a reviewed pull request.
  - **Deviate when:** Never on these two branches. On your own feature branch, a force-push is allowed when you are the only one using it and you say so.

---

## Writing the pull request

- `[H]` **SHOULD** Pull request descriptions list what changed, the migrations to run, the build steps, and what was and was not tested. Keep them accurate as the change evolves.
  - **Benefit:** The description is what the reviewer and the person deploying read. A list of migrations and build steps prevents a deploy that breaks because a step was forgotten. Stating what was not tested tells the reviewer where to look harder.
  - **Example:**
    ```markdown
    ## Changes
    - Partial refunds in the payment service

    ## Migrations
    - Run the migration step (adds `refunded_minor` to `payments`)

    ## Build
    - None (no stylesheet or script changes)

    ## Tested
    - `pytest -k refund`: 14 passed
    - Not run: full suite (about 20 minutes; runs in CI)
    ```
  - **Deviate when:** A pull request is a one-line typo fix. A short description is enough, but it should still say what changed.

---

**Related:** [Code quality](../general/code-quality.md) (the honest hand-off) · [Testing](../testing/testing.md) (what the pull request must say was tested) · [Summary](../SUMMARY.md)
