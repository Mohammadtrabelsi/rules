# Security

Every public entry point is rate-limited, every action is authorized, and money is never hard-deleted.

## Rate limiting

- `[H]` **MUST** Every public (front-office) form and endpoint is rate-limited: contact, demo request, newsletter, quote request, search, login, password reset, verification links, API auth, payment webhooks.
- `[H]` **MUST** Named limiters are declared with `RateLimiter::for()` in a service provider and applied with `throttle:<name>` middleware; Livewire forms use a shared trait (IMEXCO's `ThrottlesSubmissions`) that counts every attempt, valid or not, and returns a translated validation error.
- `[H]` **MUST** Limits are configurable (e.g. `config/site.php` → `form_throttle.<form>`), keyed by form + IP (+ email where relevant). Reference values: auth 6/min, API 60/min, webhooks 60/min, public forms 10/min.
- `[H]` **SHOULD** Public forms add a honeypot field; AI assistant endpoints have per-user limits and an audit log.

## Authorization and data protection

- `[H]` **MUST** Every Create/Read/Update/Delete goes through a Policy; permissions follow `{entity}.{action}` (`expenses.create`, `payments.refund`). Hide buttons with `@can`, and authorize again on the server.
- `[H]` **MUST** Users see only their own tenant/building/space; role areas (platform admin, syndic, resident) are separated, with a space chooser at login.
- `[H]` **MUST** Financial records (payments, expenses, incomes, budgets, salaries, invoices) use soft deletes only; `forceDelete` is forbidden. Prefer soft deletes on every model.
- `[H]` **MUST** Changes are logged with `spatie/laravel-activitylog` (who, what, old → new) so the audit trail stays complete.
- `[H]` **SHOULD** Consent tracking and personal-data export exist where personal data is stored (GDPR).
- `[+]` **MUST** Validate all input server-side; mass assignment only through `$fillable` or validated arrays; escape output with `{{ }}`, sanitise any HTML you must render with `{!! !!}`.
- `[+]` **MUST** Keep CSRF on (and keep the token valid across multi-step logins); no secrets in code or seeders; `.env` never committed.
- `[+]` **SHOULD** Security headers (CSP, HSTS, X-Content-Type-Options, Referrer-Policy) and signed URLs for one-off links; follow the OWASP Top 10.
