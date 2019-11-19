from LRU_Cache import LRUCache

class SubLRUCache(LRUCache):
    def __init__(self, capacity, top_level_frequency):
        super().__init__(capacity)
        self.top_level_frequency = top_level_frequency
