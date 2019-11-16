class Cache:
    """Basic cache class for use as super classes of LRU and LFU caches"""
    def __init__(self, capacity = 10):
        self.capacity = capacity
        self.size = 0
        self.key_node_map = dict()

    def is_at_capacity(self):
        return self.size == self.capacity
