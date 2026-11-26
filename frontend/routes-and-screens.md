[Rules index](../README.md) › Frontend › Routes and screens

**Navigation:** Previous: [Views and components](views-and-components.md) · Next: [Data and performance](../backend/data-and-performance.md) · [Table of contents](../README.md#table-of-contents)

# Routes and screens

Each task gets its own URL: forms, tabs and detail panels are pulled out of list pages into dedicated routes.

A page that is a URL can be bookmarked, shared, reloaded, opened in a new tab, tested with a single request, and linked from an email. A modal or a hidden tab cannot do any of these. Most of the rules below follow from that.

---

## Own route per task

- `[H]` **MUST** Create and edit forms are their own full-page Livewire components on their own routes (`/budgets/create`, `/budgets/{budget}/edit`), not modals or inline panels on the list page.
  - **Benefit:** A form on its own page can be reloaded without losing its place and can show validation errors at full width. A failed save returns the user to a clear page, not a modal stacked on a list that may have changed. The route can also be authorized as a whole with middleware.
  - **Example:** `Route::get('budgets/{budget}/edit', EditBudget::class)->name('budgets.edit')->middleware('can:budgets.update,budget');`

- `[H]` **MUST** Tabs that are really separate reports or areas become separate routes (BI report per category, visitor announcement, demo page, FAQ page, terms page, notifications "see all" page).
  - **Benefit:** A report with its own URL can be shared with an accountant or linked from a dashboard. Tabs that only switch state on one page cannot be linked to, and the browser's back button does not work with them.
  - **Deviate when:** The tab is a quick filter on the same data. Keep it on the page and persist the filter in the query string (see below).

---

## Naming

- `[H]` **MUST** URL segments and route names are in English and kebab-case (`my-lot`, `dues`), never French or Arabic, whatever the UI language.
  - **Benefit:** URLs stay stable when the translation changes, so existing links, bookmarks and search results do not break. A URL in a non-Latin script is also hard to type, copy and share.
  - **Example:** `/my-lot/dues` in every language. The French label "Mes lots" and the Arabic label are translated in the view, never in the URL.

- `[H]` **MUST** Use named routes and `route()` everywhere; group admin routes by feature and protect each group with permission middleware.
  - **Benefit:** If a URL changes, only the route definition changes, not every link. Grouping by feature with middleware means a new admin page is protected by default, not by someone remembering to add a check.
  - **Example:**
    ```php
    Route::prefix('admin/billing')
        ->name('billing.')
        ->middleware('can:billing.manage')
        ->group(function (): void {
            Route::get('invoices', InvoiceIndex::class)->name('invoices.index');
        });
    ```

- `[+]` **SHOULD** RESTful naming (`index`, `create`, `store`, `show`, `edit`, `update`, `destroy`); APIs versioned (`/api/v1`) with Eloquent API Resources and JSON errors.
  - **Benefit:** Standard names are recognised immediately by every Laravel developer. Versioned APIs let you change a response shape without breaking an app that already depends on the old one. API Resources keep the output shape in one class instead of ad-hoc arrays.

---

## Filters, pages and lists

- `[H]` **SHOULD** Filters and periods (month, quarter, year) persist in the query string so a screen can be bookmarked and shared.
  - **Benefit:** A manager can send a colleague the exact view they are looking at ("dues, Q3, overdue"). The back button returns the user to the same filter. Livewire's `#[Url]` attribute or `$queryString` makes this a single line.
  - **Example:** `#[Url(as: 'period')] public string $period = 'month';`

- `[H]` **SHOULD** Long lists are paginated (25 per page by default), including audit logs.
  - **Benefit:** A page with 25 records loads in a fraction of the time a page with 5,000 does, and the user can scan it. Audit logs in particular grow without limit, so they must always be paged.
  - **Deviate when:** The list is short and bounded by design (for example, the five roles a user has). Note the bound in a comment.

---

**Related:** [Views and components](views-and-components.md) (cards and the "two sections" limit) · [Security](../security/security.md) (policies and middleware on routes) · [Summary](../SUMMARY.md)
