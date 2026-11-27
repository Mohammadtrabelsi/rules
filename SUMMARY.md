[Rules index](README.md) › Summary

**Navigation:** [Table of contents](README.md#table-of-contents) · [How to read these rules](general/how-to-read.md) · [Stack mapping](stacks/README.md) · [Proposed rules](general/proposed-rules.md)

# Summary of all rules

A one-page résumé of every category. Each line links to the full rule file; **MUST** rules are never broken without approval, **SHOULD** rules are the default (see [How to read these rules](general/how-to-read.md)).

These rules apply to any web site or application, in any language or framework. For the framework names of each concept, see the [stack mapping](stacks/README.md).

## General ([code quality](general/code-quality.md))

- **MUST** Explicit types and strict mode where the language offers them; descriptive names.
- **MUST** Run the formatter and the static analyzer on changed files before committing; fix new findings, don't grow the baseline.
- **MUST** Honest hand-off: say which tests, formatter and analyzer ran (or didn't, and why), and name any migration or build step needed.
- **SHOULD** Small functions, early returns, no dead or commented-out code; no new docs files unless asked.

## Architecture ([layering and patterns](architecture/layering-and-patterns.md))

- **MUST** One-way flow: entry point → service → data access. No queries, direct writes or business rules in controllers, route handlers or UI components.
- **MUST** Logic lives in a service layer, one service per aggregate, injected. Services return data, never views or HTTP responses.
- **MUST** Authorization rules per entity with `{entity}.{action}` permission names; reusable UI components for repeated markup; reuse existing code before adding new.
- **MUST** No new top-level folders and no dependency changes without approval.
- **SHOULD** Enums for statuses, shared behaviour in mixins or traits, events and queued listeners for side effects, data transfer objects past 3–4 arguments, interfaces for swappable providers, no extra repository layer.

## Frontend: views ([views and components](frontend/views-and-components.md))

- **MUST** No logic in templates, no inline styles or style blocks, no inline script blocks or inline event handlers. Use the server-driven update mechanism, then small client state, then bundled modules. Keeps a strict Content-Security-Policy possible.
- **MUST** Cards, not tables, for admin and list screens (tables only for real reports, stacked on phones).
- **MUST** One design system per project, with a prefix and its shared components.
- **MUST** WCAG 2.2 AA accessibility and a right-to-left layout for Arabic; state the build step after any stylesheet or script change.
- **SHOULD** At most two sections per component, grouped navigation with breadcrumbs, mobile first with no horizontal scroll.

## Frontend: routes ([routes and screens](frontend/routes-and-screens.md))

- **MUST** Create and edit forms are full pages on their own routes, not modals; separate reports or areas get separate routes.
- **MUST** English kebab-case URLs and route names; build links from named routes; protect admin route groups with a permission check.
- **SHOULD** Filters in the query string, 25 items per page, standard action names, versioned APIs (`/api/v1`) with one definition per response shape.

## Backend ([data and performance](backend/data-and-performance.md))

- **MUST** Every schema or data change is a versioned migration; columns sized for real data; money as integer minor units or decimal, never floating point.
- **MUST** No N+1 queries: load related data in one query or batch, and make accidental lazy loading fail loudly outside production.
- **SHOULD** Index foreign keys and filter columns, tiered seeders in all locales, background work for long tasks, cache expensive aggregates, wrap multi-step writes in a transaction.

## i18n ([translations](i18n/translations.md))

- **MUST** Every visible string goes through the translation function, in per-feature bundles; no catch-all file for new keys.
- **MUST** Every key in every supported locale; run the missing-key check and fill every placeholder marker.
- **MUST** Arabic is right-to-left: `dir` and `lang` on `<html>`, logical layout properties (start and end, not left and right).
- **SHOULD** Missing-translation tests, translatable database content per locale, locale kept through login, named placeholders and plural forms, locale-aware formatting.

## Security ([security](security/security.md))

- **MUST** Rate-limit every public form and endpoint with a named, configurable limit declared in one place, keyed by form and address.
- **MUST** Every create, read, update and delete goes through an authorization rule on the server; users see only their own tenant, building or space.
- **MUST** Financial records use soft delete only, never a permanent delete; changes logged with who, what, and old and new values.
- **MUST** Server-side validation with allow-listed fields, escaped output, CSRF protection on, no secrets in code, environment files never committed.
- **SHOULD** Honeypots on public forms, GDPR consent and export, security headers, signed expiring links, OWASP Top 10.

## Testing ([testing](testing/testing.md))

- **MUST** Automated tests for every behaviour change, including failure paths and authorization (not for pure copy or styling).
- **MUST** Never delete or skip a test to get green; run the narrowest relevant tests and report exactly what ran.
- **SHOULD** JUnit XML reports and readable test names; run the [self-check](testing/testing.md#self-check-before-finishing) before finishing.

## Git ([workflow](git/workflow.md))

- **MUST** Branch from the integration branch (`feature/`, `bugfix/`, `refactor/`, `docs/`, `chore/`) and open pull requests against it, never against the release branch.
- **MUST** Conventional commits `type(scope): subject`; no force-push to, or direct push of, the integration or release branch.
- **SHOULD** One concern per pull request, under about 400 changed lines, with a description listing changes, migrations, build steps and tests.

## AI agents ([prompt](ai-agents/README.md))

- Paste [`ai-agents/CLAUDE.md`](ai-agents/CLAUDE.md) into a project's instruction file. It keeps the MUST rules, a self-check and a checklist, and every numbered rule is traced to its section.

## Originals

- The unchanged source files are in [`originals/`](originals/): [`CLAUDE.md`](originals/CLAUDE.md) (a framework-specific prompt, kept for reference) and [`Mohammad-Development-Rules.pdf`](originals/Mohammad-Development-Rules.pdf). <!-- lint:allow -->
