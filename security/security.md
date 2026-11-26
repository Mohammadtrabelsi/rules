[Rules index](../README.md) › Security

**Navigation:** Previous: [Translations](../i18n/translations.md) · Next: [Testing](../testing/testing.md) · [Table of contents](../README.md#table-of-contents)

# Security

Every public entry point is rate-limited, every action is authorized, and money is never hard-deleted.

These rules assume the usual threats: bots hammering a form, a user reading someone else's record by changing an ID in the URL, an accidental delete of a payment, and a secret committed to git. Each rule below closes one of them.

---

## Rate limiting

- `[H]` **MUST** Every public (front-office) form and endpoint is rate-limited: contact, demo request, newsletter, quote request, search, login, password reset, verification links, API auth, payment webhooks.
  - **Benefit:** Without a limit, a bot can submit a contact form ten thousand times, flood the inbox, send password-reset emails to a victim, or brute-force a login. A limit makes each of these slow and expensive for the attacker.

- `[H]` **MUST** Named limiters are declared with `RateLimiter::for()` in a service provider and applied with `throttle:<name>` middleware; Livewire forms use a shared trait (IMEXCO's `ThrottlesSubmissions`) that counts every attempt, valid or not, and returns a translated validation error.
  - **Benefit:** A named limiter is one definition used in many places, so limits are easy to find and change. Counting every attempt, including valid ones, matters: a limiter that only counts failures lets a bot use valid input to test volume. The translated error means a limited user sees a helpful message, not a 429 page.
  - **Example:**
    ```php
    // app/Providers/AppServiceProvider.php
    RateLimiter::for('contact', function (Request $request): Limit {
        return Limit::perMinute(config('site.form_throttle.contact', 10))
            ->by('contact|'.$request->ip());
    });

    // routes/web.php
    Route::post('contact', ContactController::class)->middleware('throttle:contact');
    ```

- `[H]` **MUST** Limits are configurable (e.g. `config/site.php` → `form_throttle.<form>`), keyed by form + IP (+ email where relevant). Reference values: auth 6/min, API 60/min, webhooks 60/min, public forms 10/min.
  - **Benefit:** Configurable limits can be raised for a real traffic spike or lowered after an attack without a code release. Keying by form and IP means one busy form does not lock out every other form for the same visitor. Adding the email to login limits protects a single account from being guessed even when the attacker rotates IPs.
  - **Deviate when:** The traffic is from a trusted internal network. Document the exemption and keep it in config.

- `[H]` **SHOULD** Public forms add a honeypot field; AI assistant endpoints have per-user limits and an audit log.
  - **Benefit:** A honeypot is a field hidden from people (for example, a `website` field hidden with CSS) that bots fill in. Any submission with it filled is discarded, which blocks many bots without bothering a real user. Per-user limits on AI endpoints control cost, since each call bills tokens, and the audit log shows who used it.

---

## Authorization and data protection

- `[H]` **MUST** Every Create/Read/Update/Delete goes through a Policy; permissions follow `{entity}.{action}` (`expenses.create`, `payments.refund`). Hide buttons with `@can`, and authorize again on the server.
  - **Benefit:** Hiding a button is cosmetic; anyone can still send the request. The server check is what stops a user from editing another building's invoice. Permission names in the form `{entity}.{action}` are searchable, listable in one admin screen, and easy to assign to roles.
  - **Example:**
    ```php
    final class PaymentPolicy
    {
        public function refund(User $user, Payment $payment): bool
        {
            return $user->can('payments.refund') && $user->tenant_id === $payment->tenant_id;
        }
    }

    // Livewire component
    $this->authorize('refund', $this->payment);
    ```

- `[H]` **MUST** Users see only their own tenant/building/space; role areas (platform admin, syndic, resident) are separated, with a space chooser at login.
  - **Benefit:** In a multi-tenant app, one missed `where('tenant_id', …)` shows one client's data to another. Scoping every query to the current tenant at one point (a global scope or the service) makes that mistake hard to make. Separating role areas means an admin's screens are not reachable by a resident, even by guessing URLs.

- `[H]` **MUST** Financial records (payments, expenses, incomes, budgets, salaries, invoices) use soft deletes only; `forceDelete` is forbidden. Prefer soft deletes on every model.
  - **Benefit:** A deleted payment is usually a mistake or a dispute, and it must still be explainable to an auditor. A soft delete keeps the row, so totals, history and the audit trail stay consistent. A hard delete is permanent and cannot be undone from the application.
  - **Example:**
    ```php
    final class Payment extends Model
    {
        use SoftDeletes;
    }
    ```
  - **Deviate when:** Never for financial records. For non-financial data, a permanent delete is acceptable if the reason is stated, for example a legal erasure request under GDPR.

- `[H]` **MUST** Changes are logged with `spatie/laravel-activitylog` (who, what, old → new) so the audit trail stays complete.
  - **Benefit:** When a balance is disputed, the log answers "who changed this, when, and from what value". Without it, the answer is guesswork. Logging old and new values is what makes the log useful for reconciling money.
  - **Example:** Add `use LogsActivity;` to the model and configure `getActivitylogOptions()` with `logOnly()` for the fields that matter.

- `[H]` **SHOULD** Consent tracking and personal-data export exist where personal data is stored (GDPR).
  - **Benefit:** Under GDPR, a person can ask what data is held about them and can withdraw consent. Having consent recorded and an export ready turns a stressful request into a routine one, and it avoids a breach of the regulation.

- `[+]` **MUST** Validate all input server-side; mass assignment only through `$fillable` or validated arrays; escape output with `{{ }}`, sanitise any HTML you must render with `{!! !!}`.
  - **Benefit:** Client-side validation is for the user's convenience and is trivially bypassed. Mass assignment without `$fillable` lets a user set `is_admin` or `tenant_id` by adding a field to the form. Blade's `{{ }}` escapes HTML, which blocks most cross-site scripting; `{!! !!}` disables that protection, so it needs a sanitiser first.
  - **Example:**
    ```php
    // Good: only validated keys reach the model
    $data = $request->validate(['title' => ['required', 'string', 'max:120']]);
    Announcement::create($data);
    ```

- `[+]` **MUST** Keep CSRF on (and keep the token valid across multi-step logins); no secrets in code or seeders; `.env` never committed.
  - **Benefit:** CSRF protection stops another site from submitting a form as a logged-in user. A secret in code or a seeder is in git history forever and can be read by everyone with repository access. An expired CSRF token on a long login makes the user lose their place; keeping it valid avoids that.
  - **Deviate when:** A machine-to-machine webhook cannot send a CSRF token. Exclude only that route, and verify its signature instead.

- `[+]` **SHOULD** Security headers (CSP, HSTS, X-Content-Type-Options, Referrer-Policy) and signed URLs for one-off links; follow the OWASP Top 10.
  - **Benefit:** Headers are a cheap second line of defence: CSP limits what a script can do, HSTS forces HTTPS, `X-Content-Type-Options` stops a browser from guessing a file's type, and `Referrer-Policy` limits what URLs leak to other sites. A signed URL (`URL::temporarySignedRoute()`) for a one-off link such as a password-setup email cannot be guessed or reused after it expires. The OWASP Top 10 is the checklist auditors and reviewers use, so following it gives a shared vocabulary for security decisions.

---

**Related:** [Routes and screens](../frontend/routes-and-screens.md) (middleware on route groups) · [Views and components](../frontend/views-and-components.md) (CSP and no inline scripts) · [Testing](../testing/testing.md) (authorization tests) · [Summary](../SUMMARY.md)
