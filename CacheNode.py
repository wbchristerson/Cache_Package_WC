class CacheNode:
    """Basic node class for use in a doubly linked list"""
    def __init__(self, key, prev = None, next = None):
        self.key = key
        self.prev = prev
        self.next = next

    def remove_node(self):
        """Function to remove a node from a linked list by updating its
            previous and next properties

            Args:
                None

            Returns:
                CacheNode: the newly remove linked list node
        """
        if self.next is not None:
            self.next.prev = self.prev
        if self.prev is not None:
            self.prev.next = self.next
        self.prev = None
        self.next = None
        return self

    def add_node_after(self, other_node):
        """Function to add a node to a linked list

            Args:
                other_node: the node after which to place this instance node
                    which must not be None

            Returns:
                None
        """
        if other_node is None:
            raise ValueError("Node to insert node after is of None type")
        else:
            if other_node.next is not None:
                other_node.next.prev = self
            self.next = other_node.next
            self.prev = other_node
            other_node.next = self
