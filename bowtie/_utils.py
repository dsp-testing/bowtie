"""
Small, generic helpers shared across Bowtie's modules.
"""
from __future__ import annotations


def pluralize(count: int, noun: str, plural: str | None = None) -> str:
    """
    Combine a count with the singular or plural form of a noun.

    >>> pluralize(1, "test")
    '1 test'
    >>> pluralize(0, "test")
    '0 tests'
    >>> pluralize(2, "test")
    '2 tests'
    >>> pluralize(2, "story", plural="stories")
    '2 stories'
    """
    plural = plural or f"{noun}s"
    word = noun if count == 1 else plural
    return f"{count} {word}"
