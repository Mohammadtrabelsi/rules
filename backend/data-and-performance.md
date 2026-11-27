[Rules index](../README.md) › Backend › Data and performance

**Navigation:** Previous: [Routes and screens](../frontend/routes-and-screens.md) · Next: [Translations](../i18n/translations.md) · [Table of contents](../README.md#table-of-contents)

# Data and performance

Schema changes go through versioned migrations, queries are indexed and loaded in batches, and heavy work runs in the background. (Service layer rules: see [Layering and patterns](../architecture/layering-and-patterns.md).)

---

## Schema and money

- `[H]` **MUST** Every schema or data change is a versioned migration, including one-off data fixes such as repricing. Never edit a shared database by hand. Name the migration step in the hand-off.
  - **Benefit:** A migration is code, so it is reviewed, versioned and run the same way on every machine, staging and production. A hand-edited database exists only on one machine and cannot be reproduced. A data fix written as a migration also runs exactly once on each environment and leaves a record.
  - **Example:**
    ```text
    migration "reprice legacy plans":
        up:   UPDATE plans SET price_minor = 4900 WHERE code = 'legacy';
    ```
  - **Deviate when:** Never. If a fix seems too small for a migration, it is still a change to data that someone must be able to trace.

- `[H]` **MUST** Size every column for the real data it will hold, with room to spare. Store money as an integer count of minor units (cents) or as a fixed-point decimal, never as a floating-point number.
  - **Benefit:** A 20-character column that receives 24-character references fails in production, not in development, because the database rejects or truncates the value. Floating-point numbers cannot represent `0.1 + 0.2` exactly, so totals drift by a cent across many rows. Integer minor units add and compare exactly.
  - **Example:**
    ```text
    amount_minor      integer   -- 12345 = €123.45
    exchange_rate     decimal(12, 6)   -- rates need fractions; decimal, not float
    ```
  - **Deviate when:** Never store money as a float. Use a decimal type when the fraction is a rate, not an amount.

---

## Indexes and seeders

- `[H]` **SHOULD** Index foreign keys and every column used in filters, sorting or status checks.
  - **Benefit:** Without an index, a filter on a table with a million rows scans every row. Foreign keys are also used in joins and deletes, so indexing them prevents slow lock behaviour and makes related lookups fast.
  - **Example:** an index on `building_id`, and a composite index on `(status, due_date)` for a dashboard query that filters on both.

- `[H]` **SHOULD** Seeders come in tiers (minimal, demo, full). They seed realistic data for every tenant and every supported locale.
  - **Benefit:** A minimal seeder runs in production or CI in seconds. A demo seeder shows the product to a client. A full seeder exercises pages with realistic volume, which is when performance problems appear. Seeding every locale and tenant catches translation and scoping bugs that a single-language seed hides.

---

## Queues and performance

- `[H]` **SHOULD** Queue long-running work, and send notifications from queued listeners.
  - **Benefit:** See the same benefit in [Layering and patterns](../architecture/layering-and-patterns.md#queues). A queued listener also lets a failing email retry without rolling back the payment that triggered it.

- `[+]` **MUST** No N+1 queries. Load each related set in one query or in a batch (eager loading, joins, or the ORM's include option), and make accidental lazy loading fail loudly outside production.
  - **Benefit:** An N+1 query runs one query per row. A list of 25 invoices, each needing one lookup, makes 26 queries; at 1,000 rows it is 1,001. Turning accidental lazy loads into errors in development and tests catches the bug before a user sees a slow page.
  - **Example:**
    ```text
    Bad:   invoices = list 25 invoices
           for each invoice: print invoice.building.name            -> 26 queries

    Good:  invoices = list 25 invoices, including their building
           print each invoice.building.name                         -> 2 queries
    ```
  - **Setup:** Enable the ORM's strict-loading or N+1 detector in development and tests. Examples per stack are in [Stack mapping](../stacks/README.md#examples-in-one-stack).

- `[+]` **SHOULD** Cache expensive read-only aggregates (dashboards, configuration) and invalidate them on write. Read settings once per request.
  - **Benefit:** A dashboard that sums thousands of rows on every page view is the slowest page in the app. Caching it for a short time serves most views from memory. Invalidating on write keeps the numbers correct after a change.
  - **Deviate when:** The number must be exact at every moment, such as a bank balance shown before a payment. Do not cache it.

- `[+]` **SHOULD** Wrap multi-step writes in a database transaction inside the service.
  - **Benefit:** If a payment is recorded but the invoice status update fails, the database is left half-changed and the books no longer match. A transaction makes the steps succeed or fail together.
  - **Example:**
    ```text
    function recordPayment(invoice, amount_minor):
        within a transaction:
            payment = create payment for invoice with amount_minor
            set invoice.status = "paid"
            return payment
    ```

---

**Related:** [Layering and patterns](../architecture/layering-and-patterns.md) · [Security](../security/security.md) (soft deletes on financial data) · [Testing](../testing/testing.md) · [Stack mapping](../stacks/README.md) · [Summary](../SUMMARY.md)
