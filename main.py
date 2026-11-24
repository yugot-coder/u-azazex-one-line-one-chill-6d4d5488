#!/usr/bin/env python3
"""One Line, One Chill — make.fun entry.

Writes one single-sentence horror line to /output/entry.txt
(or $OUTPUT_DIR/entry.txt). Standard library only; fully deterministic:
the same text every run.

The line is a single sentence of 116 characters, under the 200-character
gate. Its scare is earned, not announced: a man finds his own obituary
already printed, dated tomorrow, with the cause of death in his own
handwriting — a concrete image whose dread outlasts the line, and whose
last word lands the blow.
"""

import os
from pathlib import Path

ENTRY = (
    "I found my own obituary folded in my coat pocket, dated tomorrow, "
    "with the cause of death written in my handwriting.\n"
)

MAX_CHARS = 200


def main() -> None:
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ENTRY, encoding="utf-8")
    # Read-back validation: exactly one non-empty line, within the gate.
    text = target.read_text(encoding="utf-8")
    # The file must round-trip byte-for-byte to the intended entry.
    assert text == ENTRY, "entry.txt does not match the intended entry"
    # Exactly one trailing newline: no missing newline, no blank lines.
    assert text.endswith("\n"), "entry.txt must end with a newline"
    assert not text.endswith("\n\n"), "entry.txt must not end with blank lines"
    line = text[:-1]
    assert line, "entry.txt must not be only whitespace"
    assert "\n" not in line, "entry must be a single line"
    # No leading/trailing whitespace and no control characters in the line.
    assert line == line.strip(), "entry line must not have leading/trailing whitespace"
    assert all(c == " " or c.isprintable() for c in line), (
        "entry line must not contain control characters"
    )
    assert "  " not in line, "entry line must not contain double spaces"
    # Character and byte length both inside the 1-200 gate.
    assert 1 <= len(line) <= MAX_CHARS, (
        f"entry must be 1-{MAX_CHARS} characters, got {len(line)}"
    )
    assert 1 <= len(text.encode("utf-8")) <= MAX_CHARS + 1, (
        f"entry must be 1-{MAX_CHARS + 1} bytes including newline, "
        f"got {len(text.encode('utf-8'))}"
    )


if __name__ == "__main__":
    main()
