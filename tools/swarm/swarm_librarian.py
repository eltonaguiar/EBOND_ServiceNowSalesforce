#!/usr/bin/env python3
"""swarm_librarian.py — tooling for the Swarm / Isolated-Worktree Framework.

Subcommands:
  scaffold   Create a dated SWARM folder structure (idempotent). Domains are
             generic: pass --domains or --domains-file; CROSSCUTTING is always
             appended as the sanctioned escape hatch.
  collect    Harvest .md (and small .json evidence) from one or more agent
             worktrees into a SWARM subfolder. Never overwrites; suffixed
             copies on collision.
  index      Write INDEX.md listing every artifact in a SWARM folder.
  validate   Structural + contract lint for a SWARM folder: required folders,
             the five canonical final files, front-matter on completed
             deliverables, evidence tokens in review files, stray files.

Stdlib only. No git mutations: 'collect' copies files, it does not cherry-pick;
cherry-picking across repos stays a deliberate human/librarian action.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DOMAINS = ["DB", "GHACTIONS", "AUDIT", "PREDICTION"]
REQUIRED_REVIEW4 = ["PLAN.md", "TESTING_PLAN.md", "IMPLEMENTATION_STEPS.md", "FILES_TO_TOUCH.md", "EVIDENCE_INDEX.md"]
PHASE_DIRS = ["01_TODO", "02_IN_PROGRESS", "03_DONE", "04_final_review", "05_final_reviewv2", "06_final_review3", "07_final_review4", "99_archive"]
ALLOWED_TOP_EXTRA = {"README.md", "HANDOFF.md", "00_CHARTER.md", "INDEX.md", "templates", "tools", "swarm_domains.txt", "evidence"}

# V8: conflict markers. V9: secret-like strings. Both are hard errors.
CONFLICT_MARKER_RE = re.compile(r"^(<{7}|={7}|>{7})", re.MULTILINE)
SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private-key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "aws-key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}"), "sk-token"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "github-token"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"), "slack-token"),
    (re.compile(r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*\S{8,}"), "assigned-secret"),
]
# V4: path-like evidence tokens, resolved relative to the source repo (optional).
PATH_TOKEN_RE = re.compile(r"(?<![\w/:])([\w./-]+\.(?:py|md|json|ya?ml|html|sql|tsv|js))(?::\d+)?\b")
SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", ".next", "dist", "build"}
DEFAULT_MAX_JSON_BYTES = 256 * 1024  # evidence files only; bigger JSON stays out

# Evidence token: repo-relative path, URL, 7+ hex SHA, or file:line. Light lint, not proof.
EVIDENCE_RE = re.compile(r"(https?://|[\w./-]+\.(py|md|json|ya?ml|html|sql|tsv)\b|[0-9a-f]{7,40}\b|\w+\.py:\d+)")


def _dated_dir(root: Path, date: str) -> Path:
    return root / f"{date}-SWARM"


def _resolve_domains(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    """Return (todo_domains, done_domains). CROSSCUTTING is TODO-only."""
    domains: list[str] = []
    if getattr(args, "domains", None):
        domains = [d.strip().upper() for d in args.domains.split(",") if d.strip()]
    elif getattr(args, "domains_file", None):
        df = Path(args.domains_file)
        if not df.is_file():
            raise SystemExit(f"domains file not found: {df}")
        domains = [ln.strip().upper() for ln in df.read_text(encoding="utf-8").splitlines()
                   if ln.strip() and not ln.startswith("#")]
    else:
        domains = list(DEFAULT_DOMAINS)
    seen, todo = set(), []
    for d in domains + ["CROSSCUTTING"]:
        if d not in seen:
            seen.add(d)
            todo.append(d)
    return todo, [d for d in todo if d != "CROSSCUTTING"]


def cmd_scaffold(args: argparse.Namespace) -> int:
    target = _dated_dir(Path(args.root).resolve(), args.date)
    todo_domains, done_domains = _resolve_domains(args)
    dirs = (
        ["01_TODO/" + d for d in todo_domains]
        + ["02_IN_PROGRESS"]
        + ["03_DONE/" + d for d in done_domains]
        + ["evidence/" + d for d in todo_domains]
        + [
            "04_final_review",
            "05_final_reviewv2",
            "06_final_review3",
            "07_final_review4",
            "99_archive",
        ]
    )
    created = 0
    for d in dirs:
        p = target / d
        if not p.exists():
            p.mkdir(parents=True)
            created += 1
        gitkeep = p / ".gitkeep"
        if not any(x for x in p.iterdir() if x.name != ".gitkeep") and not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")
    for fname in ["00_CHARTER.md", "README.md"]:
        p = target / fname
        if not p.exists():
            p.write_text(f"# {fname.replace('.md', '')} — {args.date} SWARM\n", encoding="utf-8")
            created += 1
    df = target / "swarm_domains.txt"
    if not df.exists():
        df.write_text("\n".join(todo_domains) + "\n", encoding="utf-8")
    print(f"scaffold: {target} ({created} new entries, domains={','.join(todo_domains)})")
    return 0


def _iter_artifacts(src: Path, max_json_bytes: int):
    for p in sorted(src.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        if p.suffix.lower() == ".md":
            yield p
        elif p.suffix.lower() == ".json" and p.stat().st_size <= max_json_bytes:
            yield p


def _collision_free(dest_dir: Path, name: str) -> Path:
    cand = dest_dir / name
    if not cand.exists():
        return cand
    stem, suffix = cand.stem, cand.suffix
    i = 2
    while True:
        cand = dest_dir / f"{stem}__{i}{suffix}"
        if not cand.exists():
            return cand
        i += 1


def cmd_collect(args: argparse.Namespace) -> int:
    dest = Path(args.dest).resolve()
    moves = []
    for src_arg in args.src:
        src = Path(src_arg).resolve()
        if not src.is_dir():
            print(f"collect: src not a directory, skipped: {src}", file=sys.stderr)
            continue
        for p in _iter_artifacts(src, args.max_json_bytes):
            rel = p.relative_to(src)
            target = _collision_free(dest, rel.name) if args.flat else dest / rel
            moves.append((p, target))
    for p, target in moves:
        print(f"{'DRY ' if args.dry_run else ''}{p} -> {target}")
    if args.dry_run:
        print(f"collect: dry run, {len(moves)} files")
        return 0
    for p, target in moves:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(p.read_bytes())
    print(f"collect: copied {len(moves)} files into {dest}")
    return 0


def _write_index(root: Path) -> Path:
    rows = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.name == "INDEX.md":
            continue
        if p.suffix.lower() not in (".md", ".json", ".txt", ".tsv"):
            continue
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        st = p.stat()
        rows.append((
            str(p.relative_to(root)),
            f"{st.st_size:,}",
            datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        ))
    lines = [
        f"# INDEX — {root.name}",
        f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} by swarm_librarian.py",
        "",
        "| File | Size (bytes) | Modified |",
        "|------|--------------|----------|",
    ]
    lines += [f"| {r[0]} | {r[1]} | {r[2]} |" for r in rows]
    out = root / "INDEX.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"index: wrote {out} ({len(rows)} artifacts)")
    return out


def cmd_index(args: argparse.Namespace) -> int:
    _write_index(Path(args.dir).resolve())
    return 0


def _has_front_matter(text: str) -> bool:
    if not text.startswith("---\n"):
        return False
    end = text.find("\n---", 4)
    if end == -1:
        return False
    block = text[4:end]
    return "agent:" in block and "domain:" in block


def cmd_validate(args: argparse.Namespace) -> int:
    root = Path(args.dir).resolve()
    if not root.is_dir():
        print(f"validate: not a directory: {root}", file=sys.stderr)
        return 2
    errors: list[str] = []
    warnings: list[str] = []

    for d in PHASE_DIRS:
        if not (root / d).is_dir():
            errors.append(f"missing required phase folder: {d}")

    for entry in sorted(root.iterdir()):
        if entry.name in ALLOWED_TOP_EXTRA or entry.name in PHASE_DIRS:
            continue
        warnings.append(f"stray top-level entry (allowed: {sorted(ALLOWED_TOP_EXTRA | set(PHASE_DIRS))}): {entry.name}")

    r4 = root / "07_final_review4"
    if r4.is_dir():
        present = [f for f in REQUIRED_REVIEW4 if (r4 / f).is_file()]
        if any(not n.startswith(".") for n in (x.name for x in r4.iterdir())) and len(present) < len(REQUIRED_REVIEW4):
            missing = [f for f in REQUIRED_REVIEW4 if not (r4 / f).is_file()]
            errors.append(f"07_final_review4 phase started but canonical files missing: {missing}")

    done = root / "03_DONE"
    if done.is_dir():
        allowed_domains = None
        df = root / "swarm_domains.txt"
        if df.is_file():
            allowed_domains = {ln.strip().upper() for ln in df.read_text(encoding="utf-8").splitlines() if ln.strip()} - {"CROSSCUTTING"}
        for sub in sorted(done.iterdir()):
            if not sub.is_dir() or sub.name.startswith("."):
                continue
            if allowed_domains is not None and sub.name.upper() not in allowed_domains:
                warnings.append(f"03_DONE/{sub.name} is not in swarm_domains.txt — undeclared domain")
            for f in sub.rglob("*.md"):
                if f.name == "INDEX.md":
                    continue
                if not _has_front_matter(f.read_text(encoding="utf-8", errors="replace")):
                    warnings.append(f"no agent/domain front-matter: {f.relative_to(root)}")

    for phase in ("04_final_review", "05_final_reviewv2"):
        ph = root / phase
        if ph.is_dir():
            for f in ph.glob("*.md"):
                if f.name == "README.md":
                    continue
                text = f.read_text(encoding="utf-8", errors="replace")
                if not EVIDENCE_RE.search(text):
                    warnings.append(f"review file has no evidence token (path/URL/SHA): {f.relative_to(root)}")

    # V8 (errors) + V9 (errors): conflict markers and secret-like strings anywhere in the tree.
    # V4 (warnings): path-like evidence tokens resolve against an optional source repo root.
    repo_root = Path(args.repo_root).resolve() if getattr(args, "repo_root", None) else None
    for f in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIR_NAMES for part in f.parts):
            continue
        rel = f.relative_to(root)
        text = f.read_text(encoding="utf-8", errors="replace")
        if CONFLICT_MARKER_RE.search(text):
            errors.append(f"V8 conflict marker present: {rel}")
        for pat, name in SECRET_PATTERNS:
            if pat.search(text):
                errors.append(f"V9 secret-like string ({name}): {rel}")
        if repo_root is not None and repo_root.is_dir():
            for m in PATH_TOKEN_RE.finditer(text):
                tok = m.group(1)
                if tok.startswith(("http", "inbox", "templates")) or "/" not in tok:
                    continue
                if not (repo_root / tok).exists():
                    warnings.append(f"V4 evidence path not found under repo root: {tok} (in {rel})")

    for e in errors:
        print(f"ERROR   {e}")
    for w in warnings:
        print(f"WARN    {w}")
    print(f"validate: {len(errors)} error(s), {len(warnings)} warning(s) in {root.name}")
    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("scaffold", help="create dated SWARM folder structure")
    sp.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    sp.add_argument("--root", default=".")
    sp.add_argument("--domains", help="comma-separated domain list, e.g. DB,GHACTIONS,AUDIT,FRONTEND,SECURITY")
    sp.add_argument("--domains-file", help="text file, one domain per line (overridden by --domains)")
    sp.set_defaults(fn=cmd_scaffold)

    cp = sub.add_parser("collect", help="copy .md + small .json evidence out of worktree(s)")
    cp.add_argument("--src", required=True, nargs="+", help="agent worktree path(s)")
    cp.add_argument("--dest", required=True, help="SWARM subfolder, e.g. 2026-11-16-SWARM/03_DONE/DB")
    cp.add_argument("--flat", action="store_true", help="flatten paths (rename on collision) instead of preserving tree")
    cp.add_argument("--max-json-bytes", type=int, default=DEFAULT_MAX_JSON_BYTES)
    cp.add_argument("--dry-run", action="store_true")
    cp.add_argument("--auto-index", metavar="SWARM_DIR", help="rewrite INDEX.md of this SWARM dir after collecting")
    cp.set_defaults(fn=lambda a: cmd_collect(a) or (_write_index(Path(a.auto_index).resolve()) and 0 if a.auto_index else 0))

    ip = sub.add_parser("index", help="write INDEX.md for a SWARM folder")
    ip.add_argument("--dir", required=True)
    ip.set_defaults(fn=cmd_index)

    vp = sub.add_parser("validate", help="lint a SWARM folder against the structural contract")
    vp.add_argument("--dir", required=True)
    vp.add_argument("--strict", action="store_true", help="treat warnings as failures")
    vp.add_argument("--repo-root", help="source repo root; enables V4 evidence-path resolution")
    vp.set_defaults(fn=cmd_validate)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
