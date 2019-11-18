from Cache import Cache
from LFUNode import LFUNode
from LRUNode import LRUNode

class LFUCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.head = LFUNode(0, capacity)
        self.tail = LFUNode(0, capacity)
        self.head.add_node_after(self.tail)
        self.key_to_frequency_node = dict()

    def get_value(self, key):
        """Function to retrieve value associated with a key if it exists,
            updating to reflect its recent usage

            Args:
                key (int) - key that is being queried

            Returns:
                value associated with key in cache if it is present, otherwise
                None; if present, the (key, value) pair's frequency of querying
                is updated
        """
        if self.is_key_in_cache(key):
            pass
        else:
            return None

    def put_key_value(self, key, value):
        """Function to place a key and an associated value into the cache,
            updating frequency to reflect its placement

            Args:
                key (int) - key that is being placed
                value (int) - value that is being placed

            Returns:
                None; cache is updated to mark the (key, value) pair with its
                new frequency
        """
        if self.is_key_in_cache(key):
            entry_node = self.key_node_map[key]
            entry_node.value = value
            entry_frequency_node = self.key_to_frequency_node[key]
            if entry_frequency_node.next.key == entry_frequency_node.key + 1:
                entry_node.top_level_frequency += 1
                
                self.key_to_frequency_node[key] = entry_frequency_node.next
            else:
                pass
        elif self.is_at_capacity():
            self.__evict_least_frequent_entry()
            self.__add_new_entry(key, value)
        else:
            self.__add_new_entry(key, value)

    def __add_new_entry(self, key, value):
        """Function to add a new (key, value) pair to the cache; it is assumed
            that the cache is not at full capacity

            Args:
                key (int)
                value (int)

            Returns:
                LRUNode - the LRUNode corresponding to the created entry
        """
        if not self.__has_frequency_one():
            frequency_one = LFUNode(key, self.capacity)
            frequency_one.add_node_after(self.head)
        self.size += 1
        self.key_node_map[key] = self.head.next.frequency_cache.put_key_value_internally(key, value)
        self.key_to_frequency_node[key] = self.head.next
        return self.key_node_map[key]

    def __evict_least_frequent_entry(self):
        """Function to remove the least frequently used entry of the cache;
            if there is a tie by frequency for least used, the least recently
            used entry is removed; if the LFU group corresponding to the
            frequency becomes empty, it is removed from the cache; it is assumed
            that the cache is non-empty at the start of this method

            Args: None

            Returns:
                LRUNode - the LRUNode corresponding to the removed entry
        """
        least_frequent_group = self.head.next.frequency_cache
        self.size -= 1
        removed_node = least_frequent_group.evict_LRU_entry()
        del self.key_node_map[removed_node.key] # remove from self.key_node_map
        del self.key_to_frequency_node[removed_node.key] # remove from self.key_to_frequency_node
        if least_frequent_group.size == 0: # if frequency group now empty, remove it
            self.head.next.remove_node()
        return removed_node

    def __has_frequency_one(self):
        """Function to test whether a top-level node with frequency 1 is
        present

        Args: None

        Returns:
            boolean - true iff frequency 1 node exists
        """
        return self.head.next.key == 1