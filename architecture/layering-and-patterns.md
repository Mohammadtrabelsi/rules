[Rules index](../README.md) › Architecture › Layering and patterns

**Navigation:** Previous: [Code quality](../general/code-quality.md) · Next: [Views and frontend](../frontend/views-and-components.md) · [Table of contents](../README.md#table-of-contents)

# Architecture and layering

Every request flows one way: **route → controller or Livewire component → service → model**, and the view only renders what it is handed.

```text
Route ──► Controller / Livewire ──► <Domain>Service ──► Eloquent model
            (state, validate,          (data access,        (persistence)
             authorize, delegate)       business rules)
                     │
                     ▼
                  View (renders what it is handed)
```

---

## Thin entry points

### No queries in controllers or Livewire

- `[H]` **MUST** Controllers and Livewire components contain no Eloquent queries (`::where`, `::find`, `::create`), no `DB::`, no `->save()/->update()/->delete()` and no business rules. They hold UI state, validate, authorize, delegate to a service and map the result back.
  - **Benefit:** The same logic is reachable from a web page, an API endpoint, a queued job and a console command without copying it. It is also testable without an HTTP request. When a rule changes, there is one place to change.
  - **Example:**
    ```php
    // Livewire component: thin
    public function refund(): void
    {
        $this->authorize('payments.refund', $this->payment);
        $this->payments->refund($this->payment, $this->validatedAmount());
        $this->dispatch('refunded');
    }
    ```
  - **Deviate when:** Never for business rules. A trivial read for a view-only value is still better in the service.

### One service per aggregate

- `[H]` **MUST** All data access and business logic live in a `<Domain>Service` under `app/Services/` (sub-domains in sub-folders, e.g. `app/Services/Payroll/`). One service per aggregate, not one per table.
  - **Benefit:** An aggregate (for example, an invoice and its lines) is changed as one unit, so its rules belong together. One class per table produces many small classes that call each other, and business rules end up scattered.
  - **Deviate when:** A sub-domain grows large enough to deserve its own service (for example, `Payroll/PayslipService`). Put it in a sub-folder, not at the top level.

### Dependency injection

- `[H]` **MUST** Inject services: constructor or action type-hint in controllers; `boot()` into a `protected` property in Livewire (never a public, serialized property). Never `new`, `app()` or facades to reach models.
  - **Benefit:** Injected services can be replaced with fakes in tests. In Livewire, a `public` property is sent to the browser and rehydrated from the request, so a public service would be serialized or exposed; a `protected` property is not.
  - **Example:**
    ```php
    class RefundForm extends Component
    {
        protected PaymentService $payments;

        public function boot(PaymentService $payments): void
        {
            $this->payments = $payments;
        }
    }
    ```

### Services return data

- `[H]` **MUST** Services return domain data (models, collections, paginators, DTOs, arrays), never views or HTTP responses.
  - **Benefit:** A service that returns data can be called from a job or command. A service that returns a `response()` is tied to HTTP and cannot be reused.

### Cross-cutting concerns

- `[H]` **SHOULD** Cross-cutting concerns (notifications, activity log, PDF, exports, CRUD notifications) are their own services or listeners, composed by DI, not copied.
  - **Benefit:** Copying the audit or notification code into each feature means one forgotten copy produces a gap in the audit trail. A single service makes the behaviour consistent.

### Queues

- `[H]` **SHOULD** Long-running work (bulk dues generation, imports, notifications to many users) goes to queued jobs.
  - **Benefit:** The user gets a response in milliseconds instead of waiting on a page that times out. Failed jobs can be retried without the user repeating the action.
  - **Deviate when:** The work is short and the user needs the result immediately to continue. Keep it synchronous and say why.

---

## Design patterns

Each row names a pattern, where it lives, and how strict the rule is.

| Pattern | Where | Level | Benefit |
|---|---|---|---|
| Service layer | `app/Services/*Service.php` | `[H]` MUST | One place for business rules; reusable from web, API, jobs and commands |
| Policies + Gates per entity, permission names `{entity}.{action}` | `app/Policies`, `ActionPermissions` | `[H]` MUST | Authorization is named, checkable in one place and visible in the UI with `@can` |
| Form objects / Form Requests for validation | Livewire Forms, `app/Http/Requests` | `[+]` SHOULD | Validation rules live with the input, not inside the component method |
| Enums for statuses and types (TitleCase keys) | `app/Enums` | `[H]` SHOULD | A typo in a status string is impossible; `match` on an enum is checked for exhaustiveness |
| Traits/Concerns for shared model behaviour (`EnforcesSoftDelete`, `MaintainsAuditChain`, `ThrottlesSubmissions`) | `app/Models/Concerns`, `app/Support` | `[H]` SHOULD | Shared behaviour is written once and applied consistently to every model that needs it |
| Observers / Events + queued Listeners for side effects | `app/Observers`, `app/Listeners` | `[H]` SHOULD | A save does not need to know about every side effect; side effects can be added or moved without touching the saving code |
| Reusable Blade components for repeated UI (flash message, hero, action buttons, sort chip) | `resources/views/components` | `[H]` MUST | One change updates every screen; screens look and behave the same |
| DTOs (readonly classes) when a service needs more than 3–4 loose arguments | `app/Data` | `[+]` SHOULD | A named object with named fields avoids argument-order mistakes |
| Strategy/driver interfaces for swappable providers (payment, AI provider via Prism) | `app/Contracts` + bindings | `[+]` SHOULD | Switching a provider or faking it in tests does not touch callers |

### Enum example

```php
enum InvoiceStatus: string
{
    case Draft = 'draft';
    case Sent = 'sent';
    case Paid = 'paid';
}
```

Benefit: `InvoiceStatus::Pad` fails at analysis time; the string `'pad'` in a `where` clause would fail silently.

### Observer or listener example

Use an observer or a queued listener to send a notification after an invoice is paid. Do not call the mailer from inside `PaymentService::record()`. Then a new side effect (for example, an accounting export) is one new listener, and the payment code does not change.

---

## Principles

- `[+]` **SHOULD** SOLID, especially single responsibility and dependency inversion: depend on interfaces where a second implementation is realistic.
  - **Benefit:** Code that depends on an interface can be tested with a fake and can switch implementation later without a rewrite.
  - **Deviate when:** There is only one implementation and no realistic second one. An interface with one implementor is extra code with no benefit.

- `[+]` **SHOULD** Don't add a repository layer on top of services; Eloquent already is one. Match the altitude of the existing code.
  - **Benefit:** A repository over Eloquent duplicates every query method and adds a layer to read without making the code more testable. The service is already the seam.
  - **Deviate when:** The project already has a repository for an aggregate. Follow it; do not start a second style.

- `[H]` **MUST** Reuse existing components, services and helpers before creating new ones; mirror the nearest well-factored sibling file.
  - **Benefit:** Reuse keeps the codebase small and consistent. A new file that copies an existing one's shape is easy to review because the reader already knows the pattern.
  - **Example:** Before writing a new "status badge", search `resources/views/components` for an existing badge. Before writing a new `InvoiceService`, read `PaymentService` and match its structure.

- `[H]` **MUST** No new top-level folders and no dependency changes without approval.
  - **Benefit:** A new top-level folder or package is a decision that every future developer inherits. Asking first keeps the structure one person can hold in their head.

---

**Related:** [Data and performance](../backend/data-and-performance.md) (transactions and queues in the service) · [Security](../security/security.md) (policies called from the controller) · [Summary](../SUMMARY.md)
