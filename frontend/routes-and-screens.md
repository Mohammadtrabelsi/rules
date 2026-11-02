# Routes and screens

Each task gets its own URL: forms, tabs and detail panels are pulled out of list pages into dedicated routes.

- `[H]` **MUST** Create and edit forms are their own full-page Livewire components on their own routes (`/budgets/create`, `/budgets/{budget}/edit`), not modals or inline panels on the list page.
- `[H]` **MUST** Tabs that are really separate reports or areas become separate routes (BI report per category, visitor announcement, demo page, FAQ page, terms page, notifications "see all" page).
- `[H]` **MUST** URL segments and route names are in English and kebab-case (`my-lot`, `dues`), never French or Arabic, whatever the UI language.
- `[H]` **MUST** Use named routes and `route()` everywhere; group admin routes by feature and protect each group with permission middleware.
- `[H]` **SHOULD** Filters and periods (month, quarter, year) persist in the query string so a screen can be bookmarked and shared.
- `[H]` **SHOULD** Long lists are paginated (25 per page by default), including audit logs.
- `[+]` **SHOULD** RESTful naming (`index`, `create`, `store`, `show`, `edit`, `update`, `destroy`); APIs versioned (`/api/v1`) with Eloquent API Resources and JSON errors.
