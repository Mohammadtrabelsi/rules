# Testing

- `[H]` **MUST** Pest tests (feature tests by default, factories over manual setup) for every behaviour or logic change, covering failure paths and authorization. Skip tests for pure copy or styling changes.
- `[H]` **MUST** Never delete or skip a test to get green; fix the code or update an out-of-date expectation and say so.
- `[H]` **MUST** Run the narrowest relevant tests before handing back, and state exactly which ran and which could not run and why.
- `[H]` **SHOULD** Test runs write JUnit and TestDox reports to `storage/test-reports/`; CI uploads them.
- `[H]` **SHOULD** Add a test that fails on missing translations for new menu entries and pages (see [`../i18n/translations.md`](../i18n/translations.md)).

## Self-check before finishing

```bash
grep -rn '@php' resources/views                                   # must be empty
grep -rn '<script' resources/views                                # must be empty
grep -rn '<style' resources/views --exclude-dir=pdf               # must be empty
grep -rnE '\son(click|change|submit|input|keydown)=' resources/views  # must be empty
grep -rn '<table' resources/views --exclude-dir=pdf               # lists must use cards
grep -rnE '::(where|find|create|all|first)\(|DB::' app/Livewire app/Http/Controllers  # must be empty
php artisan translations:sync --dry-run                           # no missing keys
```
