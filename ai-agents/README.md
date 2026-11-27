[Rules index](../README.md) › AI agents

**Navigation:** Previous: [Git workflow](../git/workflow.md) · Next: [Stack mapping](../stacks/README.md) · [Table of contents](../README.md#table-of-contents)

# AI agent prompt

[`CLAUDE.md`](CLAUDE.md) is the short version of the rules for AI coding agents. Paste it into a project's `CLAUDE.md` or `AGENTS.md`, or any other instruction file the agent reads at the start of a session. It works for any language or framework: it names no stack, and it tells the agent to map each term onto the project it is working in.

It keeps only **MUST** rules, numbered, and ends with a self-check and a checklist the agent runs before handing back.

## Why a short version exists

An agent reads its instructions on every task. A long document is partly skipped, and the rules most likely to be missed are the ones buried in the middle. The short prompt keeps every MUST rule in a numbered list the agent can check one by one, and it puts the self-check at the end, where the agent reads it last.

| Use this | When |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Pasting into a project's instruction file: the agent needs the rules and checklist every session |
| The category pages (linked from the [table of contents](../README.md#table-of-contents)) | A person wants the reason behind a rule, the example, or when a deviation is acceptable |
| The [summary](../SUMMARY.md) | A one-page review of every category |
| The [stack mapping](../stacks/README.md) | The project uses a framework, and the agent needs the concrete names for a concept |

## Where each numbered rule comes from

Every numbered rule in `CLAUDE.md` is traced to the section of a category page that states it. The table below is that trace. `tools/check_rules.py` reads it and fails when:

- a numbered rule has no row here, or a row matches no numbered rule;
- a row points at a file or heading that does not exist;
- the section it points at contains no **MUST** rule.

| # | Rule | Source |
|---|---|---|
| 1 | Entry points stay thin | [Thin entry points](../architecture/layering-and-patterns.md#thin-entry-points) |
| 2 | Logic in services | [One service per aggregate](../architecture/layering-and-patterns.md#one-service-per-aggregate) |
| 3 | Authorization on every action | [Authorization and data protection](../security/security.md#authorization-and-data-protection) |
| 4 | Reuse and no new folders | [Principles](../architecture/layering-and-patterns.md#principles) |
| 5 | No logic in templates | [No logic in templates](../frontend/views-and-components.md#no-logic-in-templates) |
| 6 | No inline styles | [No inline styles](../frontend/views-and-components.md#no-inline-styles) |
| 7 | No inline scripts | [No inline scripts or handlers](../frontend/views-and-components.md#no-inline-scripts-or-handlers) |
| 8 | Cards, not tables | [Cards instead of tables](../frontend/views-and-components.md#cards-instead-of-tables) |
| 9 | Design system, WCAG, right-to-left | [Accessibility](../frontend/views-and-components.md#accessibility) |
| 10 | Own route per form or report | [Own route per task](../frontend/routes-and-screens.md#own-route-per-task) |
| 11 | English kebab-case URLs | [Naming](../frontend/routes-and-screens.md#naming) |
| 12 | Every string translated | [Keys and bundles](../i18n/translations.md#keys-and-bundles) |
| 13 | Every key in every locale | [Locale coverage](../i18n/translations.md#locale-coverage) |
| 14 | Rate-limit public endpoints | [Rate limiting](../security/security.md#rate-limiting) |
| 15 | Tenant scoping | [Authorization and data protection](../security/security.md#authorization-and-data-protection) |
| 16 | Soft delete and audit log | [Authorization and data protection](../security/security.md#authorization-and-data-protection) |
| 17 | Server-side validation, CSRF, no secrets | [Authorization and data protection](../security/security.md#authorization-and-data-protection) |
| 18 | Migrations and money types | [Schema and money](../backend/data-and-performance.md#schema-and-money) |
| 19 | No N+1 queries | [Queues and performance](../backend/data-and-performance.md#queues-and-performance) |
| 20 | Explicit types | [Language style](../general/code-quality.md#language-style) |
| 21 | Tests for every change | [What to test](../testing/testing.md#what-to-test) |
| 22 | Formatter and analyzer | [Tooling](../general/code-quality.md#tooling) |
| 23 | Branches and commits | [Branches and pull requests](../git/workflow.md#branches-and-pull-requests) |

## Keeping the prompt in step

`CLAUDE.md` is generated from the category pages by hand, so the trace above is the safety net. When a MUST rule changes on a category page, change the matching line in `CLAUDE.md` in the same commit. Keep the numbering stable, so a reviewer can compare the two. The checker then confirms the trace still holds, and that the self-check block in `CLAUDE.md` is identical to the one in [Testing](../testing/testing.md#self-check-before-finishing).

`originals/CLAUDE.md` is the earlier, framework-specific prompt, kept unchanged for reference. Do not copy it into new projects.
