# rules

Mohammad's personal coding rules and development guidelines, organized by category.

They apply to every Laravel 13 + Livewire project (Livewire 3/4, Alpine, Tailwind, Pest, PHP 8.4). Start with [How to read these rules](general/how-to-read.md) for the `[H]` / `[+]` tags and the MUST / SHOULD levels.

## Categories

| Folder | What's in it |
|---|---|
| [`general/`](general/) | [How to read the rules](general/how-to-read.md), [code quality](general/code-quality.md) (PHP style, Pint, PHPStan, honest hand-offs) |
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
