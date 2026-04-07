"""Decorators for tagging section functions with review metadata."""

from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)


def references_numbers(func: F) -> F:
    """Tag a section function as containing hardcoded numbers from data."""
    func._references_numbers = True  # type: ignore[attr-defined]
    return func


def interpretation(func: F) -> F:
    """Tag a section function as containing a subjective claim."""
    func._interpretation = True  # type: ignore[attr-defined]
    return func
