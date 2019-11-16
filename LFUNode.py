from LRU_Cache import LRUCache

class LFUNode(CacheNode):
    def __init__(self, key, prev = None, next = None):
        super().__init__(key, prev, next)
        self.frequency_cache = LRUCache()

    def __repr__(self):
        return f"(key: {self.key})"
