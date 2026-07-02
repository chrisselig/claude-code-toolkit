"""Structural lint for the toolkit's skill, command, and docs files.

Enforces the house format described in CLAUDE.md and docs/writing-your-own.md:
valid frontmatter, names matching paths, a Steps section, and the rule that
every skill/command has a docs mirror wired into the MkDocs nav.
"""

from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent

SKILL_FILES = sorted(REPO.glob("skills/*/SKILL.md"))
COMMAND_FILES = sorted(REPO.glob("commands/*.md"))
ALL_SOURCE = SKILL_FILES + COMMAND_FILES

DOCS_SKILL_PAGES = sorted(
    p for p in REPO.glob("docs/skills/*.md") if p.name != "index.md"
)
DOCS_COMMAND_PAGES = sorted(
    p for p in REPO.glob("docs/commands/*.md") if p.name != "index.md"
)


def _ident(path: Path) -> str:
    """A skill's identity is its directory name; a command's is its file stem."""
    return path.parent.name if path.name == "SKILL.md" else path.stem


def _split_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path}: missing frontmatter opening '---'"
    _, fm, body = text.split("---", 2)
    meta = yaml.safe_load(fm)
    assert isinstance(meta, dict), f"{path}: frontmatter is not a YAML mapping"
    return meta, body


def test_toolkit_is_nonempty():
    assert len(SKILL_FILES) >= 17
    assert len(COMMAND_FILES) >= 11


@pytest.mark.parametrize("path", ALL_SOURCE, ids=_ident)
def test_frontmatter(path: Path):
    meta, _ = _split_frontmatter(path)

    assert meta.get("name") == _ident(path), (
        f"{path}: frontmatter name {meta.get('name')!r} != path name {_ident(path)!r}"
    )

    desc = meta.get("description", "")
    assert isinstance(desc, str) and len(desc.strip()) >= 20, (
        f"{path}: description missing or too short"
    )
    assert "Use when" in desc, (
        f"{path}: description needs a 'Use when ...' sentence "
        "— it's how Claude decides to invoke it"
    )

    allowed = {"name", "description", "argument-hint", "allowed-tools", "model"}
    unknown = set(meta) - allowed
    assert not unknown, f"{path}: unknown frontmatter keys {sorted(unknown)}"


@pytest.mark.parametrize("path", ALL_SOURCE, ids=_ident)
def test_body_structure(path: Path):
    _, body = _split_frontmatter(path)
    assert body.lstrip().startswith("# "), (
        f"{path}: body must start with a '# Title' heading"
    )
    assert "## Steps" in body, f"{path}: a '## Steps' section is required"


@pytest.mark.parametrize("path", SKILL_FILES, ids=_ident)
def test_skill_has_docs_mirror(path: Path):
    mirror = REPO / "docs" / "skills" / f"{_ident(path)}.md"
    assert mirror.exists(), f"{path} has no docs mirror at {mirror.relative_to(REPO)}"


@pytest.mark.parametrize("path", COMMAND_FILES, ids=_ident)
def test_command_has_docs_mirror(path: Path):
    mirror = REPO / "docs" / "commands" / f"{_ident(path)}.md"
    assert mirror.exists(), f"{path} has no docs mirror at {mirror.relative_to(REPO)}"


@pytest.mark.parametrize(
    "page",
    DOCS_SKILL_PAGES + DOCS_COMMAND_PAGES,
    ids=lambda p: f"{p.parent.name}/{p.stem}",
)
def test_docs_page_has_source(page: Path):
    """No orphan docs: every docs page corresponds to a real skill or command."""
    if page.parent.name == "skills":
        source = REPO / "skills" / page.stem / "SKILL.md"
    else:
        source = REPO / "commands" / page.name
    assert source.exists(), (
        f"{page.relative_to(REPO)} documents nothing — "
        f"{source.relative_to(REPO)} missing"
    )


@pytest.mark.parametrize(
    "page",
    DOCS_SKILL_PAGES + DOCS_COMMAND_PAGES,
    ids=lambda p: f"{p.parent.name}/{p.stem}",
)
def test_docs_page_in_nav(page: Path):
    nav_text = (REPO / "mkdocs.yml").read_text(encoding="utf-8")
    rel = f"{page.parent.name}/{page.name}"
    assert rel in nav_text, f"{rel} is not listed in the mkdocs.yml nav"


@pytest.mark.parametrize("path", ALL_SOURCE, ids=_ident)
def test_listed_in_readme(path: Path):
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert f"/{_ident(path)}" in readme, (
        f"{path}: /{_ident(path)} missing from the README tables"
    )
