"""Unit tests for tools/check_rules.py.

Run from the repository root:

    python3 -m unittest discover -s tests -v

Each test builds a small throw-away repository in a temporary folder, so the
checks are exercised on known input. The last class runs the checker on the
real repository and requires zero findings.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_rules", REPO_ROOT / "tools" / "check_rules.py")
check_rules = importlib.util.module_from_spec(_spec)
sys.modules["check_rules"] = check_rules  # dataclasses look the module up by name
_spec.loader.exec_module(check_rules)

PROMPT = "ai-agents/CLAUDE.md"
AGENT_INDEX = "ai-agents/README.md"
TESTING = "testing/testing.md"
SELF_CHECK = textwrap.dedent(
    """\
    ## Self-check before finishing

    ```bash
    grep -rn 'TODO' src          # must be empty
    ```
    """
)
PROMPT_BODY = "# Rules\n\n1. First rule\n2. Second rule\n\n" + SELF_CHECK.replace("Self-check before finishing", "Before you finish (self-check)")
VALID_INDEX = textwrap.dedent(
    """\
    # Rules index

    - [Testing](testing/testing.md)
    - [Prompt](ai-agents/CLAUDE.md)
    - [Agent index](ai-agents/README.md)
    - [Source](general/source.md)
    - [Summary](SUMMARY.md)
    """
)
VALID_SOURCES = "| # | Source |\n|---|---|\n| 1 | [Good](../general/source.md#good) |\n| 2 | [Good](../general/source.md#good) |\n"
VALID_SOURCE_BODY = "## Good\n\n- `[H]` **MUST** Do it.\n  - **Benefit:** Yes.\n"


def build_repo(files: dict[str, str]) -> Path:
    """Write the given files under a fresh temporary folder and return its path."""
    root = Path(tempfile.mkdtemp(prefix="rules-test-"))
    for name, content in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return root


def valid_repo(**overrides: str) -> dict[str, str]:
    """A minimal repository that passes every check; override any file by name."""
    files = {
        "README.md": VALID_INDEX,
        "SUMMARY.md": "# Summary\n",
        "testing/testing.md": "[Rules index](../README.md) › Testing\n\n# Testing\n\n" + SELF_CHECK,
        "general/source.md": "[Rules index](../README.md) › General\n\n# Source\n\n" + VALID_SOURCE_BODY,
        "ai-agents/CLAUDE.md": PROMPT_BODY,
        "ai-agents/README.md": "# Agent index\n\n" + VALID_SOURCES,
    }
    files.update(overrides)
    return files


def rule(tag: str, level: str, benefit: bool = True) -> str:
    lines = [f"- `[{tag}]` **{level}** Do the thing."]
    if benefit:
        lines.append("  - **Benefit:** It helps.")
    return "\n".join(lines) + "\n"


def category_page(body: str, breadcrumb: bool = True) -> str:
    head = "[Rules index](../README.md) › Testing\n\n" if breadcrumb else ""
    return head + "# Testing\n\n" + body


def findings_for(files: dict[str, str], check) -> list:
    corpus = check_rules.Corpus(build_repo(files))
    return check(corpus)


class FindingTests(unittest.TestCase):
    def test_str_format(self) -> None:
        finding = check_rules.Finding("a.md", 3, "links", "boom")
        self.assertEqual(str(finding), "a.md:3: [links] boom")


class SlugAndAnchorTests(unittest.TestCase):
    def test_slugify_lowercases_and_hyphenates(self) -> None:
        self.assertEqual(check_rules.slugify("Frontend: views"), "frontend-views")

    def test_slugify_drops_backticks_and_punctuation(self) -> None:
        self.assertEqual(check_rules.slugify("`[H]` Tags — and levels"), "h-tags--and-levels")

    def test_anchors_get_numeric_suffix_for_duplicates(self) -> None:
        self.assertEqual(check_rules.anchors_in("# A\n## A\n### A\n"), {"a", "a-1", "a-2"})

    def test_anchors_ignore_headings_inside_code_fences(self) -> None:
        text = "```\n# not a heading\n```\n# Real\n"
        self.assertEqual(check_rules.anchors_in(text), {"real"})

    def test_anchors_ignore_plain_text_hash_lines(self) -> None:
        self.assertEqual(check_rules.anchors_in("#hashtag without space\n"), set())


class LinkParsingTests(unittest.TestCase):
    def test_links_report_line_numbers_and_skip_code(self) -> None:
        text = "[a](one.md)\n```\n[b](hidden.md)\n```\n[c](two.md#x)\n"
        self.assertEqual(check_rules.links_in(text), [(1, "one.md"), (5, "two.md#x")])

    def test_link_with_title_is_parsed(self) -> None:
        self.assertEqual(check_rules.links_in('[a](one.md "Title")'), [(1, "one.md")])


class SelfCheckBlockTests(unittest.TestCase):
    def test_returns_bash_block_after_self_check_heading(self) -> None:
        text = "## Self-check\n\n```bash\ncmd one  \ncmd two\n```\n"
        self.assertEqual(check_rules.self_check_block(text), ["cmd one", "cmd two"])

    def test_skips_other_fences_before_the_bash_block(self) -> None:
        text = "## Self-check\n```text\nnot this\n```\n```bash\nthis\n```\n"
        self.assertEqual(check_rules.self_check_block(text), ["this"])

    def test_returns_none_without_self_check_heading(self) -> None:
        self.assertIsNone(check_rules.self_check_block("## Other\n```bash\nx\n```\n"))

    def test_returns_none_for_unclosed_block(self) -> None:
        self.assertIsNone(check_rules.self_check_block("## Self-check\n```bash\nx\n"))


class SectionTests(unittest.TestCase):
    def test_section_runs_until_next_heading_of_same_or_higher_level(self) -> None:
        text = "# Top\n\n## One\nalpha\n### Deep\nbeta\n## Two\ngamma\n"
        self.assertEqual(check_rules.section_text(text, "one"), "## One\nalpha\n### Deep\nbeta")

    def test_section_at_end_of_file_runs_to_the_end(self) -> None:
        self.assertEqual(check_rules.section_text("# A\n\nlast\n", "a"), "# A\n\nlast")

    def test_missing_section_returns_none(self) -> None:
        self.assertIsNone(check_rules.section_text("# A\n", "b"))

    def test_duplicate_heading_anchor_selects_the_second_section(self) -> None:
        text = "## Rule\nfirst\n## Rule\nsecond\n"
        self.assertEqual(check_rules.section_text(text, "rule-1"), "## Rule\nsecond")

    def test_numbered_rules_returns_line_and_value(self) -> None:
        self.assertEqual(check_rules.numbered_rules("1. a\n```\n9. x\n```\n2. b\n"), [(1, 1), (5, 2)])


class SourceCheckTests(unittest.TestCase):
    INDEX = (
        "# Agent index\n\n"
        "| # | Source |\n|---|---|\n"
        "| 1 | [Layering](../general/source.md#good) |\n"
    )
    GOOD_SOURCE = "# S\n\n## Good\n\n- `[H]` **MUST** Do it.\n  - **Benefit:** Yes.\n"

    def _files(self, prompt: str, index: str | None = None, source: str | None = None) -> dict[str, str]:
        files = valid_repo(**{PROMPT: prompt, "ai-agents/README.md": index or self.INDEX})
        files["general/source.md"] = source or self.GOOD_SOURCE
        return files

    def test_every_rule_with_a_must_source_passes(self) -> None:
        self.assertEqual(findings_for(self._files("1. Do it\n"), check_rules.check_sources), [])

    def test_rule_without_source_row_is_reported(self) -> None:
        found = findings_for(self._files("1. a\n2. b\n"), check_rules.check_sources)
        self.assertEqual([f.message for f in found], ["rule 2 has no source row in ai-agents/README.md"])

    def test_stale_source_row_is_reported(self) -> None:
        index = self.INDEX + "| 7 | [Old](../testing/testing.md#good) |\n"
        found = findings_for(self._files("1. a\n", index=index), check_rules.check_sources)
        self.assertEqual([f.message for f in found], ["source row 7 matches no numbered rule"])

    def test_duplicate_source_row_is_reported(self) -> None:
        index = self.INDEX + "| 1 | [Again](../testing/testing.md#good) |\n"
        found = findings_for(self._files("1. a\n", index=index), check_rules.check_sources)
        self.assertIn("listed twice", found[0].message)

    def test_source_pointing_at_missing_file_is_reported(self) -> None:
        index = "| 1 | [Gone](../nowhere.md#good) |\n"
        found = findings_for(self._files("1. a\n", index=index), check_rules.check_sources)
        self.assertIn("missing file '../nowhere.md'", found[0].message)

    def test_source_pointing_at_missing_anchor_is_reported(self) -> None:
        index = "| 1 | [Gone](../general/source.md#absent) |\n"
        found = findings_for(self._files("1. a\n", index=index), check_rules.check_sources)
        self.assertIn("missing anchor '#absent'", found[0].message)

    def test_source_section_without_must_is_reported(self) -> None:
        source = "# S\n\n## Good\n\n- `[+]` **SHOULD** Only a suggestion.\n  - **Benefit:** Yes.\n"
        found = findings_for(self._files("1. a\n", source=source), check_rules.check_sources)
        self.assertIn("cites a section with no MUST rule", found[0].message)


class RepositoryWalkTests(unittest.TestCase):
    def test_skips_tooling_and_hidden_folders(self) -> None:
        root = build_repo({
            "a.md": "x",
            "tools/skip.md": "x",
            "tests/skip.md": "x",
            ".git/skip.md": "x",
            ".github/skip.md": "x",
            "vendor/skip.md": "x",
            "sub/b.md": "x",
        })
        names = [check_rules.relative(root, p) for p in check_rules.markdown_files(root)]
        self.assertEqual(names, ["a.md", "sub/b.md"])

    def test_resolve_joins_relative_target(self) -> None:
        base = Path("/repo/frontend/page.md")
        self.assertEqual(check_rules.resolve(base, "../README.md"), Path("/repo/README.md"))


class CorpusTests(unittest.TestCase):
    def test_category_pages_exclude_proposed_rules_and_non_categories(self) -> None:
        corpus = check_rules.Corpus(build_repo(valid_repo(**{
            "testing/extra.md": "x",
            "general/proposed-rules.md": "x",
            "general/code.md": "x",
        })))
        names = sorted(corpus.rel(p) for p in corpus.category_pages())
        self.assertEqual(names, ["general/code.md", "general/source.md", "testing/extra.md", "testing/testing.md"])

    def test_anchor_cache_is_reused(self) -> None:
        corpus = check_rules.Corpus(build_repo(valid_repo()))
        path = corpus.root / TESTING
        first = corpus.anchors(path)
        self.assertIs(first, corpus.anchors(path))


class LinkCheckTests(unittest.TestCase):
    def test_missing_target_is_reported(self) -> None:
        files = valid_repo(**{"testing/testing.md": "[x](gone.md)\n"})
        found = findings_for(files, check_rules.check_links)
        self.assertEqual([f.check for f in found], ["links"])
        self.assertIn("missing target 'gone.md'", found[0].message)

    def test_missing_anchor_is_reported_with_target_file(self) -> None:
        files = valid_repo(**{"testing/testing.md": "[x](../README.md#nope)\n"})
        found = findings_for(files, check_rules.check_links)
        self.assertIn("missing anchor '#nope' in README.md", found[0].message)

    def test_valid_cross_file_anchor_passes(self) -> None:
        files = valid_repo(**{"testing/testing.md": "[x](../SUMMARY.md#title)\n"})
        files["SUMMARY.md"] = "# Title\n"
        self.assertEqual(findings_for(files, check_rules.check_links), [])

    def test_same_file_anchor_is_checked(self) -> None:
        files = valid_repo(**{"testing/testing.md": "# Top\n\n[ok](#top) [bad](#missing)\n"})
        found = findings_for(files, check_rules.check_links)
        self.assertEqual(len(found), 1)
        self.assertIn("#missing", found[0].message)

    def test_external_links_are_ignored(self) -> None:
        files = valid_repo(**{"testing/testing.md": "[a](https://example.com/x) [b](mailto:a@b.c)\n"})
        self.assertEqual(findings_for(files, check_rules.check_links), [])

    def test_directory_link_and_non_markdown_anchor_pass(self) -> None:
        files = valid_repo(**{
            "testing/testing.md": "[d](../ai-agents/) [img](pic.png#frag)\n",
            "testing/pic.png": "binary-ish",
        })
        self.assertEqual(findings_for(files, check_rules.check_links), [])


class ReachCheckTests(unittest.TestCase):
    def test_orphan_page_is_reported(self) -> None:
        files = valid_repo(**{"orphan/page.md": "# Orphan\n"})
        found = findings_for(files, check_rules.check_reach)
        self.assertEqual([f.path for f in found], ["orphan/page.md"])

    def test_pages_linked_from_index_are_reachable(self) -> None:
        self.assertEqual(findings_for(valid_repo(), check_rules.check_reach), [])

    def test_external_links_in_index_do_not_count(self) -> None:
        files = valid_repo(**{"README.md": VALID_INDEX + "[x](https://example.com/SUMMARY.md)\n"})
        files["SUMMARY.md"] = "# Summary\n"
        self.assertEqual(findings_for(files, check_rules.check_reach), [])


class StructureCheckTests(unittest.TestCase):
    def test_category_page_needs_breadcrumb(self) -> None:
        files = valid_repo(**{"testing/testing.md": category_page("", breadcrumb=False)})
        found = findings_for(files, check_rules.check_structure)
        self.assertEqual([f.message for f in found], ["category page must open with the breadcrumb"])

    def test_non_category_page_is_not_checked(self) -> None:
        files = valid_repo(**{"SUMMARY.md": "- **MUST** untagged bullet\n"})
        self.assertEqual(findings_for(files, check_rules.check_structure), [])

    def test_valid_tagged_rule_passes(self) -> None:
        body = rule("H", "MUST") + "\n" + rule("+", "SHOULD")
        self.assertEqual(findings_for(valid_repo(**{"testing/testing.md": category_page(body)}), check_rules.check_structure), [])

    def test_rule_without_benefit_is_reported(self) -> None:
        body = rule("H", "MUST", benefit=False)
        found = findings_for(valid_repo(**{"testing/testing.md": category_page(body)}), check_rules.check_structure)
        self.assertEqual([f.message for f in found], ["rule has no Benefit line"])

    def test_benefit_after_unindented_paragraph_does_not_count(self) -> None:
        body = "- `[H]` **MUST** Do it.\n\nA paragraph that ends the rule.\n  - **Benefit:** Too late.\n"
        found = findings_for(valid_repo(**{"testing/testing.md": category_page(body)}), check_rules.check_structure)
        self.assertEqual([f.message for f in found], ["rule has no Benefit line"])

    def test_benefit_after_blank_line_inside_rule_counts(self) -> None:
        body = "- `[H]` **MUST** Do it.\n\n  - **Benefit:** Still part of the rule.\n"
        self.assertEqual(findings_for(valid_repo(**{"testing/testing.md": category_page(body)}), check_rules.check_structure), [])

    def test_untagged_or_bad_tag_is_reported(self) -> None:
        body = "- **MUST** no tag here\n- `[X]` **SHOULD** bad tag\n"
        found = findings_for(valid_repo(**{"testing/testing.md": category_page(body)}), check_rules.check_structure)
        self.assertEqual(len(found), 2)
        self.assertTrue(all("needs a [H] or [+] tag" in f.message for f in found))

    def test_rule_syntax_inside_code_fence_is_ignored(self) -> None:
        body = "```\n- **MUST** example only\n```\n"
        self.assertEqual(findings_for(valid_repo(**{"testing/testing.md": category_page(body)}), check_rules.check_structure), [])

    def test_proposed_rules_page_is_exempt(self) -> None:
        files = valid_repo(**{"general/proposed-rules.md": "- **MUST** untagged\n"})
        self.assertEqual(findings_for(files, check_rules.check_structure), [])


class NumberingCheckTests(unittest.TestCase):
    def test_contiguous_numbering_passes(self) -> None:
        self.assertEqual(findings_for(valid_repo(**{PROMPT: "1. a\n2. b\n"}), check_rules.check_numbering), [])

    def test_gap_is_reported_and_recovers(self) -> None:
        found = findings_for(valid_repo(**{PROMPT: "1. a\n3. c\n4. d\n"}), check_rules.check_numbering)
        self.assertEqual([f.message for f in found], ["expected rule 2, found 3"])

    def test_missing_numbers_are_reported(self) -> None:
        found = findings_for(valid_repo(**{PROMPT: "# no numbers\n"}), check_rules.check_numbering)
        self.assertEqual([f.message for f in found], ["no numbered rules found"])

    def test_numbers_inside_code_fences_are_ignored(self) -> None:
        found = findings_for(valid_repo(**{PROMPT: "1. a\n```\n7. not a rule\n```\n2. b\n"}), check_rules.check_numbering)
        self.assertEqual(found, [])


class SyncCheckTests(unittest.TestCase):
    def test_identical_blocks_pass(self) -> None:
        self.assertEqual(findings_for(valid_repo(), check_rules.check_sync), [])

    def test_different_blocks_are_reported(self) -> None:
        files = valid_repo(**{PROMPT: PROMPT_BODY.replace("grep -rn 'TODO' src", "grep -rn 'FIXME' src")})
        found = findings_for(files, check_rules.check_sync)
        self.assertEqual(len(found), 1)
        self.assertIn("differs from testing/testing.md", found[0].message)

    def test_missing_block_in_prompt_is_reported(self) -> None:
        found = findings_for(valid_repo(**{PROMPT: "# no block\n"}), check_rules.check_sync)
        self.assertEqual(found[0].path, PROMPT)

    def test_missing_block_in_testing_is_reported(self) -> None:
        found = findings_for(valid_repo(**{TESTING: "# no block\n"}), check_rules.check_sync)
        self.assertEqual(found[0].path, TESTING)


class LintCheckTests(unittest.TestCase):
    def test_framework_term_is_reported(self) -> None:
        found = findings_for(valid_repo(**{"testing/testing.md": "Use Laravel here.\n"}), check_rules.check_lint)
        self.assertEqual(len(found), 1)
        self.assertIn("'Laravel'", found[0].message)

    def test_term_inside_code_fence_is_still_reported(self) -> None:
        found = findings_for(valid_repo(**{"testing/testing.md": "```\nDB::table('x')\n```\n"}), check_rules.check_lint)
        self.assertEqual(len(found), 1)

    def test_allow_marker_exempts_the_line(self) -> None:
        files = valid_repo(**{"testing/testing.md": "Sources: Laravel <!-- lint:allow -->\n"})
        self.assertEqual(findings_for(files, check_rules.check_lint), [])

    def test_stacks_and_originals_are_exempt(self) -> None:
        files = valid_repo(**{
            "stacks/laravel.md": "Laravel, Livewire and Pest.\n",
            "originals/notes.md": "Laravel.\n",
        })
        self.assertEqual(findings_for(files, check_rules.check_lint), [])

    def test_partial_names_do_not_match(self) -> None:
        self.assertEqual(findings_for(valid_repo(**{"testing/testing.md": "Pesto and Blades.\n"}), check_rules.check_lint), [])

    def test_php_inside_phpstan_is_reported_as_phpstan(self) -> None:
        found = findings_for(valid_repo(**{"testing/testing.md": "Run PHPStan.\n"}), check_rules.check_lint)
        self.assertIn("'PHPStan'", found[0].message)


class BudgetCheckTests(unittest.TestCase):
    def test_prompt_within_budget_passes(self) -> None:
        self.assertEqual(findings_for(valid_repo(), check_rules.check_budget), [])

    def test_prompt_over_budget_is_reported(self) -> None:
        with mock.patch.object(check_rules, "PROMPT_WORD_BUDGET", 3):
            found = findings_for(valid_repo(), check_rules.check_budget)
        self.assertEqual(len(found), 1)
        self.assertIn("budget is 3", found[0].message)


class RequiredFilesTests(unittest.TestCase):
    def test_missing_core_file_is_reported_and_other_checks_are_skipped(self) -> None:
        files = valid_repo()
        del files[PROMPT]
        report = check_rules.run_checks(build_repo(files))
        self.assertEqual([f.check for f in report.findings], ["required"])
        self.assertIn(PROMPT, report.findings[0].message)

    def test_all_core_files_present_yields_no_findings(self) -> None:
        corpus = check_rules.Corpus(build_repo(valid_repo()))
        self.assertEqual(check_rules.check_required(corpus), [])


class MetricsTests(unittest.TestCase):
    def test_metrics_count_words_lines_and_tokens(self) -> None:
        corpus = check_rules.Corpus(build_repo(valid_repo(**{"testing/testing.md": "one two three\n"})))
        metrics = check_rules.collect_metrics(corpus)
        self.assertEqual(metrics["files"]["testing/testing.md"]["words"], 3)
        self.assertEqual(metrics["files"]["testing/testing.md"]["lines"], 2)
        self.assertGreater(metrics["prompt_est_tokens"], 0)

    def test_framework_hits_exclude_stacks_and_allowed_lines(self) -> None:
        files = valid_repo(**{
            "stacks/laravel.md": "Laravel Livewire\n",
            "testing/testing.md": "Laravel <!-- lint:allow -->\nPest\n",
        })
        metrics = check_rules.collect_metrics(check_rules.Corpus(build_repo(files)))
        self.assertEqual(metrics["framework_term_hits"], 1)

    def test_run_checks_reports_sorted_findings_and_timing(self) -> None:
        files = valid_repo(**{"testing/testing.md": "Laravel\nPest\n"})
        report = check_rules.run_checks(build_repo(files))
        lines = [f.line for f in report.findings if f.path == TESTING]
        self.assertEqual(lines, sorted(lines))
        self.assertIn("seconds", report.metrics)
        self.assertEqual(report.metrics["pages_checked"], len(files))


class MainTests(unittest.TestCase):
    def test_exit_zero_and_pass_banner_on_clean_repo(self) -> None:
        root = build_repo(valid_repo())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check_rules.main(["--root", str(root), "--metrics"])
        self.assertEqual(code, 0)
        self.assertIn("static checks: PASS", out.getvalue())
        self.assertIn("agent prompt words", out.getvalue())

    def test_missing_core_file_with_metrics_does_not_crash(self) -> None:
        files = valid_repo()
        del files[AGENT_INDEX]
        root = build_repo(files)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check_rules.main(["--root", str(root), "--metrics"])
        self.assertEqual(code, 1)
        self.assertIn("[required]", out.getvalue())
        self.assertNotIn("agent prompt words", out.getvalue())

    def test_exit_one_and_finding_lines_on_broken_repo(self) -> None:
        root = build_repo(valid_repo(**{"testing/testing.md": "Laravel [x](gone.md)\n"}))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check_rules.main(["--root", str(root)])
        self.assertEqual(code, 1)
        self.assertIn("[links]", out.getvalue())
        self.assertIn("[lint]", out.getvalue())
        self.assertIn("FAIL", out.getvalue())


@unittest.skipUnless(shutil.which("bash"), "needs bash to run the self-check block")
class SelfCheckBehaviourTests(unittest.TestCase):
    """Runs the self-check block that ships in the agent prompt, against small projects."""

    def _run_block(self, files: dict[str, str], env_overrides: dict[str, str] | None = None) -> int:
        block = check_rules.self_check_block((REPO_ROOT / PROMPT).read_text(encoding="utf-8"))
        self.assertIsNotNone(block)
        project = Path(tempfile.mkdtemp(prefix="selfcheck-"))
        for name, content in files.items():
            (project / name).parent.mkdir(parents=True, exist_ok=True)
            (project / name).write_text(content, encoding="utf-8")
        script = project / "selfcheck.sh"
        script.write_text("\n".join(block) + "\n", encoding="utf-8")
        env = {
            "PATH": os.environ.get("PATH", ""),
            "TEMPLATES": "templates",
            "HANDLERS": "controllers",
            "DATA_ACCESS_RE": r"DB::|::where\(",
        }
        env.update(env_overrides or {})
        env = {key: value for key, value in env.items() if value is not None}
        result = subprocess.run(["bash", str(script)], cwd=project, env=env, capture_output=True, text=True)
        return result.returncode

    def _clean(self, **overrides: str) -> dict[str, str]:
        files = {
            "templates/page.html": '<div class="card">x</div>\n<script src="/build/app.js"></script>\n',
            "controllers/handler.txt": "calls the service only\n",
        }
        files.update(overrides)
        return files

    def test_clean_project_passes(self) -> None:
        self.assertEqual(self._run_block(self._clean()), 0)

    def test_inline_script_fails(self) -> None:
        self.assertNotEqual(self._run_block(self._clean(**{"templates/page.html": "<script>x()</script>\n"})), 0)

    def test_inline_style_block_fails(self) -> None:
        self.assertNotEqual(self._run_block(self._clean(**{"templates/page.html": "<style>p{}</style>\n"})), 0)

    def test_style_attribute_fails(self) -> None:
        self.assertNotEqual(self._run_block(self._clean(**{"templates/page.html": '<p style="x">y</p>\n'})), 0)

    def test_inline_event_handler_fails(self) -> None:
        self.assertNotEqual(self._run_block(self._clean(**{"templates/page.html": '<b onclick="go()">y</b>\n'})), 0)

    def test_table_in_template_fails(self) -> None:
        self.assertNotEqual(self._run_block(self._clean(**{"templates/page.html": "<table></table>\n"})), 0)

    def test_data_access_in_handler_fails(self) -> None:
        self.assertNotEqual(self._run_block(self._clean(**{"controllers/handler.txt": "DB::table('x')\n"})), 0)

    def test_missing_variable_fails_loudly(self) -> None:
        self.assertNotEqual(self._run_block(self._clean(), env_overrides={"DATA_ACCESS_RE": None}), 0)


class RepositoryTests(unittest.TestCase):
    """The real repository must pass every static check: this is the gate."""

    def test_repository_has_zero_findings(self) -> None:
        report = check_rules.run_checks(REPO_ROOT)
        self.assertEqual([str(f) for f in report.findings], [])

    def test_prompt_is_within_budget(self) -> None:
        report = check_rules.run_checks(REPO_ROOT)
        self.assertLessEqual(report.metrics["prompt_words"], check_rules.PROMPT_WORD_BUDGET)


if __name__ == "__main__":
    unittest.main()
