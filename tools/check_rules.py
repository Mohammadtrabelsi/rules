#!/usr/bin/env python3
"""Static checks for the rules repository. Standard library only.

Run from anywhere:

    python3 tools/check_rules.py            # exit 1 when a check fails
    python3 tools/check_rules.py --metrics  # also print size and cost figures

Checks
  links      relative links and #anchors point at real files and headings
  reach      every Markdown page is linked directly from README.md
  structure  category pages open with a breadcrumb; every rule has a
             [H]/[+] tag, a MUST/SHOULD level and a Benefit line
  numbering  the numbered rules in the agent prompt run 1..N without gaps
  sync       the self-check block in the agent prompt equals the one in testing/testing.md
  lint       no framework-specific names outside stacks/ and originals/
  budget     the agent prompt stays within PROMPT_WORD_BUDGET words
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import os
import re
import sys
import time
from pathlib import Path

PROMPT_FILE = "ai-agents/CLAUDE.md"
AGENT_INDEX_FILE = "ai-agents/README.md"
TESTING_FILE = "testing/testing.md"
INDEX_FILE = "README.md"
REQUIRED_FILES = (INDEX_FILE, PROMPT_FILE, AGENT_INDEX_FILE, TESTING_FILE)
PROMPT_WORD_BUDGET = 700
CATEGORY_DIRS = ("general", "architecture", "frontend", "backend", "i18n", "security", "testing", "git")
EXCLUDED_RULE_PAGES = frozenset({"general/proposed-rules.md"})
LINT_EXEMPT_DIRS = frozenset({"stacks", "originals"})
SKIP_DIRS = frozenset({".git", ".github", "tools", "tests", "node_modules", "vendor"})
ALLOW_MARKER = "<!-- lint:allow -->"

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
TAGGED_RULE_RE = re.compile(r"^- `\[(H|\+)\]` \*\*(MUST|SHOULD)\*\* \S")
MALFORMED_RULE_RE = re.compile(r"^- (`\[|\*\*(MUST|SHOULD)\*\*)")
BENEFIT_RE = re.compile(r"^\s+- \*\*Benefit:\*\*")
NUMBERED_RULE_RE = re.compile(r"^(\d+)\. ")
SOURCE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|.*?\]\(([^)\s]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")

# Names and paths that tie a rule to one framework or one project.
BANNED_TERMS = re.compile(
    r"\b(Laravel|Livewire|Blade|Pest|Pint|PHPStan|Larastan|Eloquent|Alpine|Tailwind|DomPDF|"
    r"spatie|Spatie|PHP|Composer|Artisan|ResiCore|IMEXCO|OrganiCore|GreenHumanResource)\b"
    r"|php artisan|vendor/bin|@php|\$fillable|\bDB::|::where|storage/test-reports|resources/"
    r"|app/Services|app/Policies|\.blade\b"
)


@dataclasses.dataclass(frozen=True)
class Finding:
    path: str
    line: int
    check: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: [{self.check}] {self.message}"


@dataclasses.dataclass
class Report:
    findings: list[Finding]
    metrics: dict[str, object]


def iter_lines(text: str):
    """Yield (line_number, line, in_code) for every line; fence markers count as code."""
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            yield number, line, True
            continue
        yield number, line, in_fence


def code_mask(text: str) -> list[bool]:
    return [in_code for _, _, in_code in iter_lines(text)]


def slugify(heading: str) -> str:
    """Approximate GitHub's heading anchor: lower case, punctuation removed, spaces to hyphens."""
    text = heading.strip().lower().replace("`", "")
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def headings_in(text: str) -> list[tuple[int, int, str]]:
    """Return (zero-based line index, heading depth, anchor slug) for each heading outside code."""
    headings: list[tuple[int, int, str]] = []
    seen: dict[str, int] = {}
    mask = code_mask(text)
    for index, line in enumerate(text.splitlines()):
        match = None if mask[index] else HEADING_RE.match(line)
        if not match:
            continue
        base = slugify(match.group(2))
        count = seen.get(base, 0)
        seen[base] = count + 1
        headings.append((index, len(match.group(1)), base if count == 0 else f"{base}-{count}"))
    return headings


def anchors_in(text: str) -> set[str]:
    return {slug for _, _, slug in headings_in(text)}


def section_text(text: str, anchor: str) -> str | None:
    """Return the lines under the heading with this anchor, up to the next heading of the same or higher level."""
    lines = text.splitlines()
    headings = headings_in(text)
    for position, (index, depth, slug) in enumerate(headings):
        if slug != anchor:
            continue
        end = len(lines)
        for next_index, next_depth, _ in headings[position + 1:]:
            if next_depth <= depth:
                end = next_index
                break
        return "\n".join(lines[index:end])
    return None


def numbered_rules(text: str) -> list[tuple[int, int]]:
    """Return (line number, rule number) for each top-level numbered item outside code."""
    return [
        (number, int(match.group(1)))
        for number, line, in_code in iter_lines(text)
        if not in_code and (match := NUMBERED_RULE_RE.match(line))
    ]


def links_in(text: str) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for number, line, in_code in iter_lines(text):
        if in_code:
            continue
        found.extend((number, match.group(1)) for match in LINK_RE.finditer(line))
    return found


def self_check_block(text: str) -> list[str] | None:
    """Return the first ```bash block that follows a heading containing 'self-check'."""
    armed = False
    collected: list[str] | None = None
    for line in text.splitlines():
        if collected is None:
            heading = HEADING_RE.match(line)
            if heading and "self-check" in line.lower():
                armed = True
            elif armed and line.startswith("```bash"):
                collected = []
        elif line.startswith("```"):
            return [entry.rstrip() for entry in collected]
        else:
            collected.append(line.rstrip())
    return None


def markdown_files(root: Path) -> list[Path]:
    found: list[Path] = []
    for directory, subdirs, names in os.walk(root):
        subdirs[:] = sorted(d for d in subdirs if d not in SKIP_DIRS)
        found.extend(Path(directory, name) for name in names if name.endswith(".md"))
    return sorted(found)


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def resolve(base: Path, target: str) -> Path:
    return Path(os.path.normpath(base.parent / target))


class Corpus:
    """Reads each Markdown file once and caches what the checks need."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.files = markdown_files(root)
        self.texts = {path: path.read_text(encoding="utf-8") for path in self.files}
        self._anchors: dict[Path, set[str]] = {}

    def rel(self, path: Path) -> str:
        return relative(self.root, path)

    def anchors(self, path: Path) -> set[str]:
        if path not in self._anchors:
            self._anchors[path] = anchors_in(self.texts[path])
        return self._anchors[path]

    def category_pages(self) -> list[Path]:
        return [
            path for path in self.files
            if self.rel(path).split("/")[0] in CATEGORY_DIRS
            and self.rel(path) not in EXCLUDED_RULE_PAGES
        ]


def check_links(corpus: Corpus) -> list[Finding]:
    findings: list[Finding] = []
    for path in corpus.files:
        for number, target in links_in(corpus.texts[path]):
            if target.startswith(EXTERNAL_PREFIXES):
                continue
            file_part, _, anchor = target.partition("#")
            dest = path if file_part == "" else resolve(path, file_part)
            if file_part and not dest.exists():
                findings.append(Finding(corpus.rel(path), number, "links", f"missing target '{target}'"))
                continue
            if anchor and dest.suffix == ".md" and dest in corpus.texts and anchor not in corpus.anchors(dest):
                findings.append(Finding(corpus.rel(path), number, "links", f"missing anchor '#{anchor}' in {corpus.rel(dest)}"))
    return findings


def check_reach(corpus: Corpus) -> list[Finding]:
    index = corpus.root / INDEX_FILE
    linked = {
        resolve(index, target.partition("#")[0])
        for _, target in links_in(corpus.texts[index])
        if target.partition("#")[0] and not target.startswith(EXTERNAL_PREFIXES)
    }
    return [
        Finding(corpus.rel(path), 1, "reach", "not linked directly from README.md")
        for path in corpus.files
        if path != index and path not in linked
    ]


def check_structure(corpus: Corpus) -> list[Finding]:
    findings: list[Finding] = []
    for path in corpus.category_pages():
        rel = corpus.rel(path)
        text = corpus.texts[path]
        first = next((line for line in text.splitlines() if line.strip()), "")
        if not first.startswith("[Rules index]"):
            findings.append(Finding(rel, 1, "structure", "category page must open with the breadcrumb"))
        lines = text.splitlines()
        mask = code_mask(text)
        for index, line in enumerate(lines):
            if mask[index]:
                continue
            if TAGGED_RULE_RE.match(line):
                if not _has_benefit(lines, index):
                    findings.append(Finding(rel, index + 1, "structure", "rule has no Benefit line"))
            elif MALFORMED_RULE_RE.match(line):
                findings.append(Finding(rel, index + 1, "structure", "rule needs a [H] or [+] tag and a MUST or SHOULD level"))
    return findings


def _has_benefit(lines: list[str], start: int) -> bool:
    for line in lines[start + 1:]:
        if line.strip() and not line.startswith((" ", "\t")):
            return False
        if BENEFIT_RE.match(line):
            return True
    return False


def check_numbering(corpus: Corpus) -> list[Finding]:
    path = corpus.root / PROMPT_FILE
    rel = corpus.rel(path)
    numbers = numbered_rules(corpus.texts[path])
    if not numbers:
        return [Finding(rel, 1, "numbering", "no numbered rules found")]
    findings: list[Finding] = []
    expected = 1
    for number, value in numbers:
        if value != expected:
            findings.append(Finding(rel, number, "numbering", f"expected rule {expected}, found {value}"))
        expected = value + 1
    return findings


def check_sources(corpus: Corpus) -> list[Finding]:
    """Every numbered prompt rule needs a source row that points at a section containing a MUST rule."""
    prompt = corpus.root / PROMPT_FILE
    index = corpus.root / AGENT_INDEX_FILE
    prompt_rel = corpus.rel(prompt)
    index_rel = corpus.rel(index)
    findings: list[Finding] = []
    sources: dict[int, tuple[int, str]] = {}
    for number, line, in_code in iter_lines(corpus.texts[index]):
        match = None if in_code else SOURCE_ROW_RE.match(line)
        if not match:
            continue
        value = int(match.group(1))
        if value in sources:
            findings.append(Finding(index_rel, number, "sources", f"source row {value} is listed twice"))
        sources.setdefault(value, (number, match.group(2)))
    listed = {value for _, value in numbered_rules(corpus.texts[prompt])}
    for number, value in numbered_rules(corpus.texts[prompt]):
        if value not in sources:
            findings.append(Finding(prompt_rel, number, "sources", f"rule {value} has no source row in {AGENT_INDEX_FILE}"))
            continue
        row_line, target = sources[value]
        file_part, _, anchor = target.partition("#")
        dest = resolve(index, file_part)
        if dest not in corpus.texts:
            findings.append(Finding(index_rel, row_line, "sources", f"rule {value} cites missing file '{file_part}'"))
            continue
        section = section_text(corpus.texts[dest], anchor)
        if section is None:
            findings.append(Finding(index_rel, row_line, "sources", f"rule {value} cites missing anchor '#{anchor}'"))
        elif "**MUST**" not in section:
            findings.append(Finding(index_rel, row_line, "sources", f"rule {value} cites a section with no MUST rule"))
    for value, (row_line, _) in sources.items():
        if value not in listed:
            findings.append(Finding(index_rel, row_line, "sources", f"source row {value} matches no numbered rule"))
    return findings


def check_sync(corpus: Corpus) -> list[Finding]:
    prompt = corpus.root / PROMPT_FILE
    testing = corpus.root / TESTING_FILE
    prompt_block = self_check_block(corpus.texts[prompt])
    testing_block = self_check_block(corpus.texts[testing])
    if prompt_block is None:
        return [Finding(corpus.rel(prompt), 1, "sync", "no self-check bash block found")]
    if testing_block is None:
        return [Finding(corpus.rel(testing), 1, "sync", "no self-check bash block found")]
    if prompt_block != testing_block:
        return [Finding(corpus.rel(prompt), 1, "sync", f"self-check block differs from {TESTING_FILE}")]
    return []


def check_lint(corpus: Corpus) -> list[Finding]:
    findings: list[Finding] = []
    for path in corpus.files:
        rel = corpus.rel(path)
        if rel.split("/")[0] in LINT_EXEMPT_DIRS:
            continue
        for number, line, _ in iter_lines(corpus.texts[path]):
            if ALLOW_MARKER in line:
                continue
            match = BANNED_TERMS.search(line)
            if match:
                findings.append(Finding(
                    rel, number, "lint",
                    f"framework-specific term '{match.group(0)}'; make the rule generic or move the example to stacks/",
                ))
    return findings


def check_budget(corpus: Corpus) -> list[Finding]:
    path = corpus.root / PROMPT_FILE
    words = len(corpus.texts[path].split())
    if words > PROMPT_WORD_BUDGET:
        return [Finding(corpus.rel(path), 1, "budget", f"{words} words; the budget is {PROMPT_WORD_BUDGET}")]
    return []


def collect_metrics(corpus: Corpus) -> dict[str, object]:
    per_file = {}
    for path in corpus.files:
        text = corpus.texts[path]
        per_file[corpus.rel(path)] = {
            "words": len(text.split()),
            "lines": text.count("\n") + 1,
            "est_tokens": math.ceil(len(text) / 4),
        }
    prompt = corpus.texts[corpus.root / PROMPT_FILE]
    return {
        "files": per_file,
        "total_words": sum(entry["words"] for entry in per_file.values()),
        "prompt_words": len(prompt.split()),
        "prompt_est_tokens": math.ceil(len(prompt) / 4),
        "framework_term_hits": sum(
            len(BANNED_TERMS.findall(line))
            for path in corpus.files
            if corpus.rel(path).split("/")[0] not in LINT_EXEMPT_DIRS
            for _, line, _ in iter_lines(corpus.texts[path])
            if ALLOW_MARKER not in line
        ),
    }


def check_required(corpus: Corpus) -> list[Finding]:
    return [
        Finding(name, 1, "required", f"core file '{name}' is missing")
        for name in REQUIRED_FILES
        if not (corpus.root / name).is_file()
    ]


CHECKS = (
    check_links,
    check_reach,
    check_structure,
    check_numbering,
    check_sources,
    check_sync,
    check_lint,
    check_budget,
)


def run_checks(root: Path) -> Report:
    started = time.perf_counter()
    corpus = Corpus(root)
    findings = check_required(corpus)
    metrics: dict[str, object] = {}
    if not findings:
        for check in CHECKS:
            findings.extend(check(corpus))
        metrics = collect_metrics(corpus)
    metrics["pages_checked"] = len(corpus.files)
    metrics["seconds"] = round(time.perf_counter() - started, 4)
    return Report(findings=sorted(findings, key=lambda f: (f.path, f.line, f.check)), metrics=metrics)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--metrics", action="store_true", help="print size and cost figures")
    args = parser.parse_args(argv)

    report = run_checks(args.root.resolve())
    for finding in report.findings:
        print(finding)
    if args.metrics and "total_words" in report.metrics:
        metrics = report.metrics
        print("--- metrics")
        print(f"pages checked:        {metrics['pages_checked']}")
        print(f"total words:          {metrics['total_words']}")
        print(f"agent prompt words:   {metrics['prompt_words']} (budget {PROMPT_WORD_BUDGET})")
        print(f"agent prompt tokens:  ~{metrics['prompt_est_tokens']}")
        print(f"framework-term hits:  {metrics['framework_term_hits']}")
        print(f"checker runtime:      {metrics['seconds']} s")
    status = "PASS" if not report.findings else f"FAIL ({len(report.findings)} findings)"
    print(f"static checks: {status}")
    return 1 if report.findings else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
