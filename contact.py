from __future__ import annotations

import re

from constants import COUNTRY_CODES


class Contact:
    """Represent one contact stored by the ASEAN Phonebook."""

    def __init__(
        self,
        student_id: str,
        surname: str,
        given_name: str,
        occupation: str,
        country_code: str,
        area_code: str,
        local_number: str,
    ) -> None:
        """Store all seven contact fields without changing their text."""
        self.student_id = student_id
        self.surname = surname
        self.given_name = given_name
        self.occupation = occupation
        self.country_code = country_code
        self.area_code = area_code
        self.local_number = local_number

    def phone_number(self) -> str:
        """Return the complete phone number as code-area-local."""
        return (
            f"{self.country_code}-"
            f"{self.area_code}-"
            f"{self.local_number}"
        )

    def sort_key(self) -> tuple[str, str, str]:
        """Return the surname, given-name, and student-ID sorting key."""
        return (
            self.surname.casefold(),
            self.given_name.casefold(),
            self.student_id.casefold(),
        )

    def get_field(self, field: str) -> str:
        """Return the current value of one supported UPDATE field."""
        if field == "ID":
            return self.student_id
        if field == "SURNAME":
            return self.surname
        if field == "GIVEN_NAME":
            return self.given_name
        if field == "OCCUPATION":
            return self.occupation
        if field == "COUNTRY_CODE":
            return self.country_code
        if field == "AREA_CODE":
            return self.area_code
        if field == "LOCAL_NUMBER":
            return self.local_number

        raise ValueError(f"Unsupported field: {field}")

    def copy_with_update(self, field: str, new_value: str) -> Contact:
        """Return a proposed Contact containing one field change."""
        values = {
            "student_id": self.student_id,
            "surname": self.surname,
            "given_name": self.given_name,
            "occupation": self.occupation,
            "country_code": self.country_code,
            "area_code": self.area_code,
            "local_number": self.local_number,
        }

        mapping = {
            "ID": "student_id",
            "SURNAME": "surname",
            "GIVEN_NAME": "given_name",
            "OCCUPATION": "occupation",
            "COUNTRY_CODE": "country_code",
            "AREA_CODE": "area_code",
            "LOCAL_NUMBER": "local_number",
        }

        if field not in mapping:
            raise ValueError(f"Unsupported field: {field}")

        values[mapping[field]] = new_value

        return Contact(**values)

    def __str__(self) -> str:
        """Return the exact readable contact format required."""
        country_name = COUNTRY_CODES.get(
            self.country_code,
            self.country_code,
        )

        return (
            f"{self.student_id} - "
            f"{self.surname}, {self.given_name} - "
            f"{self.occupation} - "
            f"{country_name} - "
            f"{self.phone_number()}"
        )


def is_valid_student_id(value: str) -> bool:
    """Return True when value follows the published student-ID rules."""
    if not value:
        return False

    return re.fullmatch(r"[A-Z0-9]+(?:-[A-Z0-9]+)+", value) is not None


def is_valid_name(value: str) -> bool:
    """Return True when value is a valid surname or given name."""
    if not value:
        return False

    # Allows names such as:
    # Abad
    # Garcia
    # De Leon
    # O'Connor
    # Santos-Reyes
    return (
        re.fullmatch(
            r"[A-Za-z]+(?:[ '-][A-Za-z]+)*",
            value,
        )
        is not None
    )


def is_valid_occupation(value: str) -> bool:
    """Return True when value follows the published occupation rules."""
    if not value:
        return False

    return (
        re.fullmatch(
            r"[A-Za-z0-9]+(?:[ '-][A-Za-z0-9]+)*",
            value,
        )
        is not None
    )


def is_valid_area_code(value: str) -> bool:
    """Return True for an area code containing 1 to 6 digits."""
    return re.fullmatch(r"\d{1,6}", value) is not None


def is_valid_local_number(value: str) -> bool:
    """Return True for a local number containing 3 to 12 digits."""
    return re.fullmatch(r"\d{3,12}", value) is not None


def validate_contact(contact: Contact) -> str | None:
    """Return the first required validation error, or None when valid."""

    if not is_valid_student_id(contact.student_id):
        return "ERROR INVALID_VALUE STUDENT_ID"

    if not is_valid_name(contact.surname):
        return "ERROR INVALID_VALUE SURNAME"

    if not is_valid_name(contact.given_name):
        return "ERROR INVALID_VALUE GIVEN_NAME"

    if not is_valid_occupation(contact.occupation):
        return "ERROR INVALID_VALUE OCCUPATION"

    if contact.country_code not in COUNTRY_CODES:
        return f"ERROR INVALID_COUNTRY {contact.country_code}"

    if not is_valid_area_code(contact.area_code):
        return "ERROR INVALID_VALUE AREA_CODE"

    if not is_valid_local_number(contact.local_number):
        return "ERROR INVALID_VALUE LOCAL_NUMBER"

    return None