# Translations and i18n

No user-facing string is ever hard-coded; every string is a key in a per-feature language file, present in every locale.

- `[H]` **MUST** Every visible string (labels, buttons, menus, flash messages, validation and email text, seeder content shown to users) goes through `__()` / `trans_choice()`.
- `[H]` **MUST** Keys are grouped into one bundle per feature or screen: `lang/{locale}/{feature}.php` (`billing.php`, `faq.php`, `nav.php`), nested by dots (`settings.admin.fields.temperature`). No catch-all file for new keys, no JSON string-as-key files for new work.
- `[H]` **MUST** Every key exists in every supported locale: en, fr, ar on ResiCore and IMEXCO; en, fr, ar, de, es on OrganiCore. Run `php artisan translations:sync` (the `laravel-translation-sync` package) after adding keys, then fill every `[TODO]`.
- `[H]` **SHOULD** Add a test that fails on missing translations for new menu entries and pages.
- `[H]` **SHOULD** Translatable database content (CMS pages, FAQ, plans) is stored per locale (e.g. `spatie/laravel-translatable`) and seeded in all languages, Arabic included.
- `[H]` **SHOULD** The chosen locale persists through login and is switchable from the top bar in both the public site and admin.
- `[+]` **MUST** Arabic renders right-to-left: `dir` and `lang` set on `<html>`, logical CSS properties (`ms-` / `me-`, `start` / `end`) instead of `left` / `right`.
- `[+]` **SHOULD** Use placeholders (`:name`) and pluralisation instead of concatenating strings; format dates, numbers and currency with the locale.
