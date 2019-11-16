class CacheNode:
    def __init__(self, key, prev = None, next = None):
        self.key = key
        self.prev = prev
        self.next = next

    def remove_node(self):
        if not (self.next is None):
            self.next.prev = self.prev
        if not (self.prev is None):
            self.prev.next = self.next
        self.prev = None
        self.next = None
