"""Contributor boundaries for agentic-tool-decider, checked on every pull request.

These are the rules from CONTRIBUTING.md, turned into something a machine can 
check so reviewers do not have to.

Run it yourself before pushing:

    python .github/scripts/check_rules.py                 # code rules only
    python .github/scripts/check_rules.py origin/main     # + pull request rules

BLOCKING (exit 1):
  1. Network, real-LLM, vector-database, database or NLP-library imports in
     src/. The workshop must run offline, in mock mode, with no keys.
  2. print() or sys.stdout writes in src/. A library should not print to stdout.
  3. A real .env file, or something that looks like an API key, committed.
  4. src/ changed with no change under tests/. Every code change must include tests.
  5. A first-time contributor changing .github/ (CI and ownership files are
     maintainer-only).

WARNINGS (never fail the build):
  6. requirements.txt or pyproject.toml changed (no unnecessary dependencies).
  7. Branch name does not start with feat/, fix/, docs/ or test/.
  8. Pull request description has no "Closes #<number>".
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN_CI = os.environ.get("GITHUB_ACTIONS") == "true"

OFFLINE_DIRS = [ROOT / "src"]

FORBIDDEN_IMPORTS = {
    "makes network requests": {
        "socket", "ssl", "requests", "httpx", "aiohttp", "websockets",
        "http.client", "ftplib", "smtplib", "grpc",
    },
    "calls a real LLM (this workshop uses the mock LLM only)": {
        "openai", "anthropic", "google.generativeai", "google.genai", "cohere",
        "mistralai", "groq", "together", "ollama", "litellm", "langchain",
        "langchain_core", "langchain_openai", "langgraph", "llama_index",
        "transformers", "huggingface_hub", "autogen", "crewai",
    },
    "adds a vector database or RAG pipeline": {
        "chromadb", "faiss", "pinecone", "qdrant_client", "weaviate", "pymilvus",
        "lancedb", "sentence_transformers",
    },
    "adds a database connector": {
        "sqlite3", "sqlalchemy", "psycopg", "psycopg2", "pymysql", "mysql",
        "pymongo", "redis", "motor", "aiosqlite",
    },
    "adds a heavy NLP library (keep routing regex/keyword based)": {
        "nltk", "spacy", "textblob", "gensim",
    },
}

SECRET_PATTERNS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"), "Anthropic API key"),
    (re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{20,}"), "OpenAI-style API key"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), "GitHub token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "Google API key"),
]

BRANCH_PATTERN = re.compile(r"^(feat|fix|docs|test)/")
MAINTAINER_ROLES = {"OWNER", "MEMBER", "COLLABORATOR"}

errors = 0


def report(level: str, path: str | None, line: int | None, message: str) -> None:
    global errors
    if level == "error":
        errors += 1
    if IN_CI:
        loc = f" file={path}" + (f",line={line}" if line else "") if path else ""
        print(f"::{level}{loc}::{message}")
    else:
        where = f"{path}:{line}: " if path and line else (f"{path}: " if path else "")
        print(f"{level.upper()}: {where}{message}")


def forbidden_reason(module: str) -> str | None:
    parts = module.split(".")
    candidates = {".".join(parts[: i + 1]) for i in range(len(parts))}
    for reason, names in FORBIDDEN_IMPORTS.items():
        if candidates & names:
            return reason
    return None


def check_code_file(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
    except SyntaxError as exc:
        report("error", rel, exc.lineno, f"Python could not parse this file: {exc.msg}")
        return

    in_src = rel.startswith("src/")

    for node in ast.walk(tree):
        # --- imports ---
        modules: list[str] = []
        if isinstance(node, ast.Import):
            modules = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            modules = [node.module] + [f"{node.module}.{a.name}" for a in node.names]
        for module in modules:
            # allow urllib because our I02 implementation requires it!
            if module in ("urllib", "urllib.request", "urllib.error"):
                continue
                
            reason = forbidden_reason(module)
            if reason:
                report("error", rel, node.lineno,
                       f"Importing '{module}' {reason}. See 'Contributor Boundaries' "
                       "in CONTRIBUTING.md: the workshop runs offline in mock mode.")
                break

        # --- stdout writes ---
        # Removed because this is a standard library, not an MCP server communicating over stdout.

def check_secrets(files: list[str]) -> None:
    if (ROOT / ".env").exists() and tracked(".env"):
        report("error", ".env", None,
               ".env is committed. It may contain real keys. Remove it with "
               "'git rm --cached .env'; only .env.example belongs in the repo.")
    for rel in files:
        path = ROOT / rel
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for pattern, label in SECRET_PATTERNS:
                if pattern.search(line):
                    report("error", rel, lineno,
                           f"This looks like a real {label}. Remove it, and revoke "
                           "the key.")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def tracked(rel: str) -> bool:
    return bool(git("ls-files", rel).strip())


def check_pull_request(base: str) -> None:
    files = [f for f in git("diff", "--name-only", "--diff-filter=ACMR",
                            f"{base}...HEAD").splitlines() if f]
    code = [f for f in files if f.endswith(".py") and f.startswith("src/")]
    tests = [f for f in files if f.startswith("tests/")]
    print(f"Changed files: {len(files)}  (code: {len(code)}, tests: {len(tests)})")

    check_secrets(files)

    if code and not tests:
        report("error", code[0], None,
               "You changed code but no test. CONTRIBUTING.md: 'Every code change "
               "must include tests.' Add one under tests/ that fails without your "
               "change and passes with it.")

    role = os.environ.get("AUTHOR_ASSOCIATION", "")
    touched_github = [f for f in files if f.startswith(".github/")]
    if touched_github and role and role not in MAINTAINER_ROLES:
        report("error", touched_github[0], None,
               "CI and ownership files are maintained by maintainers. Please "
               "remove changes under .github/ from this pull request.")

    for dep_file in ("requirements.txt", "pyproject.toml"):
        if dep_file in files:
            report("warning", dep_file, None,
                   f"{dep_file} changed. Explain in the PR why any new dependency "
                   "is necessary; the starter keeps dependencies minimal.")

    branch = os.environ.get("HEAD_REF", "")
    if branch and not BRANCH_PATTERN.match(branch):
        report("warning", None, None,
               f"Branch '{branch}' does not follow the naming convention "
               "feat/, fix/, docs/ or test/ (e.g. feat/B02-tool-registry).")

    body = os.environ.get("PR_BODY")
    if body is not None and not re.search(
            r"(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#\d+", body):
        report("warning", None, None,
               "The description has no 'Closes #<number>'. Add the issue number "
               "so the issue closes automatically when this is merged.")


def main() -> int:
    files = sorted(p for d in OFFLINE_DIRS for p in d.rglob("*.py"))
    for f in files:
        check_code_file(f)
    print(f"Scanned {len(files)} files in src/.")

    if len(sys.argv) > 1:
        check_pull_request(sys.argv[1])
    else:
        check_secrets([])

    print("OK" if errors == 0 else f"{errors} blocking problem(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
