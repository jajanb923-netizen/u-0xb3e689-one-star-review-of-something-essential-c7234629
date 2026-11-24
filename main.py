#!/usr/bin/env python3
"""One-star review of something essential (make.fun).

Writes a single deadpan one-star review to /output/entry.txt.
Python 3.13 standard library only. Deterministic, no network.
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 160


def review_text():
    """The chosen review (candidate #7, polished): a deadpan complaint
    against sleep, the everyday essential that takes eight hours and
    hands back a sore neck and the feeling you forgot something."""
    return (
        "Sleep: I give it eight hours and it gives me back a sore neck "
        "and the feeling I forgot something. "
        "The worst trade I make every single day."
    )


def gate_errors(text):
    """Return the list of gate violations (empty when the entry is valid)."""
    if not isinstance(text, str):
        return ["entry must be text"]
    errors = []
    if not 1 <= len(text) <= MAX_CHARS:
        errors.append(f"entry is {len(text)} chars, must be 1-{MAX_CHARS}")
    if "\n" in text or "\r" in text:
        errors.append("entry must be a single line")
    if not text.strip():
        errors.append("entry must not be only whitespace")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        errors.append("entry must be UTF-8 text")
    return errors


def write_entry(out_dir):
    """Write the review, then verify what actually landed on disk."""
    text = review_text()
    errors = gate_errors(text)
    if errors:
        raise ValueError("; ".join(errors))
    path = Path(out_dir) / "entry.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")
    written = path.read_text(encoding="utf-8")
    errors = gate_errors(written)
    if errors:
        raise ValueError("written entry failed the gate: " + "; ".join(errors))
    if written != text:
        raise ValueError("written entry differs from the review")
    return path, len(written)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path, size = write_entry(out_dir)
    print(f"wrote {path} ({size} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
