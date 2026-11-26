[Rules index](../README.md) › Frontend › Views and components

**Navigation:** Previous: [Layering and patterns](../architecture/layering-and-patterns.md) · Next: [Routes and screens](routes-and-screens.md) · [Table of contents](../README.md#table-of-contents)

# Views and frontend

Blade renders view-ready data; styling lives in stylesheets and behaviour lives in Livewire, Alpine or bundled JS.

Run the self-check greps listed in [Testing](../testing/testing.md#self-check-before-finishing) before handing back a view change: most of the rules below can be verified with one command.

---

## No inline PHP, CSS or JS

### No logic in Blade

- `[H]` **MUST** No `@php … @endphp` blocks and no logic in Blade. `@if`, `@foreach`, `@forelse`, `@can` for rendering are fine; computing, filtering, grouping, formatting (dates, money, percentages) belongs in the service or component.
  - **Benefit:** Logic in a template cannot be unit-tested without rendering HTML, and it is repeated wherever the template is copied. Formatting in the service means one currency format everywhere.
  - **Example:**
    ```blade
    {{-- Bad: formatting in the view --}}
    @php $total = number_format($invoice->total_minor / 100, 2) @endphp
    <span>{{ $total }} €</span>

    {{-- Good: the component passes a ready string --}}
    <span>{{ $invoice->formattedTotal }}</span>
    ```

### No inline styles

- `[H]` **MUST** No `style="…"` attributes and no `<style>` blocks. Use Tailwind utilities or the project stylesheet in `resources/css/` (e.g. `resicore.css`, `imexco-admin.css`). Only exceptions: a truly data-driven value (`style="width: {{ $pct }}%"`, preferably via a CSS custom property) and DomPDF templates in `resources/views/pdf/`.
  - **Benefit:** Inline styles are hard to change consistently and cannot be overridden by a theme or dark mode. They also block a strict Content-Security-Policy, which is the next rule's point.
  - **Deviate when:** The value is data-driven, such as a progress bar width. Prefer a CSS custom property set once, e.g. `style="--pct: {{ $pct }}%"`, with the bar styled in the stylesheet.

### No inline scripts or handlers

- `[H]` **MUST** No `<script>` tags and no native `onclick=` / `onchange=` handlers in Blade. Order of preference: Livewire `wire:*` → Alpine (`x-data`, `@click`, `x-on:change`) → a module in `resources/js/` bundled by Vite.
  - **Benefit:** Livewire and Alpine state stays in one place and works with the server-side component. Bundled modules are minified, versioned and cacheable. Native handlers run outside the framework's lifecycle, so they miss updates after a Livewire re-render.
  - **Example:**
    ```blade
    {{-- Bad --}}
    <button onclick="openMenu()">Menu</button>

    {{-- Good: Alpine for purely visual state --}}
    <div x-data="{ open: false }">
        <button type="button" @click="open = !open" :aria-expanded="open">Menu</button>
    </div>

    {{-- Good: Livewire when the server must know --}}
    <button type="button" wire:click="save">Save</button>
    ```

- `[+]` **SHOULD** Keep the app compatible with a strict Content-Security-Policy (no `unsafe-inline`), which these three rules make possible.
  - **Benefit:** A strict CSP blocks injected scripts even when an output escape is missed. It is one of the strongest defences against cross-site scripting that a server can set on its own.

---

## Layout and components

### Cards instead of tables

- `[H]` **MUST** No `<table>` for admin and list screens. Render records as responsive cards (card grid, item card with head / `dl` meta / actions) with sort chips and a filter bar. A table is acceptable only for genuinely tabular reports (balances, BI) and must stack on phones.
  - **Benefit:** Tables overflow on phones and need horizontal scrolling, which fails the mobile rule. A card keeps the record's key fields, status and actions together, and it reads the same at every width.
  - **Deviate when:** The screen is a real report where columns are compared, such as a balance sheet. Then use a table and make it stack on narrow widths.

### One design system

- `[H]` **MUST** One shared design system per project (classes prefixed per project, e.g. `rc-`, `ix-`); reuse its components (flash message, page hero, CRUD action buttons, sort chip) instead of one-off markup.
  - **Benefit:** A prefix keeps project classes from colliding with framework classes. Shared components mean a button looks and behaves the same on every screen, and a fix to a component fixes every screen.

### Screen size

- `[H]` **SHOULD** Keep screens simple: at most two sections per component; split anything bigger into its own page.
  - **Benefit:** A screen with two clear sections can be understood at a glance. A long component with many sections is hard to test, slow to load, and hard to change safely. Splitting it also gives each part its own bookmarkable URL (see [Routes](routes-and-screens.md)).

- `[H]` **SHOULD** Navigation is grouped by role/area (e.g. Habitat, Syndic team, Platform admin), with breadcrumbs, a collapsible sidebar and the active item highlighted; language switcher and theme toggle sit in the top bar.
  - **Benefit:** Users see only the areas they can use, and always know where they are. Breadcrumbs and an active item reduce "where am I" errors, and the top bar keeps the language and theme controls one click away.

- `[H]` **SHOULD** Icons and logos are sized by CSS classes, consistently per heading level.
  - **Benefit:** An icon sized by class is changed in one place. Icons sized inline drift to different sizes across screens and look unprofessional.

### Accessibility

- `[+]` **MUST** Accessibility to WCAG 2.2 AA: labels on every input, visible focus, keyboard-reachable menus, colour contrast ≥ 4.5:1, `dir="rtl"` honoured for Arabic.
  - **Benefit:** Labels let screen-reader users know what a field is for. Visible focus and keyboard access let people who cannot use a mouse operate the app. Contrast ≥ 4.5:1 keeps text readable in sunlight and for people with low vision. WCAG 2.2 AA is also the benchmark that accessibility standards and procurement rules commonly refer to; check the rules that apply to each client.
  - **Example:**
    ```blade
    <label for="iban">{{ __('billing.fields.iban') }}</label>
    <input id="iban" name="iban" type="text" wire:model="iban" aria-describedby="iban-help">
    <p id="iban-help">{{ __('billing.help.iban') }}</p>
    ```

### Mobile first

- `[+]` **SHOULD** Mobile first: every screen is checked at phone width; no horizontal scroll.
  - **Benefit:** Many residents and field staff use a phone. A layout that works at phone width is usually simpler and works on desktop too.

### Build step

- `[H]` **MUST** After any CSS/JS change, remind that `npm run build` is needed to see it.
  - **Benefit:** Without a build, the change is missing and the reviewer sees the old screen, which looks like a bug in the change. Saying so in the hand-off avoids a false report.

---

**Related:** [Routes and screens](routes-and-screens.md) · [Testing self-check](../testing/testing.md#self-check-before-finishing) · [i18n](../i18n/translations.md) (RTL and translated labels) · [Summary](../SUMMARY.md)
