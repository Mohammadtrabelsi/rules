[Rules index](../README.md) › Frontend › Views and components

**Navigation:** Previous: [Layering and patterns](../architecture/layering-and-patterns.md) · Next: [Routes and screens](routes-and-screens.md) · [Table of contents](../README.md#table-of-contents)

# Views and components

Templates render view-ready data. Styling lives in stylesheets. Behaviour lives in the server-side UI layer, in lightweight client state, or in bundled script files. Works for server-rendered pages, single-page apps and static sites alike.

Run the self-check in [Testing](../testing/testing.md#self-check-before-finishing) before handing back a view change: most of the rules below can be verified with a few commands.

---

## No logic, inline styles or inline scripts

### No logic in templates

- `[H]` **MUST** No computation, filtering, grouping or formatting inside a template. Control flow for rendering (conditions, loops, permission checks that decide what to show) is fine. Dates, money and percentages are formatted in the service or the component, before the template sees them.
  - **Benefit:** Logic in a template cannot be unit-tested without rendering HTML, and it is repeated wherever the template is copied. Formatting in one place means one currency format everywhere.
  - **Example:**
    ```text
    Bad:   <span>{{ format(invoice.total_minor / 100, 2) }} €</span>
    Good:  <span>{{ invoice.formatted_total }}</span>
    ```

### No inline styles

- `[H]` **MUST** No `style` attributes and no style blocks in templates. Use the project's utility classes or its stylesheet. The only exceptions are a value that is truly data-driven, and print or PDF templates.
  - **Benefit:** Inline styles are hard to change consistently and cannot be overridden by a theme or dark mode. They also block a strict Content-Security-Policy, which is the next rule's point.
  - **Deviate when:** The value is data-driven, such as a progress bar width. Set a CSS custom property once in the template and style the bar in the stylesheet: `style="--pct: 40%"`.

### No inline scripts or handlers

- `[H]` **MUST** No inline script blocks and no inline event attributes (`onclick`, `onchange` and the rest) in templates. Prefer, in this order: the framework's server-driven updates (see [Stack mapping](../stacks/README.md)); small client-side state for purely visual behaviour; a bundled module in the project's script folder, built by the project's bundler.
  - **Benefit:** Server-side and client-side state stay in one place and work together. Bundled modules are minified, versioned and cacheable. Inline handlers run outside the framework's lifecycle, so they miss updates after a re-render.
  - **Example:**
    ```text
    Bad:   <button onclick="openMenu()">Menu</button>

    Good:  <div data-menu>                       (small client-side state, visual only)
             <button type="button" aria-expanded="false">Menu</button>
           </div>

    Good:  <button type="button" data-action="save">Save</button>
           (the server-driven update attaches the handler; the server knows the state)
    ```

- `[+]` **SHOULD** Keep the app compatible with a strict Content-Security-Policy (no `unsafe-inline`), which the three rules above make possible.
  - **Benefit:** A strict CSP blocks injected scripts even when an output escape is missed. It is one of the strongest defences against cross-site scripting that a server can set on its own.

---

## Layout and components

### Cards instead of tables

- `[H]` **MUST** No table for admin and list screens. Render records as responsive cards (a card grid, each card with a heading, a key-value list of its fields, and its actions) with sort chips and a filter bar. A table is acceptable only for genuinely tabular reports, such as a balance sheet, and it must stack on narrow screens.
  - **Benefit:** Tables overflow on phones and need horizontal scrolling, which fails the mobile rule. A card keeps the record's key fields, status and actions together, and it reads the same at every width.
  - **Deviate when:** The screen is a real report where columns are compared against each other. Then use a table and make it stack on narrow widths.

### One design system

- `[H]` **MUST** One shared design system per project. Give its classes or components a project prefix (for example `app-`, `shop-`), and reuse its components (flash message, page header, action buttons, sort chip) instead of one-off markup.
  - **Benefit:** A prefix keeps project classes from colliding with framework or third-party classes. Shared components mean a button looks and behaves the same on every screen, and a fix to a component fixes every screen.

### Screen size

- `[H]` **SHOULD** Keep screens simple: at most two sections per component; split anything bigger into its own page.
  - **Benefit:** A screen with two clear sections can be understood at a glance. A long component with many sections is hard to test, slow to load, and hard to change safely. Splitting it also gives each part its own bookmarkable URL (see [Routes](routes-and-screens.md)).

- `[H]` **SHOULD** Navigation is grouped by role or area, with breadcrumbs, a collapsible sidebar on wide screens, and the active item highlighted. The language switcher and the theme toggle sit in the top bar.
  - **Benefit:** Users see only the areas they can use, and always know where they are. Breadcrumbs and an active item reduce "where am I" errors, and the top bar keeps the language and theme controls one click away.

- `[H]` **SHOULD** Icons and logos are sized by CSS classes, consistently per heading level.
  - **Benefit:** An icon sized by class is changed in one place. Icons sized inline drift to different sizes across screens and look unprofessional.

### Accessibility

- `[+]` **MUST** Meet WCAG 2.2 AA: a label on every input, visible focus, menus reachable by keyboard, colour contrast of at least 4.5:1 for normal text, and a layout that honours the document's text direction.
  - **Benefit:** Labels tell screen-reader users what a field is for. Visible focus and keyboard access let people who cannot use a mouse operate the app. Contrast of 4.5:1 keeps text readable in sunlight and for people with low vision. WCAG 2.2 AA is the benchmark that accessibility standards and procurement rules commonly refer to; check the rules that apply to each client.
  - **Example:**
    ```text
    <label for="iban">{{ t("billing.fields.iban") }}</label>
    <input id="iban" name="iban" type="text" aria-describedby="iban-help">
    <p id="iban-help">{{ t("billing.help.iban") }}</p>
    ```

### Mobile first

- `[+]` **SHOULD** Mobile first: every screen is checked at phone width, with no horizontal scroll.
  - **Benefit:** Many users work from a phone. A layout that works at phone width is usually simpler and works on desktop too.

### Build step

- `[H]` **MUST** After any stylesheet or script change, state the build step the project needs (for example, `npm run build` or the project's equivalent) before the change is reviewed.
  - **Benefit:** Without a build, the change is missing and the reviewer sees the old screen, which looks like a bug in the change. Saying so in the hand-off avoids a false report.

---

**Related:** [Routes and screens](routes-and-screens.md) · [Testing self-check](../testing/testing.md#self-check-before-finishing) · [Translations](../i18n/translations.md) (right-to-left and translated labels) · [Summary](../SUMMARY.md)
