# Data and performance

Schema changes go through migrations, queries are indexed and eager-loaded, and heavy work runs in the queue. (Service layer rules: see [`../architecture/layering-and-patterns.md`](../architecture/layering-and-patterns.md).)

- `[H]` **MUST** Every schema or data change is a migration (including one-off data fixes such as repricing); never edit the database by hand. Mention `php artisan migrate` in the hand-off.
- `[H]` **MUST** Size columns for real data (the quote reference overflow); money as integer minor units or `decimal`, never float.
- `[H]` **SHOULD** Index foreign keys and every column used in `where`, `orderBy` or status filters.
- `[H]` **SHOULD** Seeders come in tiers (minimal / demo / full) and seed realistic data for every building or tenant, in all locales.
- `[H]` **SHOULD** Queue long-running work; queued listeners for notifications.
- `[+]` **MUST** No N+1 queries: eager-load relations (`with()`), enable `Model::preventLazyLoading()` outside production.
- `[+]` **SHOULD** Cache expensive read-only aggregates (dashboards, feature flags) and invalidate on write; read settings once per request.
- `[+]` **SHOULD** Wrap multi-step writes in `DB::transaction()` inside the service.
