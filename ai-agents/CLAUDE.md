# Project rules — read before every change

These rules apply to any web site or application. Map each term to the project's own stack.
If a rule conflicts with the task, stop and ask. Check every item under "Before you finish (self-check)" before handing back.

## Architecture
1. Entry points (routes, controllers, handlers, UI components) only hold state, validate, authorize and delegate. No database queries, direct storage writes or business rules in them.
2. All data access and business logic live in a service layer, one service per aggregate. Inject services; never create them inside a method. Services return data, never HTML or HTTP responses.
3. Authorize every create, read, update and delete on the server with a rule named `{entity}.{action}`. Hide controls with the same check in the UI.
4. Reuse existing components, services and helpers before creating new ones. No new top-level folders and no dependency changes without approval.

## Views
5. No logic in templates: no computation, filtering, grouping or formatting. Pass view-ready data.
6. No inline styles or style blocks. Use utility classes or the project stylesheet. Exceptions: data-driven CSS custom properties, print and PDF templates.
7. No inline script blocks or inline event attributes such as `onclick`. Use server-driven updates, then small client state, then bundled modules.
8. No table for list or admin screens; use responsive cards. Tables only for true reports, stacked on phones.
9. Reuse design-system components. Meet WCAG 2.2 AA. Support right-to-left layout for Arabic.

## Routes
10. Create and edit forms get their own full-page route, not a modal. Separate reports and areas get their own route.
11. URLs and route names are English kebab-case. Build links from route names, never hard-coded paths.

## Translations
12. Every visible string goes through the translation function, in a per-feature bundle with nested keys. Never hard-code text.
13. Add every key to every supported locale, then replace every placeholder marker before handing back.

## Security
14. Rate-limit every public form and endpoint with a named, configurable limit keyed by form and client address.
15. Scope every query to the current tenant, building or space.
16. Financial records use soft delete only, never permanent deletion. Log changes: who, what, old and new values.
17. Validate all input on the server, accepting only allow-listed fields. Escape output. Keep CSRF protection on. No secrets in code; never commit environment files.

## Data
18. Every schema or data change is a versioned migration. Store money as integer minor units or decimal, never floating point.
19. No N+1 queries: load related data in one query or batch. Detect lazy loading outside production.

## Quality and Git
20. Use explicit types and the language's strict mode wherever available.
21. Write automated tests for every behaviour change, including failure and authorization paths. Never delete or skip a test to get green.
22. Run the formatter, static analyzer and narrowest relevant tests before handing back.
23. Branch from the integration branch and open pull requests into it, never into the release branch. Commit as `type(scope): subject`. No force-push to shared branches.

## Before you finish (self-check)
```bash
# Export these per project (values per stack: see the stack mapping).
: "${TEMPLATES:?}" "${HANDLERS:?}" "${DATA_ACCESS_RE:?}"
status=0
grep -rn '<script' "$TEMPLATES" | grep -v 'src=' && status=1   # must be empty
grep -rn '<style' "$TEMPLATES" && status=1                     # must be empty
grep -rn ' style=' "$TEMPLATES" && status=1                    # must be empty
grep -rnE '[[:space:]]on(click|change|submit|input|keydown)=' "$TEMPLATES" && status=1   # must be empty
grep -rn '<table' "$TEMPLATES" && status=1                     # lists must use cards
grep -rnE "$DATA_ACCESS_RE" $HANDLERS && status=1              # must be empty; $HANDLERS unquoted on purpose (lists, globs)
# run the project's missing-translation check: no missing keys
[ "$status" -eq 0 ]
```
- [ ] Logic in a service; entry points thin
- [ ] No inline styles or scripts; cards not tables
- [ ] Own route per form and report; English URLs
- [ ] Every string translated in every supported locale
- [ ] Public endpoints rate-limited; actions authorized
- [ ] Migration and tests added; formatter, analyzer and tests run
- [ ] Hand-off names what ran, what did not, and what is still needed
