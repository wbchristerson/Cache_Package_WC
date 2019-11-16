from Cache import Cache
from LRUNode import LRUNode

class LRUCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.head = LRUNode(0, 0)
        self.tail = LRUNode(0, 0)
        self.tail.add_node_after(self.head)

    def get_value(self, key):
        """Function to retrieve value associated with a key if it exists,
            updating to reflect its recent usage

            Args:
                key (int) - key that is being queried

            Returns:
                value associated with key in cache if it is present, otherwise
                None; if present, the (key, value) pair is marked as the most
                recently queried
        """
        if self.is_key_in_cache(key):
            matching_node = self.key_node_map[key]
            matching_node.remove_node()
            matching_node.add_node_after(self.head)
            return matching_node.value
        else:
            return None

    def put_key_value(self, key, value):
        """Function to place a key and an associated value into the cache,
            updating to reflect its recent placement

            Args:
                key (int) - key that is being placed
                value (int) - value that is being placed

            Returns:
                None; cache is updated to mark the (key, value) pair as the most
                recently queried
        """
        pass

    def __is_key_in_cache(self, key):
        """Function to check if a key is present in the cache

            Args:
                key (int) - key that is being checked

            Returns:
                boolean
        """
        return key in self.key_node_map
