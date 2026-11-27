[Rules index](../README.md) › Security

**Navigation:** Previous: [Translations](../i18n/translations.md) · Next: [Testing](../testing/testing.md) · [Table of contents](../README.md#table-of-contents)

# Security

Every public entry point is rate-limited, every action is authorized, and money is never hard-deleted.

These rules assume the usual threats: bots hammering a form, a user reading someone else's record by changing an ID in the URL, an accidental delete of a payment, and a secret committed to git. Each rule below closes one of them.

---

## Rate limiting

- `[H]` **MUST** Every public (front-office) form and endpoint is rate-limited: contact, demo request, newsletter, quote request, search, login, password reset, verification links, API authentication, payment webhooks.
  - **Benefit:** Without a limit, a bot can submit a contact form ten thousand times, flood the inbox, send password-reset emails to a victim, or brute-force a login. A limit makes each of these slow and expensive for the attacker.

- `[H]` **MUST** Limits are named and declared in one place, then applied by name to each route or form. A form that cannot use the standard mechanism counts every attempt, valid or not, and returns a translated validation error rather than a bare error page.
  - **Benefit:** A named limit is one definition used in many places, so limits are easy to find and change. Counting every attempt, including valid ones, matters: a limit that only counts failures lets a bot use valid input to test volume. The translated error means a limited user sees a helpful message.
  - **Example:**
    ```text
    declare limit "contact": 10 requests per minute, keyed by "contact" + client address
    apply limit "contact" to: POST /contact
    ```

- `[H]` **MUST** Limits are configurable (from configuration or environment, not hard-coded), keyed by form and client address, and by email where relevant. Reference values: login 6 per minute, API 60 per minute, webhooks 60 per minute, public forms 10 per minute.
  - **Benefit:** Configurable limits can be raised for a real traffic spike or lowered after an attack without a code release. Keying by form and address means one busy form does not lock out every other form for the same visitor. Adding the email to login limits protects a single account from being guessed even when the attacker rotates addresses.
  - **Deviate when:** The traffic comes from a trusted internal network. Document the exemption and keep it in configuration.

- `[H]` **SHOULD** Public forms add a honeypot field: a field hidden from people (for example, a `website` field hidden with CSS) that bots fill in. Any submission with it filled is discarded. AI assistant endpoints have per-user limits and an audit log.
  - **Benefit:** A honeypot blocks many bots without bothering a real user. Per-user limits on AI endpoints control cost, since each call bills tokens, and the audit log shows who used it.

---

## Authorization and data protection

- `[H]` **MUST** Every create, read, update and delete goes through an authorization rule on the server, with permission names of the form `{entity}.{action}` (for example `expenses.create`, `payments.refund`). Hide controls with the same check in the UI, and check again on the server.
  - **Benefit:** Hiding a button is cosmetic; anyone can still send the request. The server check is what stops a user from editing another building's invoice. Permission names of this form are searchable, listable in one admin screen, and easy to assign to roles.
  - **Example:**
    ```text
    rule "payments.refund" for payment:
        allow if user has permission "payments.refund"
              and user.tenant == payment.tenant

    handler "refund payment":
        authorize "payments.refund" on payment      # server check, always
    ```

- `[H]` **MUST** Users see only their own tenant, building or space. Every query is scoped to the current tenant at one point (a shared query scope or the service), and role areas (platform admin, management, resident) are separated, so an admin's screens are not reachable by a resident even by guessing URLs.
  - **Benefit:** In a multi-tenant application, one missed filter on the tenant shows one client's data to another. Scoping at one point makes that mistake hard to make.

- `[H]` **MUST** Financial records (payments, expenses, incomes, budgets, salaries, invoices) use soft delete only: the row is marked as deleted, never removed. A permanent delete is forbidden for them. Prefer soft delete on every model.
  - **Benefit:** A deleted payment is usually a mistake or a dispute, and it must still be explainable to an auditor. A soft delete keeps the row, so totals, history and the audit trail stay consistent. A hard delete is permanent and cannot be undone from the application.
  - **Example:**
    ```text
    table payments:
        ...
        deleted_at  timestamp, nullable      -- set on delete; rows are never removed
    default queries: exclude rows where deleted_at is set
    ```
  - **Deviate when:** Never for financial records. For other data, a permanent delete is acceptable if the reason is stated, for example a legal erasure request under GDPR.

- `[H]` **MUST** Changes to important records are logged (who, what, and old → new values) in an audit log, so the trail stays complete.
  - **Benefit:** When a balance is disputed, the log answers "who changed this, when, and from what value". Without it, the answer is guesswork. Logging old and new values is what makes the log useful for reconciling money.
  - **Example:** Record the actor, the entity, the changed fields with their previous and new values, and the time. Use an audit library for your stack (see [Stack mapping](../stacks/README.md)).

- `[H]` **SHOULD** Consent tracking and personal-data export exist wherever personal data is stored (GDPR and similar laws).
  - **Benefit:** Under GDPR, a person can ask what data is held about them and can withdraw consent. Having consent recorded and an export ready turns a stressful request into a routine one.

- `[+]` **MUST** Validate all input on the server, even if the browser validated it too. Accept only the fields you list explicitly (an allow-list), never the whole request body. Escape output by default, and sanitise any HTML you must render unescaped.
  - **Benefit:** Client-side validation is for the user's convenience and is trivially bypassed. Accepting the whole request body lets a user set `is_admin` or `tenant_id` by adding a field to the form. Escaped output blocks most cross-site scripting; unescaped output disables that protection, so it needs a sanitiser first.
  - **Example:**
    ```text
    data = validate request against:
        title: required, text, at most 120 characters
    save announcement with data           # only the validated fields reach storage
    ```

- `[+]` **MUST** Keep CSRF protection on, including across multi-step logins. No secrets in code or seed data, and never commit files that hold environment secrets.
  - **Benefit:** CSRF protection stops another site from submitting a form as a logged-in user. A secret in code or a seed file stays in version history forever and can be read by everyone with repository access. An expired token during a long login makes the user lose their place; keeping it valid avoids that.
  - **Deviate when:** A machine-to-machine webhook cannot send a CSRF token. Exclude only that route, and verify its signature instead.

- `[+]` **SHOULD** Set security headers (Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, Referrer-Policy) and use signed, expiring URLs for one-off links. Follow the OWASP Top 10.
  - **Benefit:** Headers are a cheap second line of defence: CSP limits what a script can do, HSTS forces HTTPS, `X-Content-Type-Options` stops a browser from guessing a file's type, and `Referrer-Policy` limits what URLs leak to other sites. A signed, expiring link for a password-setup email cannot be guessed or reused after it expires. The OWASP Top 10 is the checklist auditors and reviewers use, so it gives a shared vocabulary for security decisions.

---

**Related:** [Routes and screens](../frontend/routes-and-screens.md) (authorization on route groups) · [Views and components](../frontend/views-and-components.md) (CSP and no inline scripts) · [Testing](../testing/testing.md) (authorization tests) · [Stack mapping](../stacks/README.md) · [Summary](../SUMMARY.md)
