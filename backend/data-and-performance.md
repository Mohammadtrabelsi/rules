[Rules index](../README.md) › Backend › Data and performance

**Navigation:** Previous: [Routes and screens](../frontend/routes-and-screens.md) · Next: [Translations](../i18n/translations.md) · [Table of contents](../README.md#table-of-contents)

# Data and performance

Schema changes go through migrations, queries are indexed and eager-loaded, and heavy work runs in the queue. (Service layer rules: see [`../architecture/layering-and-patterns.md`](../architecture/layering-and-patterns.md).)

---

## Schema and money

- `[H]` **MUST** Every schema or data change is a migration (including one-off data fixes such as repricing); never edit the database by hand. Mention `php artisan migrate` in the hand-off.
  - **Benefit:** A migration is code, so it is reviewed, versioned and run the same way on every machine, staging and production. A hand-edited database exists only on one machine and cannot be reproduced. A data fix written as a migration also runs exactly once on each environment and leaves a record.
  - **Example:**
    ```php
    // database/migrations/2026_11_01_000000_reprice_legacy_plans.php
    public function up(): void
    {
        DB::table('plans')->where('code', 'legacy')->update(['price_minor' => 4900]);
    }
    ```
  - **Deviate when:** Never. If a fix seems too small for a migration, it is still a change to the data that someone must be able to trace.

- `[H]` **MUST** Size columns for real data (the quote reference overflow); money as integer minor units or `decimal`, never float.
  - **Benefit:** A `varchar(20)` for a reference that sometimes reaches 24 characters fails in production, not in development, because the database rejects or truncates it. Floats cannot represent `0.1 + 0.2` exactly, so totals drift by a cent across many rows. Integer minor units (cents) add and compare exactly.
  - **Example:**
    ```php
    $table->unsignedBigInteger('amount_minor');   // 12345 = €123.45
    $table->decimal('exchange_rate', 12, 6);       // rates need fractions; use decimal, not float
    ```
  - **Deviate when:** Never store money as float. Use `decimal` when the fraction is a rate, not an amount.

---

## Indexes and seeders

- `[H]` **SHOULD** Index foreign keys and every column used in `where`, `orderBy` or status filters.
  - **Benefit:** Without an index, a filter on a table with a million rows scans every row. Foreign keys are also used in joins and deletes, so indexing them prevents slow lock behaviour and makes related lookups fast.
  - **Example:** `$table->foreignId('building_id')->constrained()->index();` and `$table->index(['status', 'due_date']);` for a dashboard query that filters on both.

- `[H]` **SHOULD** Seeders come in tiers (minimal / demo / full) and seed realistic data for every building or tenant, in all locales.
  - **Benefit:** A minimal seeder runs in production or CI in seconds. A demo seeder shows the product to a client. A full seeder exercises pages with realistic volume, which is when performance problems appear. Seeding every locale and tenant catches translation and scoping bugs that a single-language seed hides.

---

## Queues and performance

- `[H]` **SHOULD** Queue long-running work; queued listeners for notifications.
  - **Benefit:** See the same benefit in [Layering and patterns](../architecture/layering-and-patterns.md#queues). Queued listeners also let a failing email retry without rolling back the payment that triggered it.

- `[+]` **MUST** No N+1 queries: eager-load relations (`with()`), enable `Model::preventLazyLoading()` outside production.
  - **Benefit:** An N+1 query runs one query per row. A list of 25 invoices with one lookup each makes 26 queries; at 1,000 rows it is 1,001. `preventLazyLoading()` turns every accidental lazy load into an exception in development and tests, so the bug is caught before a user sees a slow page.
  - **Example:**
    ```php
    // Bad: one query per invoice for its building
    $invoices = Invoice::paginate(25);
    foreach ($invoices as $invoice) { echo $invoice->building->name; }

    // Good: two queries in total
    $invoices = Invoice::with('building')->paginate(25);
    ```
  - **Setup:** In `AppServiceProvider::boot()`, call `Model::preventLazyLoading(! app()->isProduction());`.

- `[+]` **SHOULD** Cache expensive read-only aggregates (dashboards, feature flags) and invalidate on write; read settings once per request.
  - **Benefit:** A dashboard that sums thousands of rows on every page view is the slowest page in the app. Caching it for a short time serves most views from memory. Invalidating on write keeps the numbers correct after a change, so the cache does not show stale totals.
  - **Deviate when:** The number must be exact at every moment, such as a bank balance shown before a payment. Do not cache it.

- `[+]` **SHOULD** Wrap multi-step writes in `DB::transaction()` inside the service.
  - **Benefit:** If a payment is recorded but the invoice status update fails, the database is left half-changed and the books no longer match. A transaction makes the steps succeed or fail together.
  - **Example:**
    ```php
    public function recordPayment(Invoice $invoice, int $amountMinor): Payment
    {
        return DB::transaction(function () use ($invoice, $amountMinor): Payment {
            $payment = $invoice->payments()->create(['amount_minor' => $amountMinor]);
            $invoice->update(['status' => InvoiceStatus::Paid]);

            return $payment;
        });
    }
    ```

---

**Related:** [Layering and patterns](../architecture/layering-and-patterns.md) · [Security](../security/security.md) (soft deletes on financial data) · [Testing](../testing/testing.md) · [Summary](../SUMMARY.md)
