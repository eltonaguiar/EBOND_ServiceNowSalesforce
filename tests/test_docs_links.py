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
