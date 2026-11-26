[Rules index](../README.md) › General › How to read these rules

**Navigation:** Previous: — · Next: [Code quality](code-quality.md) · [Table of contents](../README.md#table-of-contents)

# How to read these rules

These rules apply to every Laravel 13 + Livewire project (stack: Laravel 13, Livewire 3/4, Alpine, Tailwind, Pest, PHP 8.4). They beat an agent's or developer's defaults. If a rule conflicts with the task, stop and ask.

This page explains the notation every other page uses, so you can read any rule without looking anything up.

## Anatomy of a rule

Every rule in the category pages has the same shape:

```text
- `[H]` **MUST** <the rule itself>
  - **Benefit:** <why it is worth the cost>
  - **Example:** <a short illustration, where one helps>
  - **Deviate when:** <the narrow situations where breaking it is acceptable>
```

Not every rule needs every field. A rule with no example is a principle; a rule with no exception is one where the answer is always yes.

## Tags and levels

Each rule carries a **tag** and a **level**:

| Tag / level | Meaning | What to do with it |
|---|---|---|
| `[H]` | From history: asked for in past sessions, or already written into one of the repos | Treat as proven. It came from a real problem that happened more than once. |
| `[+]` | Added from well-established practice (Laravel docs, OWASP, WCAG, Spatie guidelines) to round out an existing rule | Treat as the standard default. It fills a gap the history did not cover. |
| **MUST** | Never broken without explicit approval | Stop and ask before breaking it, even if it looks like the quicker path. |
| **SHOULD** | Default; deviate only with a stated reason | Follow it, and write the reason in the pull request if you do not. |

A `[+]` rule with a **MUST** level is a deliberate choice: it is an established practice that the house decided is not optional (for example, server-side validation and CSRF).

## Why the rules exist: the benefit principle

Each rule is written to prevent a specific cost. When you are unsure whether to follow a rule, ask what it protects:

| Cost it prevents | Examples in these rules |
|---|---|
| Money or records going wrong silently | Money as integer minor units, soft deletes on financial records, audit logging |
| Users or data leaking across boundaries | Policies, tenant scoping, rate limiting, no secrets in code |
| Slow pages that only break under real data | No N+1, indexed filter columns, queued long work |
| Work that cannot be reviewed or rolled back | Migrations for every change, one concern per PR, conventional commits |
| Interfaces that exclude people | WCAG 2.2 AA, RTL for Arabic, every string translated |
| A codebase that drifts into several styles | Reuse existing components, one design system, mirror sibling files |
| Hidden failures reported as success | Honest hand-offs, never skipping a test to get green |

## Where the `[H]` rules come from

About 100 Claude Code sessions (Oct 2026), about 220 pull requests on ResiCore and OrganiCore, and the existing rule files in GreenHumanResource (`CLAUDE.md`, the most complete), ResiCore (`CLAUDE.md`, `.ai/entity-management.md`), IMEXCO (`CLAUDE.md`, `ThrottlesSubmissions`), OrganiCore and the `laravel-translation-sync` package.

## Sources

- Repos: GreenHumanResource `CLAUDE.md`, ResiCore `CLAUDE.md` and `.ai/entity-management.md`, IMEXCO `CLAUDE.md` and `app/Support/Livewire/ThrottlesSubmissions.php`, OrganiCore `CLAUDE.md` and `routes/`, `laravel-translation-sync`
- Pull request history on ResiCore (#120–#219) and OrganiCore (#533–#632); Claude Code session titles and summaries, Oct 2026
- Added practice: Laravel rate limiting, OWASP Top 10, OWASP CSP cheat sheet, WCAG 2.2, Spatie Laravel guidelines, Conventional Commits

## Using these pages

- Start at the [table of contents](../README.md#table-of-contents) to jump to a topic.
- Every page has a breadcrumb at the top and previous/next links at the top and bottom.
- Want the whole set on one page? Read the [summary](../SUMMARY.md).
- Pasting rules into an AI agent? Use the short [agent prompt](../ai-agents/CLAUDE.md) instead.
