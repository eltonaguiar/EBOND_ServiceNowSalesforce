import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_relative_markdown_links_resolve():
    broken = []
    for md in [ROOT / "README.md", ROOT / "lab" / "README.md"]:
        text = md.read_text()
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path = (md.parent / target.split("#")[0]).resolve()
            if not path.exists():
                broken.append(f"{md.name} -> {target}")
    assert broken == []


def test_live_validation_status_is_visible():
    readme = (ROOT / "README.md").read_text()
    layout = (ROOT / "site" / "_layouts" / "default.html").read_text()
    assert "## Validation status" in readme
    assert "Live integration validation pending" in readme
    assert "Live integration validation pending" in layout
    assert "FINAL_V6_REVIEW.md" in readme
