[Rules index](../README.md) › AI agents

**Navigation:** Previous: [Git workflow](../git/workflow.md) · Next: [Originals](../originals/CLAUDE.md) · [Table of contents](../README.md#table-of-contents)

# AI agent prompt

[`CLAUDE.md`](CLAUDE.md) is the short version of all the rules, for AI coding assistants. Paste it into each project's `CLAUDE.md` (or `AGENTS.md`). It keeps only the MUST rules and ends with grep guards and a checklist the agent runs before handing back.

## Why a short version exists

An assistant reads its instructions on every task. A long document is partly skipped, and the rules most likely to be missed are the ones buried in the middle. The short prompt keeps every MUST rule in a numbered list the agent can check one by one, and it puts the self-check at the end, where the agent reads it last.

| Use this | When |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Pasting into a project's `CLAUDE.md` or `AGENTS.md`: the agent needs the rules and checklist every session |
| The category pages (linked from the [table of contents](../README.md#table-of-contents)) | A person wants the reason behind a rule, the example, or when a deviation is acceptable |
| The [summary](../SUMMARY.md) | A one-page review of every category |

## Keeping the prompt in step

The prompt repeats the MUST rules, so it must change when a MUST rule changes. When you edit a MUST rule on a category page, make the same change here, and keep the numbering stable so a reviewer can compare the two.
