"""
Script manager — CRUD operations for the script library.

Scripts are stored as Markdown files under ~/.automate/scripts/<name>.md
"""

from __future__ import annotations

from pathlib import Path

from .script import Script

_DEFAULT_DIR = Path.home() / ".automate" / "scripts"


def _lib_dir() -> Path:
    d = _DEFAULT_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def _path_for(name: str) -> Path:
    safe = name.replace(" ", "_").replace("/", "_")
    return _lib_dir() / f"{safe}.md"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def save(script: Script) -> Path:
    """Persist *script* to the library. Returns the path written."""
    p = _path_for(script.name)
    script.save(p)
    return p


def load(name: str) -> Script:
    """Load a script by name. Raises FileNotFoundError if absent."""
    p = _path_for(name)
    if not p.exists():
        raise FileNotFoundError(f"No script named '{name}' in library ({p})")
    return Script.from_file(p)


def load_all() -> list[Script]:
    """Return all scripts in the library, sorted by name."""
    scripts = []
    for p in sorted(_lib_dir().glob("*.md")):
        try:
            scripts.append(Script.from_file(p))
        except Exception:
            pass
    return scripts


def delete(name: str) -> bool:
    """Delete a script. Returns True if it existed, False otherwise."""
    p = _path_for(name)
    if p.exists():
        p.unlink()
        return True
    return False


def exists(name: str) -> bool:
    return _path_for(name).exists()


def rename(old_name: str, new_name: str) -> Path:
    """Rename a script in the library. Returns the new path."""
    old_path = _path_for(old_name)
    if not old_path.exists():
        raise FileNotFoundError(f"No script named '{old_name}'")
    script = Script.from_file(old_path)
    script.name = new_name
    new_path = _path_for(new_name)
    script.save(new_path)
    old_path.unlink()
    return new_path


def lib_path() -> Path:
    """Return (and ensure) the library directory path."""
    return _lib_dir()
