class LRUNode(CacheNode):
    def __init__(self, key, value, prev = None, next = None):
        super().__init__(key, prev, next)
        self.value = value

    def __repr__(self):
        return f"(key: {self.key}, value: {self.value})"
