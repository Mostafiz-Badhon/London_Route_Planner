class DoublyLinkedList:
    """
    Doubly Linked List Data Structure

    -- Available Functions --
    It contains the ability to add and remove elements from the front, end and the middle of the list after a given
    element. It can also return the element at the head, length of the Doubly Linked List and whether it's empty or not.
    It can also traverse the list and return a list of all elements in their respective order from the head to tail.

    Reference: COMP1828 - Week 2 Data Structures Lecture
    """
    # ---Nested _Node class---.
    # Lightweight, private class for storing a singly linked list.
    class _Node:
        __slots__ = 'element', 'prev_node', 'next_node'         # Streamline memory.

        def __init__(self, element=None, prev_node=None, next_node=None):      # Initialise the node's fields.
            self.element = element                 # User's elements.
            self.prev_node = prev_node             # Previous node reference.
            self.next_node = next_node             # Next node reference.

    # ---List constructor---
    # Creates an empty list.
    def __init__(self):
        self.head = None
        self.size = 0

    # ---Public accessors---
    # Return the number of elements in the list.
    def __len__(self):
        return self.size

    def get_head(self):
        return self.head.element

    # Return TRUE if the list is empty.
    def is_empty(self):
        return self.size == 0

    # Add the given element onto a node at the head of the list.
    def add_first(self, element):
        # Creates a new node for the element with no next or previous pointers.
        new_node = self._Node(element, None, None)
        # Checks if the head pointer is already pointing to a node and sets the new node there if it isn't.
        if self.head is None:
            self.head = new_node
        else:
            # Places the new node in front of the old 1st node and updates the pointers for both of them.
            new_node.next_node = self.head
            self.head.prev_node = new_node
            self.head = new_node
        self.size += 1

    # Removes the node at the head of the list.
    def remove_first(self):
        old_head = self.head
        if self.head is not None:
            # Sets the head pointer to the next node and updates both the old and new node's pointers.
            self.head = self.head.next_node
            self.head.prev_node = None
            old_head.next_node = None
            self.size -= 1
        else:
            raise ValueError("List is already empty.")

    # Add a node to the tail of the list.
    def add_last(self, element):
        if self.is_empty() is False:
            new_node = self._Node(element, None, None)
            current_node = self.head
            # Goes to the end of the list.
            while current_node.next_node is not None:
                current_node = current_node.next_node
            current_node.next_node = new_node
            new_node.prev_node = current_node
        else:
            self.add_first(element)

    # Remove the node at the tail of the list.
    def remove_last(self):
        # If there is only one node in the list, set the node at the head to null.
        if self.head is not None and self.head.next_node is None:
            self.head = None
            self.size -= 1
        elif self.head is not None:
            current_node = self.head
            prev = current_node
            # Traverses all the way to the end of the list.
            while current_node is not None and current_node.next_node is not None:
                prev = current_node
                current_node = current_node.next_node
            # Remove the last node and update pointers.
            prev.next_node = None
            current_node.prev_node = None
            self.size -= 1
        else:
            raise ValueError("List is already empty.")

    # Insert element into the list after the first occurrence of 'after_element'.
    def insert_mid(self, element, after_element):
        new_node = self._Node(element, None, None)
        current_node = self.head
        if self.head is not None:
            # Searches for the 'after_element' in the list and stops if it reaches the end or has found it.
            while current_node.element != after_element and current_node.next_node is not None:
                current_node = current_node.next_node
        if current_node.element == after_element:
            if current_node.next_node is not None:
                old_next_node = current_node.next_node
                # Updates the pointers on both sides of the inserted node to point to element.
                current_node.next_node = new_node
                old_next_node.prev_node = new_node
                # Sets the inserted node's prev_node and next_node pointers.
                new_node.prev_node = current_node
                new_node.next_node = old_next_node
            # If it's right at the end, the node will just get appended.
            elif current_node.next_node is None:
                current_node.next_node = new_node
                new_node.prev_node = current_node
            self.size += 1
        else:
            raise ValueError(after_element, " not found.")

    # Remove the first node containing the element that's found in the list.
    def remove_mid(self, element):
        if self.head is not None:
            current_node = self.head
            prev = current_node
            # Find the node associated with the element with a pointers pointing to the current and previous node.
            while current_node.element != element and current_node.next_node is not None:
                prev = current_node
                current_node = current_node.next_node
            if current_node.element == element:
                new_next_node = current_node.next_node
                # Checks if it's in the middle of the list and executes the appropriate pointer updates.
                if current_node.prev_node is not None and current_node.next_node is not None:
                    prev.next_node = new_next_node
                    new_next_node.prev_node = prev
                # Checks if it's at the start of the list and executes the appropriate pointer updates.
                elif current_node.prev_node is None and current_node.next_node is not None:
                    self.head = new_next_node
                    prev.next_node = None
                    new_next_node.prev_node = None
                # Checks if it's at the end of the list and executes the appropriate pointer updates.
                elif current_node.prev_node is not None and current_node.next_node is None:
                    prev.next_node = None
            else:
                raise ValueError(element, " not found.")

    # Traverses and returns the elements in the linked list in the form of a list.
    def traverse_all(self):
        current_node = self.head
        items = []
        while current_node is not None:
            items.append(current_node.element)
            current_node = current_node.next_node
        return items
