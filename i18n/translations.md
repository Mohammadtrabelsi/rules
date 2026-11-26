[Rules index](../README.md) › Translations and i18n

**Navigation:** Previous: [Data and performance](../backend/data-and-performance.md) · Next: [Security](../security/security.md) · [Table of contents](../README.md#table-of-contents)

# Translations and i18n

No user-facing string is ever hard-coded; every string is a key in a per-feature language file, present in every locale.

The goal is that switching language never leaves a user with a missing label, a French sentence in an Arabic screen, or a layout that breaks in a right-to-left script.

---

## Keys and bundles

- `[H]` **MUST** Every visible string (labels, buttons, menus, flash messages, validation and email text, seeder content shown to users) goes through `__()` / `trans_choice()`.
  - **Benefit:** A string hard-coded in one view is untranslated the moment a second language is added, and the English text stays visible to other users. Routing every string through `__()` makes the translation list complete by construction.
  - **Example:**
    ```blade
    {{-- Bad --}}  <button>Save changes</button>
    {{-- Good --}}  <button>{{ __('billing.actions.save') }}</button>
    ```

- `[H]` **MUST** Keys are grouped into one bundle per feature or screen: `lang/{locale}/{feature}.php` (`billing.php`, `faq.php`, `nav.php`), nested by dots (`settings.admin.fields.temperature`). No catch-all file for new keys, no JSON string-as-key files for new work.
  - **Benefit:** A translator working on billing opens one file, not a 5,000-line catch-all. Changes to one feature do not conflict with changes to another in version control. Dotted keys are readable in code and in the translation tool.
  - **Example:**
    ```php
    // lang/en/billing.php
    return [
        'actions' => ['save' => 'Save changes'],
        'fields'  => ['iban' => 'IBAN'],
    ];
    ```

- `[+]` **SHOULD** Use placeholders (`:name`) and pluralisation instead of concatenating strings; format dates, numbers and currency with the locale.
  - **Benefit:** Word order differs between languages, so `"Invoice " . $number . " is overdue"` cannot be translated correctly. A placeholder lets the translator place the number where it belongs. Pluralisation handles the "1 invoice / 2 invoices" forms that differ across languages (Arabic has several plural forms).
  - **Example:**
    ```php
    // lang/en/billing.php
    'overdue' => ':number invoice is overdue|:number invoices are overdue',

    // in the view
    {{ trans_choice('billing.overdue', $count, ['number' => $count]) }}
    ```
  - **Formatting:** `number_format()` and fixed date formats show the same value differently across locales. Format dates with Carbon's `isoFormat()` (after `Carbon::setLocale()` for the request) and money and numbers with `NumberFormatter`, so `1 234,50` and `1,234.50` each appear where they belong.

---

## Locale coverage

- `[H]` **MUST** Every key exists in every supported locale: en, fr, ar on ResiCore and IMEXCO; en, fr, ar, de, es on OrganiCore. Run `php artisan translations:sync` (the `laravel-translation-sync` package) after adding keys, then fill every `[TODO]`.
  - **Benefit:** A missing key in Arabic shows the raw key name (`billing.actions.save`) to the user, which looks broken. The sync command adds the key to every locale with a `[TODO]` marker, so nothing is missed and the reviewer can see what still needs a translation.
  - **Deviate when:** A locale is not supported by the project. Do not add it to only some screens.

- `[H]` **SHOULD** Add a test that fails on missing translations for new menu entries and pages.
  - **Benefit:** A test catches a missing translation before merge. Without it, the gap is found by a user, often in a locale the developer never switches to. See [Testing](../testing/testing.md).

- `[H]` **SHOULD** Translatable database content (CMS pages, FAQ, plans) is stored per locale (e.g. `spatie/laravel-translatable`) and seeded in all languages, Arabic included.
  - **Benefit:** Content that lives in the database (a plan name, a FAQ answer) is not in the language files, so it needs its own per-locale storage. Seeding every language means the Arabic site has real content, not an empty page or an English fallback.

- `[H]` **SHOULD** The chosen locale persists through login and is switchable from the top bar in both the public site and admin.
  - **Benefit:** A user who chose Arabic should not be switched back to English after logging in. A switcher in the top bar lets them change language without hunting for a settings page.

---

## Right-to-left (Arabic)

- `[+]` **MUST** Arabic renders right-to-left: `dir` and `lang` set on `<html>`, logical CSS properties (`ms-` / `me-`, `start` / `end`) instead of `left` / `right`.
  - **Benefit:** A layout written with `left` and `right` puts icons and margins on the wrong side in Arabic, and the reading order breaks. Logical properties flip automatically when `dir="rtl"` is set, so one stylesheet serves both directions.
  - **Example:**
    ```blade
    <html lang="{{ str_replace('_', '-', app()->getLocale()) }}" dir="{{ app()->getLocale() === 'ar' ? 'rtl' : 'ltr' }}">
    ```
    ```html
    <!-- Bad -->  <div class="ml-4 text-left">
    <!-- Good --> <div class="ms-4 text-start">
    ```

---

**Related:** [Views and components](../frontend/views-and-components.md) (RTL inside WCAG and the design system) · [Testing](../testing/testing.md) (the missing-translation test) · [Summary](../SUMMARY.md)
