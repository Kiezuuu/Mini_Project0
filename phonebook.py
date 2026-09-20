from __future__ import annotations
from dataclasses import field

from constants import UPDATE_FIELDS
from contact import Contact, validate_contact


class Node:
    """Store one Contact and a reference to the next node."""

    def __init__(
        self,
        contact: Contact,
        next_node: Node | None = None,
    ) -> None:
        """Initialize one linked-list node."""
        self.contact = contact
        self.next = next_node


class Phonebook:
    """Manage contacts through a manually implemented singly linked list."""

    def __init__(self) -> None:
        """Create an empty phonebook with head = None and size = 0."""
        self.head: Node | None = None
        self.size = 0

    def _find_node_by_id(self, student_id: str) -> Node | None:
        """Return the node containing student_id, or None when not found."""
        current = self.head

        while current is not None:
            if current.contact.student_id == student_id:
                return current

            current = current.next

        return None

    def _student_id_exists(
        self,
        student_id: str,
        excluded_student_id: str | None = None,
    ) -> bool:
        """Return True when another contact already uses student_id."""
        current = self.head

        while current is not None:
            current_id = current.contact.student_id

            if (
                current_id == student_id
                and current_id != excluded_student_id
            ):
                return True

            current = current.next

        return False

    def _phone_exists(
        self,
        phone_number: str,
        excluded_student_id: str | None = None,
    ) -> bool:
        """Return True when another contact uses phone_number."""
        current = self.head

        while current is not None:
            current_contact = current.contact

            if (
                current_contact.phone_number() == phone_number
                and current_contact.student_id != excluded_student_id
            ):
                return True

            current = current.next

        return False

    def _insert_node_sorted(self, node: Node) -> None:
        """Insert node into its correct linked-list position."""
        if self.head is None:
            self.head = node
            node.next = None
            self.size += 1
            return

        if node.contact.sort_key() < self.head.contact.sort_key():
            node.next = self.head
            self.head = node
            self.size += 1
            return

        current = self.head

        while (
            current.next is not None
            and current.next.contact.sort_key()
            <= node.contact.sort_key()
        ):
            current = current.next

        node.next = current.next
        current.next = node
        self.size += 1

    def _detach_node(self, student_id: str) -> Node | None:
        """Unlink and return one node."""
        if self.head is None:
            return None

        if self.head.contact.student_id == student_id:
            removed = self.head
            self.head = self.head.next
            removed.next = None
            self.size -= 1
            return removed

        previous = self.head
        current = self.head.next

        while current is not None:
            if current.contact.student_id == student_id:
                previous.next = current.next
                current.next = None
                self.size -= 1
                return current

            previous = current
            current = current.next

        return None

    def add_contact(self, contact: Contact) -> str:
        """Add one validated Contact and return the exact ADD result line."""

        error = validate_contact(contact)

        if error is not None:
            return error

        if self._student_id_exists(contact.student_id):
            return f"ERROR DUPLICATE_ID {contact.student_id}"

        if self._phone_exists(contact.phone_number()):
            return f"ERROR DUPLICATE_PHONE {contact.phone_number()}"

        node = Node(contact)
        self._insert_node_sorted(node)

        return f"OK ADD {contact.student_id}"

    def find_contact(self, student_id: str) -> str:
        """Return the exact FOUND or NOT_FOUND output."""
        node = self._find_node_by_id(student_id)

        if node is None:
            return f"ERROR NOT_FOUND {student_id}"

        return f"FOUND | {node.contact}"

    def find_by_surname(self, surname: str) -> str:
        """Return MATCHES and CONTACT lines in linked-list order."""
        matches = 0
        current = self.head

        while current is not None:
            if current.contact.surname.casefold() == surname.casefold():
                matches += 1

            current = current.next

        lines = [f"MATCHES {matches}"]

        current = self.head

        while current is not None:
            if current.contact.surname.casefold() == surname.casefold():
                lines.append(f"CONTACT | {current.contact}")

            current = current.next

        return "\n".join(lines)

    def update_contact(
        self,
        target_student_id: str,
        field: str,
        new_value: str,
    ) -> str:
        """Validate and apply one complete contact update."""

        node = self._find_node_by_id(target_student_id)

        if node is None:
            return f"ERROR NOT_FOUND {target_student_id}"

        if field not in UPDATE_FIELDS:
            return f"ERROR INVALID_FIELD {field}"

        old_value = node.contact.get_field(field)

        proposed = node.contact.copy_with_update(
            field,
            new_value,
        )

        validation_error = validate_contact(proposed)

        if validation_error is not None:
            return validation_error

        if (
            field == "ID"
            and self._student_id_exists(
                proposed.student_id,
                excluded_student_id=target_student_id,
            )
        ):
            return f"ERROR DUPLICATE_ID {proposed.student_id}"

        if self._phone_exists(
            proposed.phone_number(),
            excluded_student_id=target_student_id,
        ):
            return f"ERROR DUPLICATE_PHONE {proposed.phone_number()}"

        # Save the old student ID because the target node may receive
        # a new ID during this update.
        if field in {"ID", "SURNAME", "GIVEN_NAME"}:
            removed = self._detach_node(target_student_id)

            if removed is None:
                return f"ERROR NOT_FOUND {target_student_id}"

            removed.contact = proposed
            self._insert_node_sorted(removed)

        else:
            node.contact = proposed

        return (
            f"OK UPDATE {field} | "
            f"{old_value} -> {new_value}"
        )

    def delete_contact(self, student_id: str) -> str:
        """Delete one contact and return the exact DELETE result line."""
        removed = self._detach_node(student_id)

        if removed is None:
            return f"ERROR NOT_FOUND {student_id}"

        return f"OK DELETE {student_id}"

    def list_contacts(self) -> str:
        """Return LIST followed by CONTACT lines."""
        lines = [f"LIST {self.size}"]

        current = self.head

        while current is not None:
            lines.append(f"CONTACT | {current.contact}")
            current = current.next

        return "\n".join(lines)

    def filter_by_country(self, country_codes: set[str]) -> str:
        """Return COUNTRY_MATCHES and matching contacts in list order."""
        matches = 0
        current = self.head

        while current is not None:
            if current.contact.country_code in country_codes:
                matches += 1

            current = current.next

        lines = [f"COUNTRY_MATCHES {matches}"]

        current = self.head

        while current is not None:
            if current.contact.country_code in country_codes:
                lines.append(f"CONTACT | {current.contact}")

            current = current.next

        return "\n".join(lines)