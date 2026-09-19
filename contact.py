from __future__ import annotations

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
        pass

    def phone_number(self) -> str:
        """Return the complete phone number as code-area-local."""
        pass

    def sort_key(self) -> tuple[str, str, str]:
        """Return the surname, given-name, and student-ID sorting key.

        Name comparison must ignore capitalization, but the original stored
        spelling must remain unchanged.
        """
        pass

    def get_field(self, field: str) -> str:
        """Return the current value of one supported UPDATE field."""
        pass

    def copy_with_update(self, field: str, new_value: str) -> Contact:
        """Return a proposed Contact containing one field change.

        Do not modify the current Contact. The proposed Contact is checked
        first so a failed UPDATE can leave the linked list unchanged.
        """
        pass

    def __str__(self) -> str:
        """Return the exact readable contact format required by the project."""
        pass


def is_valid_student_id(value: str) -> bool:
    """Return True when value follows the published student-ID rules."""
    pass


def is_valid_name(value: str) -> bool:
    """Return True when value is a valid surname or given name."""
    pass


def is_valid_occupation(value: str) -> bool:
    """Return True when value follows the published occupation rules."""
    pass


def is_valid_area_code(value: str) -> bool:
    """Return True for an area code containing 1 to 6 digits."""
    pass


def is_valid_local_number(value: str) -> bool:
    """Return True for a local number containing 3 to 12 digits."""
    pass


def validate_contact(contact: Contact) -> str | None:
    """Return the first required validation error, or None when valid.

    Check fields from left to right using the order published in the project
    definition. COUNTRY_CODE uses ERROR INVALID_COUNTRY <value>.
    """
    pass
