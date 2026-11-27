[Rules index](../README.md) › Translations and i18n

**Navigation:** Previous: [Data and performance](../backend/data-and-performance.md) · Next: [Security](../security/security.md) · [Table of contents](../README.md#table-of-contents)

# Translations and i18n

No user-facing string is ever hard-coded. Every string is a key in a per-feature translation file, present in every supported locale.

The goal is that switching language never leaves a user with a missing label, a sentence in the wrong language, or a layout that breaks in a right-to-left script.

---

## Keys and bundles

- `[H]` **MUST** Every visible string (labels, buttons, menus, flash messages, validation and email text, seed content shown to users) goes through the translation function.
  - **Benefit:** A string hard-coded in one view is untranslated the moment a second language is added, and the original text stays visible to other users. Routing every string through the translation function makes the translation list complete by construction.
  - **Example:**
    ```text
    Bad:   <button>Save changes</button>
    Good:  <button>{{ t("billing.actions.save") }}</button>
    ```

- `[H]` **MUST** Keys are grouped into one bundle per feature or screen (for example `billing`, `faq`, `nav`), nested by dots (`settings.admin.fields.temperature`). No catch-all file for new keys, and no files that use the English sentence itself as the key, for new work.
  - **Benefit:** A translator working on billing opens one file, not a 5,000-line catch-all. Changes to one feature do not conflict with changes to another in version control. Dotted keys are readable in code and in translation tools.
  - **Example:**
    ```text
    locales/en/billing.yml
        actions:
          save: Save changes
        fields:
          iban: IBAN
    ```

- `[+]` **SHOULD** Use named placeholders and plural forms instead of concatenating strings. Format dates, numbers and currency with the locale.
  - **Benefit:** Word order differs between languages, so `"Invoice " + number + " is overdue"` cannot be translated correctly. A placeholder lets the translator place the number where it belongs. Plural forms handle the "1 invoice / 2 invoices" distinction, and some languages, Arabic among them, have several plural forms.
  - **Example:**
    ```text
    billing.overdue:
        one:   "{count} invoice is overdue"
        other: "{count} invoices are overdue"
    ```
  - **Formatting:** A fixed date format or a hand-written number format shows the same value differently across locales. Use the platform's locale-aware formatter (for example `Intl` in JavaScript, or the equivalent in your stack), so `1 234,50` and `1,234.50` each appear where they belong.

---

## Locale coverage

- `[H]` **MUST** Every key exists in every supported locale. Keep the list of supported locales in one configuration value. After adding keys, run the project's missing-key check (examples per stack in [Stack mapping](../stacks/README.md)), then fill every placeholder marker.
  - **Benefit:** A missing key in Arabic shows the raw key name (`billing.actions.save`) to the user, which looks broken. A sync tool adds the key to every locale with a marker, so nothing is missed and the reviewer can see what still needs a translation.
  - **Deviate when:** A locale is not supported by the project. Do not add it to only some screens.

- `[H]` **SHOULD** Add a test that fails on missing translations for new menu entries and pages.
  - **Benefit:** A test catches a missing translation before merge. Without it, the gap is found by a user, often in a locale the developer never switches to. See [Testing](../testing/testing.md).

- `[H]` **SHOULD** Translatable database content (CMS pages, FAQ entries, plan names) is stored per locale and seeded in all languages, Arabic included.
  - **Benefit:** Content that lives in the database is not in the translation files, so it needs its own per-locale storage. Seeding every language means the Arabic site has real content, not an empty page or an English fallback.

- `[H]` **SHOULD** The chosen locale persists through login and can be switched from the top bar, on both the public site and the admin area.
  - **Benefit:** A user who chose Arabic should not be switched back to English after logging in. A switcher in the top bar lets them change language without hunting for a settings page.

---

## Right-to-left (Arabic)

- `[+]` **MUST** Arabic renders right-to-left: the `dir` and `lang` attributes are set on `<html>`, and layout uses logical properties (start and end, not left and right).
  - **Benefit:** A layout written with `left` and `right` puts icons and margins on the wrong side in Arabic, and the reading order breaks. Logical properties flip automatically when `dir="rtl"` is set, so one stylesheet serves both directions.
  - **Example:**
    ```text
    <html lang="{{ current_locale }}" dir="{{ rtl_if_arabic }}">

    Bad:   margin-left: 1rem; text-align: left
    Good:  margin-inline-start: 1rem; text-align: start
    ```

---

**Related:** [Views and components](../frontend/views-and-components.md) (right-to-left inside WCAG and the design system) · [Testing](../testing/testing.md) (the missing-translation test) · [Stack mapping](../stacks/README.md) · [Summary](../SUMMARY.md)
