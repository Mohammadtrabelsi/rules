# Git workflow and delivery

All work lands on `develop` through a pull request; `main` only receives releases.

- `[H]` **MUST** Branch from `develop` (`feature/`, `bugfix/`, `refactor/`, `docs/`, `chore/`) and open the PR against `develop`, never `main`.
- `[H]` **MUST** Conventional commit messages: `type(scope): subject` (`feat`, `fix`, `refactor`, `docs`, `chore`, `test`).
- `[H]` **MUST** No force-push to `develop` or `main`; no direct pushes to `main`.
- `[H]` **SHOULD** One concern per PR; merge `develop` into the branch and resolve conflicts before review, keeping `develop`'s side unless asked otherwise.
- `[H]` **SHOULD** PR descriptions list what changed, migrations to run, build steps (`npm run build`) and what was and wasn't tested, and stay accurate.
- `[+]` **SHOULD** Keep PRs reviewable (roughly under 400 changed lines where possible).
