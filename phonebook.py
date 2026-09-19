from __future__ import annotations

from constants import UPDATE_FIELDS
from contact import Contact, validate_contact


class Node:
    """Store one Contact and a reference to the next node."""

    def __init__(self, contact: Contact, next_node: Node | None = None) -> None:
        """Initialize one linked-list node."""
        pass


class Phonebook:
    """Manage contacts through a manually implemented singly linked list."""

    def __init__(self) -> None:
        """Create an empty phonebook with head = None and size = 0."""
        pass

    def _find_node_by_id(self, student_id: str) -> Node | None:
        """Return the node containing student_id, or None when not found."""
        pass

    def _student_id_exists(
        self,
        student_id: str,
        excluded_student_id: str | None = None,
    ) -> bool:
        """Return True when another contact already uses student_id.

        excluded_student_id is useful during UPDATE because the contact being
        changed is allowed to keep its own current ID.
        """
        pass

    def _phone_exists(
        self,
        phone_number: str,
        excluded_student_id: str | None = None,
    ) -> bool:
        """Return True when another contact already uses phone_number."""
        pass

    def _insert_node_sorted(self, node: Node) -> None:
        """Insert node into its correct linked-list position.

        Correctly handle an empty list, insertion before head, insertion in
        the middle, and insertion at the end. Update size exactly once.
        Do not use sort() or sorted().
        """
        pass

    def _detach_node(self, student_id: str) -> Node | None:
        """Unlink and return one node, or return None when it is missing.

        Correctly handle removing the only node, head, middle, and tail.
        Update size exactly once when a node is removed.
        """
        pass

    def add_contact(self, contact: Contact) -> str:
        """Add one validated Contact and return the exact ADD result line.

        Check duplicate student ID before duplicate complete phone number.
        """
        pass

    def find_contact(self, student_id: str) -> str:
        """Return the exact FOUND or NOT_FOUND output for student_id."""
        pass

    def find_by_surname(self, surname: str) -> str:
        """Return MATCHES and CONTACT lines in current linked-list order."""
        pass

    def update_contact(
        self,
        target_student_id: str,
        field: str,
        new_value: str,
    ) -> str:
        """Validate and apply one complete contact update.

        A failed update must leave the original Contact and linked list
        unchanged. ID, SURNAME, and GIVEN_NAME changes may require the node to
        be detached and reinserted into the correct sorted position.
        """
        pass

    def delete_contact(self, student_id: str) -> str:
        """Delete one contact and return the exact DELETE result line."""
        pass

    def list_contacts(self) -> str:
        """Return LIST followed by CONTACT lines in linked-list order."""
        pass

    def filter_by_country(self, country_codes: set[str]) -> str:
        """Return COUNTRY_MATCHES and matching CONTACT lines in list order."""
        pass
