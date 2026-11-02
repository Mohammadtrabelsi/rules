# Architecture and layering

Every request flows one way: **route → controller or Livewire component → service → model**, and the view only renders what it is handed.

## Thin entry points

- `[H]` **MUST** Controllers and Livewire components contain no Eloquent queries (`::where`, `::find`, `::create`), no `DB::`, no `->save()/->update()/->delete()` and no business rules. They hold UI state, validate, authorize, delegate to a service and map the result back.
- `[H]` **MUST** All data access and business logic live in a `<Domain>Service` under `app/Services/` (sub-domains in sub-folders, e.g. `app/Services/Payroll/`). One service per aggregate, not one per table.
- `[H]` **MUST** Inject services: constructor or action type-hint in controllers; `boot()` into a `protected` property in Livewire (never a public, serialized property). Never `new`, `app()` or facades to reach models.
- `[H]` **MUST** Services return domain data (models, collections, paginators, DTOs, arrays), never views or HTTP responses.
- `[H]` **SHOULD** Cross-cutting concerns (notifications, activity log, PDF, exports, CRUD notifications) are their own services or listeners, composed by DI, not copied.
- `[H]` **SHOULD** Long-running work (bulk dues generation, imports, notifications to many users) goes to queued jobs.

## Design patterns

| Pattern | Where | Level |
|---|---|---|
| Service layer | `app/Services/*Service.php` | `[H]` MUST |
| Policies + Gates per entity, permission names `{entity}.{action}` | `app/Policies`, `ActionPermissions` | `[H]` MUST |
| Form objects / Form Requests for validation | Livewire Forms, `app/Http/Requests` | `[+]` SHOULD |
| Enums for statuses and types (TitleCase keys) | `app/Enums` | `[H]` SHOULD |
| Traits/Concerns for shared model behaviour (`EnforcesSoftDelete`, `MaintainsAuditChain`, `ThrottlesSubmissions`) | `app/Models/Concerns`, `app/Support` | `[H]` SHOULD |
| Observers / Events + queued Listeners for side effects | `app/Observers`, `app/Listeners` | `[H]` SHOULD |
| Reusable Blade components for repeated UI (flash message, hero, action buttons, sort chip) | `resources/views/components` | `[H]` MUST |
| DTOs (readonly classes) when a service needs more than 3–4 loose arguments | `app/Data` | `[+]` SHOULD |
| Strategy/driver interfaces for swappable providers (payment, AI provider via Prism) | `app/Contracts` + bindings | `[+]` SHOULD |

## Principles

- `[+]` **SHOULD** SOLID, especially single responsibility and dependency inversion: depend on interfaces where a second implementation is realistic.
- `[+]` **SHOULD** Don't add a repository layer on top of services; Eloquent already is one. Match the altitude of the existing code.
- `[H]` **MUST** Reuse existing components, services and helpers before creating new ones; mirror the nearest well-factored sibling file.
- `[H]` **MUST** No new top-level folders and no dependency changes without approval.
