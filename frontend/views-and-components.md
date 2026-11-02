# Views and frontend

Blade renders view-ready data; styling lives in stylesheets and behaviour lives in Livewire, Alpine or bundled JS.

## No inline PHP, CSS or JS

- `[H]` **MUST** No `@php … @endphp` blocks and no logic in Blade. `@if`, `@foreach`, `@forelse`, `@can` for rendering are fine; computing, filtering, grouping, formatting (dates, money, percentages) belongs in the service or component.
- `[H]` **MUST** No `style="…"` attributes and no `<style>` blocks. Use Tailwind utilities or the project stylesheet in `resources/css/` (e.g. `resicore.css`, `imexco-admin.css`). Only exceptions: a truly data-driven value (`style="width: {{ $pct }}%"`, preferably via a CSS custom property) and DomPDF templates in `resources/views/pdf/`.
- `[H]` **MUST** No `<script>` tags and no native `onclick=` / `onchange=` handlers in Blade. Order of preference: Livewire `wire:*` → Alpine (`x-data`, `@click`, `x-on:change`) → a module in `resources/js/` bundled by Vite.
- `[+]` **SHOULD** Keep the app compatible with a strict Content-Security-Policy (no `unsafe-inline`), which these three rules make possible.

## Layout and components

- `[H]` **MUST** No `<table>` for admin and list screens. Render records as responsive cards (card grid, item card with head / `dl` meta / actions) with sort chips and a filter bar. A table is acceptable only for genuinely tabular reports (balances, BI) and must stack on phones.
- `[H]` **MUST** One shared design system per project (classes prefixed per project, e.g. `rc-`, `ix-`); reuse its components (flash message, page hero, CRUD action buttons, sort chip) instead of one-off markup.
- `[H]` **SHOULD** Keep screens simple: at most two sections per component; split anything bigger into its own page.
- `[H]` **SHOULD** Navigation is grouped by role/area (e.g. Habitat, Syndic team, Platform admin), with breadcrumbs, a collapsible sidebar and the active item highlighted; language switcher and theme toggle sit in the top bar.
- `[H]` **SHOULD** Icons and logos are sized by CSS classes, consistently per heading level.
- `[+]` **MUST** Accessibility to WCAG 2.2 AA: labels on every input, visible focus, keyboard-reachable menus, colour contrast ≥ 4.5:1, `dir="rtl"` honoured for Arabic.
- `[+]` **SHOULD** Mobile first: every screen is checked at phone width; no horizontal scroll.
- `[H]` **MUST** After any CSS/JS change, remind that `npm run build` is needed to see it.
