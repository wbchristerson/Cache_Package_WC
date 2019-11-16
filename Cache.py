class Cache:
    """Basic cache class for use as super classes of LRU and LFU caches"""
    def __init__(self, capacity = 10):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.size = 0
        self.key_node_map = dict()

    def is_at_capacity(self):
        """Function to check if the cache has reached its full capacity

            Args: None

            Returns:
                boolean
        """
        return self.size == self.capacity
