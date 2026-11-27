[Rules index](../README.md) › Frontend › Routes and screens

**Navigation:** Previous: [Views and components](views-and-components.md) · Next: [Data and performance](../backend/data-and-performance.md) · [Table of contents](../README.md#table-of-contents)

# Routes and screens

Each task gets its own URL: forms, tabs and detail panels are pulled out of list pages into dedicated routes.

A page that is a URL can be bookmarked, shared, reloaded, opened in a new tab, tested with a single request, and linked from an email. A modal or a hidden tab cannot do any of these. Most of the rules below follow from that.

---

## Own route per task

- `[H]` **MUST** Create and edit forms are full pages on their own routes (for example `/budgets/new` and `/budgets/{id}/edit`), not modals or inline panels on the list page.
  - **Benefit:** A form on its own page can be reloaded without losing its place and can show validation errors at full width. A failed save returns the user to a clear page, not a modal stacked on a list that may have changed. The route can also be authorized as a whole.
  - **Example:**
    ```text
    GET  /budgets/{id}/edit    -> edit page    requires permission "budgets.update" on that budget
    ```

- `[H]` **MUST** Tabs that are really separate reports or areas become separate routes (for example a report per category, a public FAQ page, a terms page, a "see all notifications" page).
  - **Benefit:** A report with its own URL can be shared with an accountant or linked from a dashboard. Tabs that only switch state on one page cannot be linked to, and the browser's back button does not work with them.
  - **Deviate when:** The tab is a quick filter on the same data. Keep it on the page and persist the filter in the query string (see below).

---

## Naming

- `[H]` **MUST** URL segments and route names are in English and kebab-case (`my-lot`, `dues`), never in the interface language, whatever the UI language.
  - **Benefit:** URLs stay stable when the translation changes, so existing links, bookmarks and search results do not break. A URL in a non-Latin script is also hard to type, copy and share.
  - **Example:** `/my-lot/dues` in every language. The French label "Mes lots" and the Arabic label are translated in the view, never in the URL.

- `[H]` **MUST** Build links from named routes everywhere, and protect each group of admin routes with a permission check at the group level.
  - **Benefit:** If a URL changes, only the route definition changes, not every link. Grouping by feature with a permission check means a new admin page is protected by default, not by someone remembering to add a check.
  - **Example:**
    ```text
    group "admin/billing", permission "billing.manage":
        route "invoices"  -> invoice list    (name: billing.invoices.index)
        route "invoices/new" -> invoice form (name: billing.invoices.create)
    ```

- `[+]` **SHOULD** Use standard action names (`index`, `create`, `store`, `show`, `edit`, `update`, `destroy`). Version public APIs (`/api/v1`) and define each response shape in one place.
  - **Benefit:** Standard names are recognised immediately by every developer on the team. Versioned APIs let you change a response shape without breaking an app that already depends on the old one. One definition of each response keeps the output shape consistent.

---

## Filters, pages and lists

- `[H]` **SHOULD** Filters and periods (month, quarter, year) persist in the query string so a screen can be bookmarked and shared.
  - **Benefit:** A manager can send a colleague the exact view they are looking at ("dues, Q3, overdue"). The back button returns the user to the same filter.
  - **Example:** `/dues?period=quarter&status=overdue`

- `[H]` **SHOULD** Long lists are paginated (25 per page by default), including audit logs.
  - **Benefit:** A page with 25 records loads in a fraction of the time a page with 5,000 does, and the user can scan it. Audit logs grow without limit, so they must always be paged.
  - **Deviate when:** The list is short and bounded by design (for example, the five roles a user can hold). Note the bound in a code comment.

---

**Related:** [Views and components](views-and-components.md) (cards and the "two sections" limit) · [Security](../security/security.md) (authorization on routes) · [Stack mapping](../stacks/README.md) · [Summary](../SUMMARY.md)
