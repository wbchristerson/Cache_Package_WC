from SubLRUCache import SubLRUCache
from CacheNode import CacheNode

class LFUNode(CacheNode):
    def __init__(self, key, capacity, prev = None, next = None):
        super().__init__(key, prev, next)
        self.frequency_cache = SubLRUCache(capacity, key)

    def __repr__(self):
        res = "Frequency: " + str(self.key) + "\n"
        res += "Sub LRU Cache:\n"
        res += str(self.frequency_cache)
        return res
