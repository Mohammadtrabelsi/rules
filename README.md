# rules

Development rules for any web site or application, in any language or framework: server-rendered sites, single-page apps, APIs, static sites and anything in between.

Each rule says **what** to do, **why** it is worth doing (its benefit), and when a deviation is acceptable. The rules name roles such as "service layer" and "authorization rule", and no framework. Where a tool appears on a page (a formatter, a test runner), it is an example, and the rule holds without it. [Stack mapping](stacks/README.md) says how each role is named in the common web frameworks and languages.

**New here?** Read [How to read these rules](general/how-to-read.md) first (about five minutes). It explains the `[H]` / `[+]` tags and the MUST / SHOULD levels. For a one-page overview, read the [summary](SUMMARY.md).

**Using an AI coding agent?** Paste the [agent prompt](ai-agents/CLAUDE.md) into the project's instruction file. It keeps only the MUST rules and ends with a self-check.

## Table of contents

Every page has a breadcrumb at the top and previous/next links, so you can read straight through or jump to a topic.

### General

- [How to read these rules](general/how-to-read.md): notation, rule anatomy, tags and levels, the benefit principle
- [Code quality](general/code-quality.md): language style, tooling (formatter and analyzer), honest hand-off, docs
  - [Language style](general/code-quality.md#language-style) · [Tooling](general/code-quality.md#tooling) · [Hand-off and docs](general/code-quality.md#hand-off-and-docs)
- [Proposed rules](general/proposed-rules.md): ideas not yet adopted, each with its benefit

### Architecture

- [Layering and patterns](architecture/layering-and-patterns.md): the request flow, services, authorization rules, enums, data transfer objects
  - [Thin entry points](architecture/layering-and-patterns.md#thin-entry-points) · [Design patterns](architecture/layering-and-patterns.md#design-patterns) · [Principles](architecture/layering-and-patterns.md#principles)

### Frontend

- [Views and components](frontend/views-and-components.md): no logic, inline styles or inline scripts in templates; cards not tables; accessibility
  - [No logic, inline styles or inline scripts](frontend/views-and-components.md#no-logic-inline-styles-or-inline-scripts) · [Layout and components](frontend/views-and-components.md#layout-and-components)
- [Routes and screens](frontend/routes-and-screens.md): one URL per task, English kebab-case, named routes, query-string filters
  - [Own route per task](frontend/routes-and-screens.md#own-route-per-task) · [Naming](frontend/routes-and-screens.md#naming) · [Filters, pages and lists](frontend/routes-and-screens.md#filters-pages-and-lists)

### Backend

- [Data and performance](backend/data-and-performance.md): migrations, money types, indexes, N+1 queries, background work, transactions
  - [Schema and money](backend/data-and-performance.md#schema-and-money) · [Indexes and seeders](backend/data-and-performance.md#indexes-and-seeders) · [Queues and performance](backend/data-and-performance.md#queues-and-performance)

### Internationalisation

- [Translations](i18n/translations.md): per-feature bundles, every locale, right-to-left for Arabic
  - [Keys and bundles](i18n/translations.md#keys-and-bundles) · [Locale coverage](i18n/translations.md#locale-coverage) · [Right-to-left (Arabic)](i18n/translations.md#right-to-left-arabic)

### Security

- [Security](security/security.md): rate limiting, authorization, tenant scoping, soft delete, audit log
  - [Rate limiting](security/security.md#rate-limiting) · [Authorization and data protection](security/security.md#authorization-and-data-protection)

### Testing

- [Testing](testing/testing.md): test rules, integrity of the suite, the pre-hand-off self-check
  - [What to test](testing/testing.md#what-to-test) · [Integrity of the suite](testing/testing.md#integrity-of-the-suite) · [Self-check before finishing](testing/testing.md#self-check-before-finishing)

### Git

- [Git workflow](git/workflow.md): branch from the integration branch, conventional commits, pull request contents
  - [Branches and pull requests](git/workflow.md#branches-and-pull-requests) · [Commits](git/workflow.md#commits) · [Writing the pull request](git/workflow.md#writing-the-pull-request)

### Stacks

- [Stack mapping](stacks/README.md): how each concept is named in the common web frameworks; self-check settings per stack; one worked example set
  - [Concept map](stacks/README.md#concept-map) · [Self-check settings per stack](stacks/README.md#self-check-settings-per-stack) · [Examples in one stack](stacks/README.md#examples-in-one-stack) · [Static sites and no framework](stacks/README.md#static-sites-and-no-framework)

### AI agents

- [Agent prompt](ai-agents/README.md): how the short prompt is built and traced to its source sections
- [`CLAUDE.md`](ai-agents/CLAUDE.md): the prompt itself, with the MUST rules and the pre-finish checklist

### Originals

- [`originals/`](originals/): the unchanged earlier source, [`CLAUDE.md`](originals/CLAUDE.md) (a framework-specific prompt kept for reference) and [`Mohammad-Development-Rules.pdf`](originals/Mohammad-Development-Rules.pdf) <!-- lint:allow -->

## Categories

| Folder | What's in it |
|---|---|
| [`general/`](general/) | [How to read the rules](general/how-to-read.md), [code quality](general/code-quality.md) (style, formatter and analyzer, honest hand-offs), [proposed rules](general/proposed-rules.md) |
| [`architecture/`](architecture/) | [Layering and patterns](architecture/layering-and-patterns.md): thin entry points, service layer, authorization rules, enums, data transfer objects |
| [`frontend/`](frontend/) | [Views and components](frontend/views-and-components.md) (no inline logic, styles or scripts; cards not tables; accessibility) and [routes and screens](frontend/routes-and-screens.md) |
| [`backend/`](backend/) | [Data and performance](backend/data-and-performance.md): migrations, money types, indexes, N+1 queries, background work, transactions |
| [`i18n/`](i18n/) | [Translations](i18n/translations.md): per-feature bundles, locale coverage, right-to-left for Arabic |
| [`security/`](security/) | [Security](security/security.md): rate limiting, authorization, tenant scoping, soft delete, audit log |
| [`testing/`](testing/) | [Testing](testing/testing.md): test rules and the pre-hand-off self-check |
| [`git/`](git/) | [Git workflow](git/workflow.md): integration branch, conventional commits, pull request contents |
| [`stacks/`](stacks/) | [Stack mapping](stacks/README.md): framework names for each concept, self-check settings per stack, example code for one stack |
| [`ai-agents/`](ai-agents/) | [`CLAUDE.md`](ai-agents/CLAUDE.md), the short prompt for AI agents, and its [source table](ai-agents/README.md) |
| [`originals/`](originals/) | The original source files, unchanged: [`CLAUDE.md`](originals/CLAUDE.md) and [`Mohammad-Development-Rules.pdf`](originals/Mohammad-Development-Rules.pdf) |

## Checks

The rules are checked by a small static-analysis script and a unit test suite. Both use only the Python standard library, so they run anywhere without installing anything. They are tested on Python 3.11, 3.12 and 3.13. Run them from the repository root:

```bash
python3 tools/check_rules.py --metrics     # static checks: links, anchors, structure, numbering, sync, lint, budget
python3 -m unittest discover -s tests -v   # unit tests for the checker, plus a gate that the real content passes
```

The static checks verify that every link and heading anchor resolves, every page is reachable from this README, every rule has a tag, a level and a benefit, the agent prompt is numbered without gaps and traced to MUST rules, its self-check matches the one in the testing page, the category pages stay free of framework-specific names, and the agent prompt stays within its word budget. The same checks run in continuous integration on every push and pull request.

## License

[GPL-3.0](LICENSE)
