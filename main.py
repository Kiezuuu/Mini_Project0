from __future__ import annotations

import sys

from constants import COUNTRY_CODES
from contact import Contact, validate_contact
from phonebook import Phonebook


def is_canonical_count(value: str) -> bool:
    """Return True for 0 or a nonzero decimal without signs/leading zeros."""
    if value == "0":
        return True

    if not value:
        return False

    if not value.isdigit():
        return False

    return value[0] != "0"


def process_input_line(phonebook: Phonebook, line: str) -> str:
    """Process one phonebook input line and return its exact output."""

    if line == "":
        return "ERROR MALFORMED"

    parts = line.split("|")
    command = parts[0]

    # ---------------------------------------------------------
    # ADD
    # ---------------------------------------------------------
    if command == "ADD":
        if len(parts) != 8:
            return "ERROR MALFORMED ADD"

        contact = Contact(
            parts[1],
            parts[2],
            parts[3],
            parts[4],
            parts[5],
            parts[6],
            parts[7],
        )

        return phonebook.add_contact(contact)

    # ---------------------------------------------------------
    # FIND
    # ---------------------------------------------------------
    if command == "FIND":
        if len(parts) != 2:
            return "ERROR MALFORMED FIND"

        return phonebook.find_contact(parts[1])

    # ---------------------------------------------------------
    # FIND_SURNAME
    # ---------------------------------------------------------
    if command == "FIND_SURNAME":
        if len(parts) != 2:
            return "ERROR MALFORMED FIND_SURNAME"

        return phonebook.find_by_surname(parts[1])

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------
    if command == "UPDATE":
        if len(parts) != 4:
            return "ERROR MALFORMED UPDATE"

        target_student_id = parts[1]

        # The specification requires finding the target first.
        if phonebook._find_node_by_id(target_student_id) is None:
            return f"ERROR NOT_FOUND {target_student_id}"

        return phonebook.update_contact(
            target_student_id,
            parts[2],
            parts[3],
        )

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    if command == "DELETE":
        if len(parts) != 2:
            return "ERROR MALFORMED DELETE"

        return phonebook.delete_contact(parts[1])

    # ---------------------------------------------------------
    # LIST
    # ---------------------------------------------------------
    if command == "LIST":
        if len(parts) != 1:
            return "ERROR MALFORMED LIST"

        return phonebook.list_contacts()

    # ---------------------------------------------------------
    # COUNTRY
    # ---------------------------------------------------------
    if command == "COUNTRY":
        if len(parts) != 2:
            return "ERROR MALFORMED COUNTRY"

        raw_codes = parts[1]

        if not raw_codes:
            return "ERROR INVALID_VALUE COUNTRY_CODES"

        code_parts = raw_codes.split(",")

        if any(code == "" for code in code_parts):
            return "ERROR INVALID_VALUE COUNTRY_CODES"

        requested_codes: set[str] = set()

        for code in code_parts:
            if code not in COUNTRY_CODES:
                return f"ERROR INVALID_COUNTRY {code}"

            requested_codes.add(code)

        return phonebook.filter_by_country(requested_codes)

    return f"ERROR UNKNOWN_COMMAND {command}"


def run_program(raw_input: str) -> str:
    """Process one complete ASEAN-PHONEBOOK 1.0 input."""

    lines = raw_input.splitlines()

    if not lines:
        return "ERROR MALFORMED"

    # Version line
    if lines[0] != "ASEAN-PHONEBOOK 1.0":
        return "ERROR VERSION"

    if len(lines) < 2:
        return "ERROR MALFORMED INPUT_COUNT"

    count_text = lines[1]

    if not is_canonical_count(count_text):
        return "ERROR COMMAND_COUNT"

    input_count = int(count_text)

    # Exactly the requested number of input lines must exist.
    if len(lines) - 2 < input_count:
        return "ERROR COMMAND_COUNT"

    phonebook = Phonebook()
    outputs: list[str] = []

    for index in range(input_count):
        outputs.append(
            process_input_line(
                phonebook,
                lines[index + 2],
            )
        )

    return "\n".join(outputs)


def main() -> None:
    """Read standard input, run the phonebook program, and print its output."""
    output = run_program(sys.stdin.read())

    if output:
        print(output)


if __name__ == "__main__":
    main()