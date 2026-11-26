[Rules index](../README.md) › Testing

**Navigation:** Previous: [Security](../security/security.md) · Next: [Git workflow](../git/workflow.md) · [Table of contents](../README.md#table-of-contents)

# Testing

A test is the only proof that a behaviour works and keeps working. These rules make sure the proof exists for every change and that nobody quietly removes it.

---

## What to test

- `[H]` **MUST** Pest tests (feature tests by default, factories over manual setup) for every behaviour or logic change, covering failure paths and authorization. Skip tests for pure copy or styling changes.
  - **Benefit:** A feature test runs the real request through routes, middleware, policies and the database, so it catches wiring mistakes that unit tests miss. Covering failure paths (invalid input, missing permission, a locked record) is where most real bugs live. Factories build realistic data in one line and stay correct as the schema changes.
  - **Example:**
    ```php
    it('forbids a resident from refunding a payment', function (): void {
        $resident = User::factory()->resident()->create();
        $payment = Payment::factory()->create();

        $this->actingAs($resident)
            ->post(route('payments.refund', $payment))
            ->assertForbidden();

        expect($payment->fresh()->isRefunded())->toBeFalse();
    });
    ```
  - **Deviate when:** The change is pure copy or CSS with no logic. A test for a colour is noise; check it in the browser instead.

- `[H]` **SHOULD** Add a test that fails on missing translations for new menu entries and pages (see [`../i18n/translations.md`](../i18n/translations.md)).
  - **Benefit:** An automated check finds untranslated keys on every run, in every locale, without anyone remembering to look. It replaces a manual review that would be skipped under deadline.

---

## Integrity of the suite

- `[H]` **MUST** Never delete or skip a test to get green; fix the code or update an out-of-date expectation and say so.
  - **Benefit:** A test that was skipped to make a build pass hides the failure it was written to catch. Deleting it removes the warning. If the expectation is genuinely out of date, updating it with a note keeps the record honest about why the behaviour changed.
  - **Deviate when:** The test covers a feature being removed in the same change. Delete it together with the feature, and say so in the hand-off.

- `[H]` **MUST** Run the narrowest relevant tests before handing back, and state exactly which ran and which could not run and why.
  - **Benefit:** Running the full suite on every small change is slow; running only the test you wrote can miss a neighbour that broke. The narrowest relevant set (the changed feature and its direct callers) gives fast feedback, and stating what ran lets the reviewer decide whether more is needed.
  - **Example:** `vendor/bin/pest --filter=PaymentRefund` and `vendor/bin/pest tests/Feature/Payments`.

- `[H]` **SHOULD** Test runs write JUnit and TestDox reports to `storage/test-reports/`; CI uploads them.
  - **Benefit:** JUnit is read by CI dashboards and lets failures show per test. TestDox writes the test names as sentences, so a reviewer can read what the suite promises without reading the code.
  - **Example:** `vendor/bin/pest --log-junit storage/test-reports/junit.xml`

---

## Self-check before finishing

Run these before handing back a change. Each line checks one rule from the category pages. Every command that says "must be empty" should return no output.

```bash
grep -rn '@php' resources/views                                   # must be empty
grep -rn '<script' resources/views                                # must be empty
grep -rn '<style' resources/views --exclude-dir=pdf               # must be empty
grep -rnE '\son(click|change|submit|input|keydown)=' resources/views  # must be empty
grep -rn '<table' resources/views --exclude-dir=pdf               # lists must use cards
grep -rnE '::(where|find|create|all|first)\(|DB::' app/Livewire app/Http/Controllers  # must be empty
php artisan translations:sync --dry-run                           # no missing keys
```

| Check | Rule it enforces | Why the check is worth running |
|---|---|---|
| `@php` in views | [No logic in Blade](../frontend/views-and-components.md#no-logic-in-blade) | Logic in templates is untested and repeated |
| `<script` in views | [No inline scripts](../frontend/views-and-components.md#no-inline-scripts-or-handlers) | Keeps a strict Content-Security-Policy possible |
| `<style` in views | [No inline styles](../frontend/views-and-components.md#no-inline-styles) | Styles stay in one place and survive themes |
| `on…=` handlers | [No inline scripts](../frontend/views-and-components.md#no-inline-scripts-or-handlers) | Native handlers miss Livewire re-renders |
| `<table` in views | [Cards instead of tables](../frontend/views-and-components.md#cards-instead-of-tables) | Tables overflow on phones |
| Queries in Livewire or controllers | [No queries in controllers or Livewire](../architecture/layering-and-patterns.md#no-queries-in-controllers-or-livewire) | Business rules stay in services |
| Missing translation keys | [Locale coverage](../i18n/translations.md#locale-coverage) | Users otherwise see raw keys |

A grep is a fast first pass, not a proof. A match can be a false positive (a `<table` inside a PDF template, which the `--exclude-dir=pdf` flag handles). Read each match before you decide.

---

**Related:** [Code quality](../general/code-quality.md) (Pint and PHPStan, the other checks before hand-off) · [Git workflow](../git/workflow.md) · [Summary](../SUMMARY.md)
