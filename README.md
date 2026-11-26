# rules

Mohammad's personal coding rules and development guidelines, organized by category.

They apply to every Laravel 13 + Livewire project (Livewire 3/4, Alpine, Tailwind, Pest, PHP 8.4). Each rule says **what** to do, **why** it is worth doing (its benefit), and when a deviation is acceptable.

**New here?** Read [How to read these rules](general/how-to-read.md) first (about five minutes). It explains the `[H]` / `[+]` tags and the MUST / SHOULD levels. For a one-page overview, read the [summary](SUMMARY.md).

## Table of contents

Every page has a breadcrumb at the top and previous/next links, so you can read straight through or jump to a topic.

### General

- [How to read these rules](general/how-to-read.md): notation, rule anatomy, tags and levels, the benefit principle
- [Code quality](general/code-quality.md): PHP style, tooling (Pint, PHPStan), honest hand-off, docs
  - [Style](general/code-quality.md#style) · [Tooling](general/code-quality.md#tooling) · [Hand-off and docs](general/code-quality.md#hand-off-and-docs)
- [Proposed rules](general/proposed-rules.md): ideas not yet adopted, each with its benefit

### Architecture

- [Layering and patterns](architecture/layering-and-patterns.md): the request flow, services, policies, enums, DTOs
  - [Thin entry points](architecture/layering-and-patterns.md#thin-entry-points) · [Design patterns](architecture/layering-and-patterns.md#design-patterns) · [Principles](architecture/layering-and-patterns.md#principles)

### Frontend

- [Views and components](frontend/views-and-components.md): no inline PHP, CSS or JS; cards not tables; accessibility
  - [No inline PHP, CSS or JS](frontend/views-and-components.md#no-inline-php-css-or-js) · [Layout and components](frontend/views-and-components.md#layout-and-components)
- [Routes and screens](frontend/routes-and-screens.md): one URL per task, English kebab-case, named routes, query-string filters
  - [Own route per task](frontend/routes-and-screens.md#own-route-per-task) · [Naming](frontend/routes-and-screens.md#naming) · [Filters, pages and lists](frontend/routes-and-screens.md#filters-pages-and-lists)

### Backend

- [Data and performance](backend/data-and-performance.md): migrations, money types, indexes, N+1, queues, transactions
  - [Schema and money](backend/data-and-performance.md#schema-and-money) · [Indexes and seeders](backend/data-and-performance.md#indexes-and-seeders) · [Queues and performance](backend/data-and-performance.md#queues-and-performance)

### Internationalisation

- [Translations](i18n/translations.md): per-feature bundles, every locale, right-to-left for Arabic
  - [Keys and bundles](i18n/translations.md#keys-and-bundles) · [Locale coverage](i18n/translations.md#locale-coverage) · [Right-to-left (Arabic)](i18n/translations.md#right-to-left-arabic)

### Security

- [Security](security/security.md): rate limiting, policies, tenant scoping, soft deletes, audit log
  - [Rate limiting](security/security.md#rate-limiting) · [Authorization and data protection](security/security.md#authorization-and-data-protection)

### Testing

- [Testing](testing/testing.md): Pest rules, integrity of the suite, the pre-hand-off self-check
  - [What to test](testing/testing.md#what-to-test) · [Integrity of the suite](testing/testing.md#integrity-of-the-suite) · [Self-check before finishing](testing/testing.md#self-check-before-finishing)

### Git

- [Git workflow](git/workflow.md): branch from `develop`, conventional commits, PR contents
  - [Branches and pull requests](git/workflow.md#branches-and-pull-requests) · [Commits](git/workflow.md#commits) · [Writing the PR](git/workflow.md#writing-the-pr)

### AI agents

- [Agent prompt](ai-agents/README.md): the short version to paste into a project's `CLAUDE.md` or `AGENTS.md`
- [`CLAUDE.md`](ai-agents/CLAUDE.md): the prompt itself, with the MUST rules and the pre-finish checklist

### Originals

- [`originals/`](originals/): the unchanged source files, [`CLAUDE.md`](originals/CLAUDE.md) and [`Mohammad-Development-Rules.pdf`](originals/Mohammad-Development-Rules.pdf)

## Categories

| Folder | What's in it |
|---|---|
| [`general/`](general/) | [How to read the rules](general/how-to-read.md), [code quality](general/code-quality.md) (PHP style, Pint, PHPStan, honest hand-offs), [proposed rules](general/proposed-rules.md) |
| [`architecture/`](architecture/) | [Layering and patterns](architecture/layering-and-patterns.md): thin controllers/Livewire, service layer, policies, enums, DTOs |
| [`frontend/`](frontend/) | [Views and components](frontend/views-and-components.md) (no inline PHP/CSS/JS, cards not tables, accessibility) and [routes and screens](frontend/routes-and-screens.md) |
| [`backend/`](backend/) | [Data and performance](backend/data-and-performance.md): migrations, money types, indexes, N+1, queues, transactions |
| [`i18n/`](i18n/) | [Translations](i18n/translations.md): per-feature lang bundles, every locale, RTL for Arabic |
| [`security/`](security/) | [Security](security/security.md): rate limiting, policies, tenant scoping, soft deletes, audit log |
| [`testing/`](testing/) | [Testing](testing/testing.md): Pest rules and the pre-hand-off self-check |
| [`git/`](git/) | [Git workflow](git/workflow.md): branch from `develop`, conventional commits, PR contents |
| [`ai-agents/`](ai-agents/) | [`CLAUDE.md`](ai-agents/CLAUDE.md), the short prompt to paste into a project's `CLAUDE.md` or `AGENTS.md` |
| [`originals/`](originals/) | The original source files, unchanged: [`CLAUDE.md`](originals/CLAUDE.md) and [`Mohammad-Development-Rules.pdf`](originals/Mohammad-Development-Rules.pdf) |

## License

[GPL-3.0](LICENSE)
