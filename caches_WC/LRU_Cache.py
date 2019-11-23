from .Cache import Cache
from .LRUNode import LRUNode

class LRUCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.head = LRUNode(0, 0)
        self.tail = LRUNode(0, 0)
        self.tail.add_node_after(self.head)

    def __repr__(self):
        res = "Nodes:\n"
        curr_node = self.head.next
        while curr_node != self.tail:
            res += str(curr_node) + "\n"
            curr_node = curr_node.next
        res += "\n"
        return res

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
            self.__mark_as_most_recent(matching_node)
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
                None
        """
        self.put_key_value_internally(key, value)

    def put_key_value_internally(self, key, value):
        """Same functionality as put_key_value but the resulting node is not
            returned

            Args:
                key (int) - key that is being placed
                value (int) - value that is being placed

            Returns:
                updated node; cache is updated to mark the (key, value) pair as
                the most recently queried
        """
        if self.is_key_in_cache(key):
            self.key_node_map[key].value = value
            self.__mark_as_most_recent(self.key_node_map[key])
        else:
            if self.is_at_capacity():
                self.evict_LRU_entry()
            self.size += 1
            self.key_node_map[key] = LRUNode(key, value)
            self.key_node_map[key].add_node_after(self.head)
        return self.key_node_map[key]

    def evict_LRU_entry(self):
        """Function to remove the least recently used entry from the cache;
            it is assumed that the cache has at least one entry in it

            Args: None

            Returns:
                LRUNode - the evicted node, now without links to the internal
                 linked list
        """
        self.size -= 1
        del self.key_node_map[self.tail.prev.key]
        return self.tail.prev.remove_node()

    def __mark_as_most_recent(self, cache_entry):
        """Given an LRUNode cache_entry which is present in the cache, mark it
            internally as the most recently queried

            Args:
                cache_entry (LRUNode) - node to be marked

            Returns:
                None
        """
        cache_entry.remove_node()
        cache_entry.add_node_after(self.head)
