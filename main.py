from __future__ import annotations

import sys

from constants import COUNTRY_CODES
from contact import Contact, validate_contact
from phonebook import Phonebook


def is_canonical_count(value: str) -> bool:
    """Return True for 0 or a nonzero decimal without signs/leading zeros."""
    pass


def process_input_line(phonebook: Phonebook, line: str) -> str:
    """Process one phonebook input line and return its exact output.

    Check field count before field values. The input processor may parse text,
    validate fields, and call Phonebook methods, but it must not relink nodes
    or directly change Phonebook.head.
    """
    pass


def run_program(raw_input: str) -> str:
    """Process one complete ASEAN-PHONEBOOK 1.0 input.

    Validate the version line and input-count line, process exactly the
    requested input lines, and return all produced output joined by newlines.
    """
    pass


def main() -> None:
    """Read standard input, run the phonebook program, and print its output."""
    output = run_program(sys.stdin.read())
    if output:
        print(output)


if __name__ == "__main__":
    main()
