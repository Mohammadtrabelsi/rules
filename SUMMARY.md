# Summary of all rules

A one-page résumé of every category. Each line links to the full rule file; **MUST** rules are never broken without approval, **SHOULD** rules are the default (see [How to read these rules](general/how-to-read.md)).

Stack: Laravel 13, Livewire 3/4, Alpine, Tailwind, Pest, PHP 8.4. If a rule conflicts with the task, stop and ask.

## General ([code quality](general/code-quality.md))

- **MUST** PHP 8.4 style: strict types, explicit types, constructor promotion, braces everywhere, generic PHPDoc for collections, descriptive names.
- **MUST** Run `vendor/bin/pint --dirty` and PHPStan/Larastan before committing; fix new errors, don't grow the baseline.
- **MUST** Honest hand-off: say which tests, Pint and PHPStan ran (or didn't, and why), and mention any `migrate` or `npm run build` needed.
- **SHOULD** Small functions, early returns, no dead or commented-out code; no new docs files unless asked.

## Architecture ([layering and patterns](architecture/layering-and-patterns.md))

- **MUST** One-way flow: route → controller/Livewire → service → model. No Eloquent, `DB::` or business rules in controllers or Livewire.
- **MUST** Logic lives in `app/Services/<Domain>Service`, one per aggregate, injected (constructor, or `boot()` into a `protected` property in Livewire); services return data, never views or responses.
- **MUST** Policies per entity with `{entity}.{action}` permissions; reusable Blade components for repeated UI; reuse existing code before adding new.
- **MUST** No new top-level folders and no dependency changes without approval.
- **SHOULD** Enums for statuses, traits/concerns for shared behaviour, observers and queued listeners for side effects, DTOs past 3–4 arguments, interfaces for swappable providers, no extra repository layer.

## Frontend: views ([views and components](frontend/views-and-components.md))

- **MUST** No `@php` blocks or logic in Blade, no `style=` / `<style>`, no `<script>` or `onclick=`; use services, Tailwind or the project stylesheet, then `wire:*` → Alpine → Vite modules. Keeps a strict CSP possible.
- **MUST** Cards, not `<table>`, for admin and list screens (tables only for real reports, stacked on phones).
- **MUST** One design system per project (prefixed classes such as `rc-`, `ix-`) and its shared components.
- **MUST** WCAG 2.2 AA accessibility and `dir="rtl"` for Arabic; remind that `npm run build` is needed after CSS/JS changes.
- **SHOULD** At most two sections per component, grouped navigation with breadcrumbs, mobile first with no horizontal scroll.

## Frontend: routes ([routes and screens](frontend/routes-and-screens.md))

- **MUST** Create and edit forms are full-page components on their own routes, not modals; separate reports or areas get separate routes.
- **MUST** English kebab-case URLs and route names; named routes with `route()`; admin route groups behind permission middleware.
- **SHOULD** Filters in the query string, 25 items per page, RESTful names, versioned APIs (`/api/v1`) with API Resources.

## Backend ([data and performance](backend/data-and-performance.md))

- **MUST** Every schema or data change is a migration; columns sized for real data; money as integer minor units or `decimal`, never float.
- **MUST** No N+1: eager-load with `with()`, `Model::preventLazyLoading()` outside production.
- **SHOULD** Index foreign keys and filter columns, tiered seeders in all locales, queue long work, cache expensive aggregates, wrap multi-step writes in `DB::transaction()`.

## i18n ([translations](i18n/translations.md))

- **MUST** Every visible string goes through `__()` / `trans_choice()`, in per-feature bundles `lang/{locale}/{feature}.php`; no catch-all or JSON files for new keys.
- **MUST** Every key in every locale (en, fr, ar; plus de, es on OrganiCore); run `php artisan translations:sync` and fill every `[TODO]`.
- **MUST** Arabic is right-to-left: `dir`/`lang` on `<html>`, logical CSS (`ms-`/`me-`, `start`/`end`).
- **SHOULD** Missing-translation tests, translatable DB content per locale, locale kept through login, placeholders and locale-aware formatting.

## Security ([security](security/security.md))

- **MUST** Rate-limit every public form and endpoint with named `RateLimiter::for()` limiters (or the `ThrottlesSubmissions` trait in Livewire), configurable, keyed by form + IP. Reference: auth 6/min, API and webhooks 60/min, public forms 10/min.
- **MUST** Every CRUD action goes through a Policy (`{entity}.{action}`), checked with `@can` and again on the server; users see only their own tenant/building/space.
- **MUST** Financial records use soft deletes only, never `forceDelete`; changes logged with `spatie/laravel-activitylog`.
- **MUST** Server-side validation, safe mass assignment, escaped output, CSRF on, no secrets in code, `.env` never committed.
- **SHOULD** Honeypots on public forms, GDPR consent and export, security headers, signed URLs, OWASP Top 10.

## Testing ([testing](testing/testing.md))

- **MUST** Pest feature tests for every behaviour change, including failure paths and authorization (not for pure copy or styling).
- **MUST** Never delete or skip a test to get green; run the narrowest relevant tests and report exactly what ran.
- **SHOULD** JUnit/TestDox reports in `storage/test-reports/`; run the [self-check greps](testing/testing.md#self-check-before-finishing) before finishing.

## Git ([workflow](git/workflow.md))

- **MUST** Branch from `develop` (`feature/`, `bugfix/`, `refactor/`, `docs/`, `chore/`) and open PRs against `develop`, never `main`.
- **MUST** Conventional commits `type(scope): subject`; no force-push or direct push to `develop` or `main`.
- **SHOULD** One concern per PR, under about 400 lines, with a description listing changes, migrations, build steps and tests.

## AI agents ([prompt](ai-agents/README.md))

- Paste [`ai-agents/CLAUDE.md`](ai-agents/CLAUDE.md) into each project's `CLAUDE.md` or `AGENTS.md`. It keeps the MUST rules plus the grep guards and pre-hand-off checklist.

## Originals

- The unchanged source files are in [`originals/`](originals/): [`CLAUDE.md`](originals/CLAUDE.md) and [`Mohammad-Development-Rules.pdf`](originals/Mohammad-Development-Rules.pdf).
