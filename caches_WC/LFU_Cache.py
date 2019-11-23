from .Cache import Cache
from .LFUNode import LFUNode
from .LRUNode import LRUNode

class LFUCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.head = LFUNode(0, capacity)
        self.tail = LFUNode(0, capacity)
        self.tail.add_node_after(self.head)
        self.key_to_frequency_node = dict()

    def __repr__(self):
        res = "LFU Cache:\n"
        res += "----------\n"
        res += "Capacity: " + str(self.capacity) + "\n"
        res += "Size: " + str(self.size) + "\n"
        res += "Key-Node-Map: " + str(self.key_node_map) + "\n\n"
        curr_node = self.head.next
        while curr_node != self.tail:
            res += str(curr_node) + "\n\n"
            curr_node = curr_node.next
        return res

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
            entry_node, frequency_node = self.__remove_key(key)
            if frequency_node.next.key != frequency_node.key + 1:
                self.__create_frequency_node_after(frequency_node)
            new_frequency_node = frequency_node.next
            self.__add_entry_to_frequency_node(entry_node, new_frequency_node)
            if frequency_node.frequency_cache.size == 0:
                self.__remove_frequency_node(frequency_node)
            self.key_to_frequency_node[key] = new_frequency_node
            return entry_node.value
        else:
            return None

    def __remove_frequency_node(self, frequency_node):
        """Function to remove an existent frequency_node from the cache

            Args:
                frequency_node (LFUNode) - node to remove

            Returns:
                None
        """
        frequency_node.remove_node()

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
            entry_node, entry_frequency_node = self.__remove_key(key)
            entry_node.value = value
            if entry_frequency_node.next.key != entry_frequency_node.key + 1:
                self.__create_frequency_node_after(entry_frequency_node)
            self.key_to_frequency_node[entry_node.key] = entry_frequency_node.next
            self.__add_entry_to_frequency_node(entry_node, entry_frequency_node.next)
            if entry_frequency_node.frequency_cache.size == 0: # if frequency group now empty, remove it
                self.__remove_frequency_node(entry_frequency_node)
        elif self.is_at_capacity():
            self.__evict_least_frequent_entry()
            self.__add_new_entry(key, value)
        else:
            self.__add_new_entry(key, value)

    def __add_entry_to_frequency_node(self, entry_node, frequency_node):
        """Given an LRUCache node entry_node and a frequency_node, insert
            entry_node into frequency_node's LRU cache

            Args:
                entry_node (LRUNode) - node to be entered into cache
                frequency_node (LFUNode) - frequency node at which to add LRUNode

            Returns:
                None
        """
        y = frequency_node.frequency_cache
        if y.size == y.capacity:
            raise ValueError("Frequency (LRU) cache is already at capacity!")
        self.key_to_frequency_node[entry_node.key] = frequency_node
        y.size += 1
        entry_node.add_node_after(y.head)
        y.key_node_map[entry_node.key] = entry_node

    def __remove_key(self, key):
        """Function to remove the node corresponding to a specific key from the
            cache; it is assumed that the key is present in the cache

            Args:
                key (int) - key to remove

            Returns:
                entry_node (LRUNode) - corresponds to key removed
                entry_frequency_node (LFUNode) - frequency node containing key removed
        """
        entry_node = self.key_node_map[key]
        entry_frequency_node = self.key_to_frequency_node[key]

        entry_node.remove_node()
        self.key_to_frequency_node[key].frequency_cache.size -= 1
        del self.key_to_frequency_node[key].frequency_cache.key_node_map[key]
        del self.key_to_frequency_node[key]
        return entry_node, entry_frequency_node

    def __create_frequency_node_after(self, frequency_node):
        """Function to create a new top-level frequency node which has frequency
            key one more than that of the given frequency_node; it is assumed
            that the frequency frequency_node.key + 1 does not exist in the
            cache at the start of this function

            Args:
                frequency_node (LFUNode)

            Returns:
                None
        """
        current_frequency = frequency_node.key
        new_entry = LFUNode(current_frequency+1, self.capacity)
        # self.key_to_frequency_node[current_frequency+1] = new_entry
        new_entry.add_node_after(frequency_node)

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
            frequency_one = LFUNode(1, self.capacity)
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
            self.__remove_frequency_node(self.head.next)
        return removed_node

    def __has_frequency_one(self):
        """Function to test whether a top-level node with frequency 1 is
        present

        Args: None

        Returns:
            boolean - true iff frequency 1 node exists
        """
        return self.head.next.key == 1
