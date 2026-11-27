[Rules index](../README.md) › General › Proposed rules

**Navigation:** Previous: [Stack mapping](../stacks/README.md) · Next: [AI agent prompt](../ai-agents/README.md) · [Table of contents](../README.md#table-of-contents)

# Proposed rules (not yet adopted)

> **Status: proposal.** Nothing on this page is a house rule yet. Each item needs an explicit decision before it becomes a **MUST** or **SHOULD** on a category page and before it goes into the [agent prompt](../ai-agents/CLAUDE.md). Items are listed with the benefit that would justify adopting them.

Each proposal follows the [same format](how-to-read.md#anatomy-of-a-rule) as a real rule, with a suggested level.

---

## P1. Never swallow an error

- **Suggested level:** **SHOULD**
- **Rule:** Do not write an empty error handler. Either handle the error with a clear, specific action, or let it propagate. When catching, record the error with the record ID or context that would help find it.
- **Benefit:** An empty handler turns a failure into silence. A refund that fails quietly looks like a refund that succeeded, which is the hardest kind of bug to find.
- **Example:**
  ```text
  // Bad: the failure disappears
  try: mailer.send(message)
  catch any error: (nothing)

  // Better: the failure is recorded with context and the job can retry
  try: mailer.send(message)
  catch TransportError as error:
      log warning "reminder not sent" with invoice_id and error.message
      raise error
  ```

## P2. Store and compare times in UTC

- **Suggested level:** **SHOULD**
- **Rule:** Store every timestamp in UTC. Convert to the user's timezone only when displaying it, and set the timezone once per request.
- **Benefit:** Mixed timezones produce off-by-one-day errors around midnight and during daylight-saving changes. A single storage timezone makes ordering and due-date comparisons correct.

## P3. Back up before a destructive migration

- **Suggested level:** **SHOULD** (**MUST** for dropping a column or table with production data)
- **Rule:** Before a migration that drops a column, a table or rows, take a database backup as part of the deploy plan, and state the restore step in the pull request.
- **Benefit:** A dropped column cannot be recovered from the schema. The backup is the only way back, and writing the restore step down makes it usable under pressure.

## P4. Watch the failed-job queue

- **Suggested level:** **SHOULD**
- **Rule:** Background work (invoices, notifications, imports) has an alert or a regular check on failed jobs, and a documented retry command.
- **Benefit:** A failed notification produces no error on screen. Without a check, a whole batch of reminders can fail for days before anyone notices.

## P5. Audit dependencies in CI

- **Suggested level:** **SHOULD**
- **Rule:** CI runs the stack's dependency audit (for example `npm audit`, `pip-audit`, `bundle audit` or `dotnet list package --vulnerable`) and reports known vulnerabilities. A high-severity finding blocks the merge until it is fixed or explicitly accepted with a reason.
- **Benefit:** Most real-world compromises use a known, already-published vulnerability in a dependency. An automatic check finds them when they are published, not after an incident.

## P6. Automated accessibility checks on key screens

- **Suggested level:** **SHOULD**
- **Rule:** A browser test (for example with Playwright or Cypress, and an accessibility engine such as axe-core) runs on the main screens of each area: sign-in, the home screen, one form and one list.
- **Benefit:** The WCAG rules in [Views and components](../frontend/views-and-components.md#accessibility) are easy to break with one new class. An automated check catches missing labels and low contrast on every run, which manual review does not do reliably.

---

## Adopting a proposal

1. Discuss the item and decide whether to adopt it, at which level, and for which projects.
2. Move the rule into the right category page, in the standard format, with a benefit and an example.
3. Add it to the [summary](../SUMMARY.md), and to the [agent prompt](../ai-agents/CLAUDE.md) if it is a **MUST**, with a matching row in the [source table](../ai-agents/README.md#where-each-numbered-rule-comes-from).
4. Delete it from this page, so there is only one source of truth.
