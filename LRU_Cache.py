from Cache import Cache
from LRUNode import LRUNode

class LRUCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.head = LRUNode(0, 0)
        self.tail = LRUNode(0, 0)
        self.tail.add_node_after(self.head)
