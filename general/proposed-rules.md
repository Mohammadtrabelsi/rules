[Rules index](../README.md) › General › Proposed rules

**Navigation:** Previous: [Git workflow](../git/workflow.md) · Next: [AI agent prompt](../ai-agents/README.md) · [Table of contents](../README.md#table-of-contents)

# Proposed rules (not yet adopted)

> **Status: proposal.** Nothing on this page is a house rule yet. Each item needs an explicit decision before it becomes a **MUST** or **SHOULD** on a category page and before it goes into the [agent prompt](../ai-agents/CLAUDE.md). Items are listed with the benefit that would justify adopting them.

Each proposal follows the [same format](how-to-read.md#anatomy-of-a-rule) as a real rule, with a suggested level.

---

## P1. Never swallow an exception

- **Suggested level:** **SHOULD**
- **Rule:** Do not write an empty `catch`. Either handle the exception with a clear, specific action, or let it propagate. When catching, log the exception with the record ID or context that would help find it.
- **Benefit:** An empty `catch` turns a failure into silence. A refund that fails quietly looks like a refund that succeeded, which is the hardest kind of bug to find.
- **Example:**
  ```php
  // Bad: the failure disappears
  try { $this->mailer->send($mail); } catch (Throwable) {}

  // Better: the failure is recorded with context and the job can retry
  try {
      $this->mailer->send($mail);
  } catch (TransportException $e) {
      Log::warning('Dues reminder not sent', ['invoice_id' => $invoice->id, 'error' => $e->getMessage()]);
      throw $e;
  }
  ```

## P2. Store and compare times in UTC

- **Suggested level:** **SHOULD**
- **Rule:** Store every timestamp in UTC. Convert to the user's timezone only when displaying it, and set the timezone once per request.
- **Benefit:** Mixed timezones produce off-by-one-day errors around midnight and during daylight-saving changes. A single storage timezone makes ordering and due-date comparisons correct.

## P3. Back up before a destructive migration

- **Suggested level:** **SHOULD** (**MUST** for dropping a column or table with production data)
- **Rule:** Before a migration that drops a column, a table or rows, take a database backup in the deploy plan and state the restore step in the PR.
- **Benefit:** A dropped column cannot be recovered from the schema. The backup is the only way back, and writing the restore step down makes it usable under pressure.

## P4. Watch the failed-jobs table

- **Suggested level:** **SHOULD**
- **Rule:** Queued work (invoices, notifications, imports) has an alert or a regular check on the failed-jobs table, and a retry command documented in the project.
- **Benefit:** A failed queued notification produces no error on screen. Without a check, a whole batch of reminders can fail for days before anyone notices.

## P5. Audit dependencies in CI

- **Suggested level:** **SHOULD**
- **Rule:** CI runs `composer audit` and `npm audit` (or the equivalent) and reports known vulnerabilities. A high-severity finding blocks the merge until it is fixed or explicitly accepted with a reason.
- **Benefit:** Most real-world compromises use a known, already-published vulnerability in a dependency. An automatic check finds them when they are published, not after an incident.

## P6. Automated accessibility checks on key screens

- **Suggested level:** **SHOULD**
- **Rule:** A browser test (for example, Pest's browser plugin with an axe-core check) runs on the main screens of each area: login, the dashboard, one form and one list.
- **Benefit:** The WCAG rules in [Views and components](../frontend/views-and-components.md#accessibility) are easy to break with one new class. An automated check catches missing labels and low contrast on every run, which manual review does not do reliably.

---

## Adopting a proposal

1. Discuss the item and decide whether to adopt it, at which level, and for which projects.
2. Move the rule into the right category page, in the standard format, with a benefit and an example.
3. Add it to the [summary](../SUMMARY.md), and to the [agent prompt](../ai-agents/CLAUDE.md) if it is a **MUST**.
4. Delete it from this page, so there is only one source of truth.
