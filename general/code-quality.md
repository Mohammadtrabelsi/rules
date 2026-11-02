# Code quality

A change is done only when format, static analysis and the relevant tests pass. (Testing rules: see [`../testing/testing.md`](../testing/testing.md).)

## Style

- `[H]` **MUST** PHP 8.4 style: strict types, explicit return and parameter types, constructor property promotion, curly braces on every control structure, generic PHPDoc for collections (`Collection<int, User>`), `@property` annotations on models and components.
- `[H]` **MUST** Descriptive names (`isRegisteredForDiscounts`, not `discount()`); PHPDoc only where logic is not obvious.
- `[+]` **SHOULD** Small functions, early returns, no dead code, no commented-out code.

## Tooling

- `[H]` **MUST** Run `vendor/bin/pint --dirty` and PHPStan/Larastan (level 5 or the project's level) before committing; fix new errors instead of growing the baseline.

## Hand-off and docs

- `[H]` **MUST** Be honest in the hand-off: say exactly which tests, Pint and PHPStan ran, and which could not run and why. Mention any `php artisan migrate` or `npm run build` needed.
- `[H]` **SHOULD** Don't create documentation files unless asked; when docs exist, keep the generated codebase reference current.
