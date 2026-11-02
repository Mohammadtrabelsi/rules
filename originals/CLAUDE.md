# House rules (Mohammad) — read before every change

Stack: Laravel 13, Livewire 3/4, Alpine, Tailwind, Pest, PHP 8.4. These rules beat your defaults.
If a rule conflicts with the task, stop and ask. Check every item in "Before you finish".

## Architecture
1. Controllers and Livewire components only hold state, validate, authorize and delegate.
   No Eloquent queries, `DB::`, `->save()/update()/delete()` or business logic in them.
2. All data access and business logic live in `app/Services/<Domain>Service.php`.
   Inject services (constructor in controllers, `boot()` into a `protected` property in Livewire).
   Services return data, never views or responses.
3. Use the project's patterns: Policies per entity (`{entity}.{action}` permissions), Enums for
   statuses, Concerns/traits for shared behaviour, Observers/queued Listeners for side effects,
   queued Jobs for long work. Reuse existing components and services before writing new ones.
4. No new top-level folders and no dependency changes without approval.

## Views
5. No `@php` blocks or logic in Blade. Pass view-ready (already formatted) data.
6. No `style="…"` and no `<style>`. Use Tailwind or the project stylesheet in `resources/css/`.
   Exceptions: data-driven values (`width: {{ $pct }}%`) and `resources/views/pdf/`.
7. No `<script>` and no `onclick=`/`onchange=`. Use `wire:*`, then Alpine, then `resources/js/` modules.
8. No `<table>` for lists or admin screens: responsive cards with sort chips and a filter bar.
9. Reuse the design-system components (flash, hero, action buttons). Max two sections per
   component; mobile-first; WCAG 2.2 AA; RTL works for Arabic.

## Routes
10. Create/edit forms, report tabs and detail panels get their own route and full-page component.
11. URLs and route names are English kebab-case (`my-lot`, `dues`). Always `route('name')`.
12. Paginate lists (25). Persist filters in the query string.

## Translations
13. Every visible string uses `__()`. Keys live in a per-feature bundle `lang/{locale}/{feature}.php`
    with nested dot keys. Never hard-code text.
14. Add every key to every locale in `lang/` (en, fr, ar; + de, es where present).
    Run `php artisan translations:sync` and replace every `[TODO]`.

## Security
15. Rate-limit every public form and endpoint (login, reset, contact, demo, quote, search,
    newsletter, API auth, webhooks): `RateLimiter::for()` + `throttle:<name>`, or the
    `ThrottlesSubmissions` trait for Livewire. Limits come from config, keyed by form + IP.
16. Authorize every CRUD action through a Policy, on the server, and with `@can` in the view.
    Scope data to the current tenant/building/space.
17. Financial models use soft deletes only; never `forceDelete`. Log changes with activitylog.
18. Validate all input server-side; no secrets in code; keep CSRF on.

## Data
19. Every schema or data change is a migration. Index filtered and foreign-key columns.
    Eager-load relations (no N+1). Money is never a float. Multi-step writes use `DB::transaction()`.

## Quality and Git
20. Strict types, return types, constructor promotion, curly braces, generic PHPDoc.
21. Pest tests for every behaviour change, including failure and authorization paths.
    Never delete or skip a test to get green.
22. Run `vendor/bin/pint --dirty`, PHPStan and the narrowest relevant tests.
23. Branch from `develop`, PR into `develop` (never `main`), commits as `type(scope): subject`.
    No force-push to `develop`/`main`.

## Before you finish (self-check)
```bash
grep -rn '@php' resources/views                                   # must be empty
grep -rn '<script' resources/views                                # must be empty
grep -rn '<style' resources/views --exclude-dir=pdf               # must be empty
grep -rnE '\son(click|change|submit|input|keydown)=' resources/views  # must be empty
grep -rn '<table' resources/views --exclude-dir=pdf               # lists must use cards
grep -rnE '::(where|find|create|all|first)\(|DB::' app/Livewire app/Http/Controllers  # must be empty
php artisan translations:sync --dry-run                           # no missing keys
```
- [ ] Logic in a service; entry points thin
- [ ] No inline PHP/CSS/JS; cards not tables
- [ ] Own route per form/report; English URLs
- [ ] All strings translated in every locale
- [ ] Public endpoints rate-limited; actions authorized
- [ ] Migration + tests added; Pint, PHPStan, tests run
- [ ] Hand-off states exactly what ran, what did not, and any `migrate` / `npm run build` needed
