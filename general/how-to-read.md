# How to read these rules

These rules apply to every Laravel 13 + Livewire project (stack: Laravel 13, Livewire 3/4, Alpine, Tailwind, Pest, PHP 8.4). They beat an agent's or developer's defaults. If a rule conflicts with the task, stop and ask.

Each rule carries a **tag** and a **level**:

| Tag / level | Meaning |
|---|---|
| `[H]` | From history: asked for in past sessions, or already written into one of the repos |
| `[+]` | Added from well-established practice (Laravel docs, OWASP, WCAG, Spatie guidelines) to round out an existing rule |
| **MUST** | Never broken without explicit approval |
| **SHOULD** | Default; deviate only with a stated reason |

## Where the `[H]` rules come from

About 100 Claude Code sessions (Oct 2026), about 220 pull requests on ResiCore and OrganiCore, and the existing rule files in GreenHumanResource (`CLAUDE.md`, the most complete), ResiCore (`CLAUDE.md`, `.ai/entity-management.md`), IMEXCO (`CLAUDE.md`, `ThrottlesSubmissions`), OrganiCore and the `laravel-translation-sync` package.

## Sources

- Repos: GreenHumanResource `CLAUDE.md`, ResiCore `CLAUDE.md` and `.ai/entity-management.md`, IMEXCO `CLAUDE.md` and `app/Support/Livewire/ThrottlesSubmissions.php`, OrganiCore `CLAUDE.md` and `routes/`, `laravel-translation-sync`
- Pull request history on ResiCore (#120–#219) and OrganiCore (#533–#632); Claude Code session titles and summaries, Oct 2026
- Added practice: Laravel rate limiting, OWASP Top 10, OWASP CSP cheat sheet, WCAG 2.2, Spatie Laravel guidelines, Conventional Commits
