[Rules index](../README.md) › General › How to read these rules

**Navigation:** Previous: — · Next: [Code quality](code-quality.md) · [Table of contents](../README.md#table-of-contents)

# How to read these rules

These rules apply to any web site or application, whatever its language or framework. They describe the work, not a tool. They beat an agent's or developer's defaults. If a rule conflicts with the task, stop and ask.

Rules name concepts such as "service layer", "authorization rule" or "migration". Each concept is a role in the code, and [Stack mapping](../stacks/README.md) says what that role is called in each framework. Examples on the category pages are neutral pseudo-code, so they read the same whatever your stack.

This page explains the notation every other page uses, so you can read any rule without looking anything up.

## Anatomy of a rule

Every rule in the category pages has the same shape:

```text
- `[H]` **MUST** <the rule itself>
  - **Benefit:** <why it is worth the cost>
  - **Example:** <a short illustration, where one helps>
  - **Deviate when:** <the narrow situations where breaking it is acceptable>
```

Not every rule needs every field. A rule with no example is a principle; a rule with no exception is one where the answer is always yes. Every rule has a benefit: `tools/check_rules.py` fails a rule that has none.

## Tags and levels

Each rule carries a **tag** and a **level**:

| Tag / level | Meaning | What to do with it |
|---|---|---|
| `[H]` | From history: learned from real projects and reviews, and found to prevent a problem that happened more than once | Treat as proven. It came from a real problem. |
| `[+]` | Added from well-established practice (framework documentation, OWASP, WCAG, accepted style guides) to round out the rules | Treat as the standard default. It fills a gap the history did not cover. |
| **MUST** | Never broken without explicit approval | Stop and ask before breaking it, even if it looks like the quicker path. |
| **SHOULD** | Default; deviate only with a stated reason | Follow it, and write the reason in the pull request if you do not. |

A `[+]` rule with a **MUST** level is a deliberate choice: it is an established practice that the house decided is not optional (for example, server-side validation and CSRF protection).

## Why the rules exist: the benefit principle

Each rule is written to prevent a specific cost. When you are unsure whether to follow a rule, ask what it protects:

| Cost it prevents | Examples in these rules |
|---|---|
| Money or records going wrong silently | Money as integer minor units, soft delete on financial records, audit logging |
| Users or data leaking across boundaries | Authorization rules, tenant scoping, rate limiting, no secrets in code |
| Slow pages that only break under real data | No N+1 queries, indexed filter columns, background work queued |
| Work that cannot be reviewed or rolled back | Migrations for every change, one concern per pull request, conventional commits |
| Interfaces that exclude people | WCAG 2.2 AA, right-to-left layouts, every string translated |
| A codebase that drifts into several styles | Reuse existing components, one design system, mirror sibling files |
| Hidden failures reported as success | Honest hand-offs, never skipping a test to get green |

## Where the `[H]` rules come from

The `[H]` rules were learned from several real projects and their review history. Their names appear here for provenance only; the rules themselves apply to any stack.

Sources for the history: the project instruction files of several production applications (the most complete was a human-resources application), a shared translation-sync tool, and the pull-request history of two multi-tenant applications.

## Sources

- Project instruction files and pull-request history from the applications named above.
- Added practice: rate limiting guidance, OWASP Top 10, OWASP Content Security Policy cheat sheet, WCAG 2.2, Conventional Commits, and the official documentation of each framework listed in [Stack mapping](../stacks/README.md).

## Using these pages

- Start at the [table of contents](../README.md#table-of-contents) to jump to a topic.
- Every page has a breadcrumb at the top and previous/next links at the top and bottom.
- Want the whole set on one page? Read the [summary](../SUMMARY.md).
- Pasting rules into an AI agent? Use the short [agent prompt](../ai-agents/CLAUDE.md) instead.
- Working in a specific framework? Use the [stack mapping](../stacks/README.md) to find the concrete names.
