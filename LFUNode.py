from LRU_Cache import LRUCache
from CacheNode import CacheNode

class LFUNode(CacheNode):
    def __init__(self, key, capacity, prev = None, next = None):
        super().__init__(key, prev, next)
        self.frequency_cache = LRUCache(capacity)

    def __repr__(self):
        return f"(key: {self.key})"
