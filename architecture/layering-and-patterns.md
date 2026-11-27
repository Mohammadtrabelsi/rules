[Rules index](../README.md) › Architecture › Layering and patterns

**Navigation:** Previous: [Code quality](../general/code-quality.md) · Next: [Views and components](../frontend/views-and-components.md) · [Table of contents](../README.md#table-of-contents)

# Architecture and layering

Every request flows one way: **entry point → service → data access**, and the view only renders what it is handed. The names of these layers differ between frameworks; the flow does not. Concrete names per stack are in [Stack mapping](../stacks/README.md).

```text
Route / handler ──► Controller or UI component ──► Service ──► Data access (ORM, SQL, API client)
                    (state, validate,              (business rules,
                     authorize, delegate)           returns data)
                             │
                             ▼
                       View (renders what it is handed)
```

---

## Thin entry points

### No queries in controllers or UI components

- `[H]` **MUST** Controllers, route handlers and UI components contain no database queries, no direct writes to storage and no business rules. They hold UI state, validate, authorize, delegate to a service and map the result back.
  - **Benefit:** The same logic is reachable from a web page, an API endpoint, a background job and a command line tool without copying it. It is also testable without an HTTP request. When a rule changes, there is one place to change.
  - **Example:**
    ```text
    handle "refund payment" request:
        authorize "payments.refund" on payment
        payment_service.refund(payment, validated_amount)
        notify the page: "refunded"
    ```
  - **Deviate when:** Never for business rules. A trivial read for a view-only value still belongs in the service.

### One service per aggregate

- `[H]` **MUST** All data access and business logic live in a service under a dedicated service folder, with one service per aggregate (for example, an invoice and its lines), not one per table. Sub-domains go in sub-folders.
  - **Benefit:** An aggregate is changed as one unit, so its rules belong together. One class per table produces many small classes that call each other, and business rules end up scattered.
  - **Deviate when:** A sub-domain grows large enough to deserve its own service, such as `payroll/payslip_service`. Put it in a sub-folder, not at the top level.

### Dependency injection

- `[H]` **MUST** Inject services through the framework's injection mechanism or the constructor. Never create a service inside a method, and never reach a model or client through a global lookup. Keep service handles out of anything that is serialised to the browser, such as client-side component state or the session.
  - **Benefit:** Injected services can be replaced with fakes in tests. A handle stored in state that is sent to the browser is exposed to the user and rebuilt from the request, so a service held there is a leak and a source of bugs.
  - **Example:**
    ```text
    class RefundForm:
        service: PaymentService        # injected, kept on the server only
        on start(service):
            this.service = service
    ```

### Services return data

- `[H]` **MUST** Services return domain data (records, collections, pages of results, data transfer objects, plain values), never rendered views or HTTP responses.
  - **Benefit:** A service that returns data can be called from a job or a command. A service that returns an HTTP response is tied to one transport and cannot be reused.

### Cross-cutting concerns

- `[H]` **SHOULD** Cross-cutting concerns (notifications, the audit log, PDF generation, exports) are their own services or listeners, composed by injection, not copied into each feature.
  - **Benefit:** Copying the audit or notification code into each feature means one forgotten copy produces a gap in the audit trail. A single service makes the behaviour consistent.

### Queues

- `[H]` **SHOULD** Long-running work (bulk billing runs, imports, notifications to many users) goes to a background job queue.
  - **Benefit:** The user gets a response in milliseconds instead of waiting on a page that times out. Failed jobs can be retried without the user repeating the action.
  - **Deviate when:** The work is short and the user needs the result immediately to continue. Keep it synchronous and say why.

---

## Design patterns

Each row names a pattern, where it usually lives, and how strict the rule is. The folder names are examples; see [Stack mapping](../stacks/README.md) for each framework.

| Pattern | Where | Level | Benefit |
|---|---|---|---|
| Service layer | a `services` folder or module | `[H]` MUST | One place for business rules; reusable from web, API, jobs and commands |
| Authorization rules per entity, permission names `{entity}.{action}` | policy classes, guards, permission checks | `[H]` MUST | Authorization is named, checkable in one place and visible in the UI |
| Validation objects (form or request objects) | input classes next to the entry point | `[+]` SHOULD | Validation rules live with the input, not inside the handler |
| Enums for statuses and types | an enum or constants module | `[H]` SHOULD | A typo in a status string is impossible; a `switch` over an enum can be checked for completeness |
| Shared behaviour in mixins, traits or concerns | a shared module | `[H]` SHOULD | Shared behaviour is written once and applied consistently |
| Observers, events or listeners for side effects | an events module | `[H]` SHOULD | A save does not need to know about every side effect; side effects can be added without touching the saving code |
| Reusable UI components for repeated markup (flash message, page header, action buttons, sort chip) | a components folder | `[H]` MUST | One change updates every screen; screens look and behave the same |
| Immutable data transfer objects when a call needs more than 3–4 arguments | a data-objects module | `[+]` SHOULD | A named object with named fields avoids argument-order mistakes |
| Interfaces for swappable providers (payment, email, AI model) | an interfaces or ports module | `[+]` SHOULD | Switching a provider or faking it in tests does not touch callers |

### Enum example

```text
enum InvoiceStatus:
    draft
    sent
    paid
```

Benefit: `InvoiceStatus.Pad` fails at analysis time; the string `"pad"` in a query would fail silently at runtime.

### Observer or listener example

Send a notification after an invoice is paid through a listener on the "invoice paid" event. Do not call the mailer from inside `PaymentService.record()`. Then a new side effect (for example, an accounting export) is one new listener, and the payment code does not change.

---

## Principles

- `[+]` **SHOULD** Follow SOLID, especially single responsibility and dependency inversion: depend on an interface where a second implementation is realistic.
  - **Benefit:** Code that depends on an interface can be tested with a fake and can switch implementation later without a rewrite.
  - **Deviate when:** There is only one implementation and no realistic second one. An interface with one implementation is extra code with no benefit.

- `[+]` **SHOULD** Do not add a repository layer on top of an ORM or data client that already acts as one. Match the altitude of the existing code.
  - **Benefit:** A repository over an ORM duplicates every query method and adds a layer to read without making the code more testable. The service is already the seam.
  - **Deviate when:** The project already has a repository for an aggregate. Follow it; do not start a second style.

- `[H]` **MUST** Reuse existing components, services and helpers before creating new ones; mirror the nearest well-factored sibling file.
  - **Benefit:** Reuse keeps the codebase small and consistent. A new file that copies an existing one's shape is easy to review because the reader already knows the pattern.
  - **Example:** Before writing a new "status badge", search the components folder for an existing badge. Before writing a new `InvoiceService`, read `PaymentService` and match its structure.

- `[H]` **MUST** No new top-level folders and no dependency changes without approval.
  - **Benefit:** A new top-level folder or package is a decision that every future developer inherits. Asking first keeps the structure one person can hold in their head.

---

**Related:** [Data and performance](../backend/data-and-performance.md) (transactions and queues in the service) · [Security](../security/security.md) (authorization called from the entry point) · [Stack mapping](../stacks/README.md) · [Summary](../SUMMARY.md)
