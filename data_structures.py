from datetime import datetime


class ContactNode:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.is_favorite = False
        self.next = None

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "is_favorite": self.is_favorite
        }


class ContactLinkedList:
    def __init__(self):
        self.head = None

    def add_contact(self, name, phone, email, is_favorite=False):

        # Check for duplicate contact
        curr = self.head

        while curr:
            if (curr.name.lower() == name.lower()
                    and curr.phone == phone
                    and curr.email.lower() == email.lower()):
                return False

            curr = curr.next

        # Create new contact
        new_node = ContactNode(name, phone, email)
        new_node.is_favorite = is_favorite

        # If list is empty
        if self.head is None:
            self.head = new_node
            return True

        # Add contact at the end
        curr = self.head

        while curr.next:
            curr = curr.next

        curr.next = new_node

        return True

    def delete_contact(self, name):
        curr = self.head
        prev = None

        while curr:
            if curr.name.lower() == name.lower():

                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next

                return curr.to_dict()

            prev = curr
            curr = curr.next

        return None

    def toggle_favorite(self, name):
        curr = self.head

        while curr:
            if curr.name.lower() == name.lower():
                curr.is_favorite = not curr.is_favorite
                return

            curr = curr.next

    def get_favorites(self):
        favorites = []
        curr = self.head

        while curr:
            if curr.is_favorite:
                favorites.append(curr.to_dict())

            curr = curr.next

        return favorites

    def to_array(self):
        result = []
        curr = self.head

        while curr:
            result.append(curr.to_dict())
            curr = curr.next

        return result


class UndoStack:
    def __init__(self):
        self.items = []

    def push(self, contact):
        self.items.append(contact)

    def pop(self):
        if self.items:
            return self.items.pop()

        return None

    def get_all(self):
        return list(reversed(self.items))


class CallQueue:
    def __init__(self, capacity=10):
        self.items = []
        self.capacity = capacity

    def enqueue(self, contact):
        call = {
            "name": contact["name"],
            "phone": contact["phone"],
            "time": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
            "type": "Outgoing"
        }

        # Remove oldest call if queue is full
        if len(self.items) >= self.capacity:
            self.items.pop(0)

        self.items.append(call)

    def get_all(self):
        return list(reversed(self.items))

    def clear(self):
        self.items.clear()