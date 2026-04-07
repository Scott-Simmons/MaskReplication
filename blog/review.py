"""Review-gating system: checks decorated sections against reviewed.json."""

import importlib
import inspect
import json
from pathlib import Path
from typing import Callable

from blog.version import VERSION

REVIEWED_JSON = Path(__file__).resolve().parent.parent / "reviewed.json"

# All section modules to scan
SECTION_MODULE_NAMES = [
    "blog.sections.appendix",
    "blog.sections.dimensions",
    "blog.sections.figures",
    "blog.sections.footnotes",
    "blog.sections.intro",
    "blog.sections.recap",
    "blog.sections.replication",
]


def _is_decorated(func: Callable) -> bool:
    return getattr(func, "_references_numbers", False) or getattr(
        func, "_interpretation", False
    )


def _decorator_names(func: Callable) -> list[str]:
    names = []
    if getattr(func, "_references_numbers", False):
        names.append("references_numbers")
    if getattr(func, "_interpretation", False):
        names.append("interpretation")
    return names


def _qualified_name(module_name: str, func_name: str) -> str:
    """Return short qualified name like 'figures.two_d_space_projection_headline'."""
    short_module = module_name.rsplit(".", 1)[-1]
    return f"{short_module}.{func_name}"


def get_decorated_sections() -> list[tuple[str, Callable, list[str]]]:
    """Return list of (qualified_name, func, decorator_names) for all decorated sections."""
    results = []
    for mod_name in SECTION_MODULE_NAMES:
        mod = importlib.import_module(mod_name)
        for name, obj in inspect.getmembers(mod, inspect.isfunction):
            if name.startswith("_"):
                continue
            if _is_decorated(obj):
                qname = _qualified_name(mod_name, name)
                results.append((qname, obj, _decorator_names(obj)))
    return results


def load_reviewed() -> dict[str, str]:
    if REVIEWED_JSON.exists():
        return json.loads(REVIEWED_JSON.read_text())
    return {}


def save_reviewed(data: dict[str, str]) -> None:
    REVIEWED_JSON.write_text(json.dumps(data, indent=2) + "\n")


def sections_needing_review() -> list[tuple[str, Callable, list[str]]]:
    """Return decorated sections whose reviewed version != current VERSION."""
    reviewed = load_reviewed()
    needs_review = []
    for qname, func, dec_names in get_decorated_sections():
        if reviewed.get(qname) != VERSION:
            needs_review.append((qname, func, dec_names))
    return needs_review


def run_interactive_review() -> None:
    """Walk through each unreviewed section and prompt the user to confirm."""
    needs = sections_needing_review()
    if not needs:
        print(f"All decorated sections are reviewed at version {VERSION}.")
        return

    reviewed = load_reviewed()
    print(f"\n{len(needs)} section(s) need review for version {VERSION}:\n")

    for qname, func, dec_names in needs:
        print("=" * 60)
        print(f"Section: {qname}")
        print(f"Decorators: {', '.join(dec_names)}")
        print("-" * 60)
        try:
            output = func()
            print(output)
        except Exception as e:
            print(f"[Error calling function: {e}]")
        print("-" * 60)
        answer = input(f"Approve '{qname}' for version {VERSION}? [y/n] ").strip().lower()
        if answer == "y":
            reviewed[qname] = VERSION
            save_reviewed(reviewed)
            print(f"  -> Approved.\n")
        else:
            print(f"  -> Skipped.\n")

    remaining = sections_needing_review()
    if remaining:
        print(f"\n{len(remaining)} section(s) still need review.")
    else:
        print(f"\nAll sections approved for version {VERSION}.")


if __name__ == "__main__":
    run_interactive_review()
