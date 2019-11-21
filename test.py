import unittest

from CacheNode import CacheNode
from LRUNode import LRUNode
from LFUNode import LFUNode
from Cache import Cache
from LRU_Cache import LRUCache
from LFU_Cache import LFUCache

class TestCacheNode(unittest.TestCase):
    def setUp(self):
        self.node_A = CacheNode(3, None, None)
        self.node_B = CacheNode(4)
        self.node_C = CacheNode(5)
        self.node_D = CacheNode(6)
        self.node_E = CacheNode(7)
        self.node_F = CacheNode(8, self.node_E)
        self.node_E.next = self.node_F

    def test_cache_node_initialization(self):
        self.assertEqual(self.node_A.key, 3, "Node A has an incorrect key")
        self.assertEqual(self.node_B.key, 4, "Node B has an incorrect key")
        self.assertEqual(self.node_C.key, 5, "Node C has an incorrect key")
        self.assertEqual(self.node_D.key, 6, "Node D has an incorrect key")
        self.assertEqual(self.node_E.key, 7, "Node E has an incorrect key")
        self.assertEqual(self.node_F.key, 8, "Node F has an incorrect key")
        self.assertEqual(self.node_E.next, self.node_F, "Node E is not linked forward to node F")
        self.assertEqual(self.node_F.prev, self.node_E, "Node F is not linked backwards to node E")

    def test_add_and_remove(self):
        self.node_B.add_node_after(self.node_A)
        self.assertEqual(self.node_A.next, self.node_B, "Node A is not linked next to Node B")
        self.node_C.add_node_after(self.node_B)
        self.assertEqual(self.node_B.next, self.node_C, "Node B is not linked next to Node C")
        self.node_B.remove_node()
        self.assertEqual(self.node_B.prev, None, "Node B is linked backwards to a non-null node")
        self.assertEqual(self.node_B.next, None, "Node B is linked forward to a non-null node")
        self.assertEqual(self.node_A.next, self.node_C, "Node A is not linked forward to node C")
        self.assertEqual(self.node_C.prev, self.node_A, "Node C is not linked backwards to node A")
        self.assertEqual(self.node_A.prev, None, "Node A is linked backwards to a non-null node")
        self.assertEqual(self.node_C.next, None, "Node C is linked forwards to a non-null node")

class TestLRUNode(unittest.TestCase):
    def setUp(self):
        self.lru_node = LRUNode(3, 7)

    def test_LRU_node_initialization(self):
        self.assertEqual(self.lru_node.value, 7, "LRU node has an incorrect value")

    def test_string_representation(self):
        self.assertEqual(repr(self.lru_node), "(key: 3, value: 7)", "LRU node's representation is inaccurate")

class TestLFUNode(unittest.TestCase):
    def setUp(self):
        self.lfu_node = LFUNode(5, 20)

    def test_LFU_node_initialization(self):
        self.assertEqual(self.lfu_node.frequency_cache.capacity, 20, "LFU node's frequency cache has an incorrect capacity")
        self.assertEqual(self.lfu_node.frequency_cache.size, 0, "LFU node's frequency cache has an incorrect size")

    def test_string_representation(self):
        res = "Frequency: 5\nSub LRU Cache:\nNodes:\n\n"
        self.assertEqual(repr(self.lfu_node), res, "LFU node's representation is inaccurate")

class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache_A = Cache(5)
        self.cache_B = Cache()

    def test_cache_initialization(self):
        self.assertEqual(self.cache_A.capacity, 5, "Cache A has an incorrect capacity")
        self.assertEqual(self.cache_B.capacity, 10, "Cache B has an incorrect capacity")
        self.assertEqual(self.cache_A.size, 0, "Cache A has an incorrect size")
        self.assertEqual(self.cache_B.size, 0, "Cache B has an incorrect size")
        self.assertEqual(len(self.cache_A.key_node_map), 0, "Cache A's key node map is not the correct size")
        self.assertEqual(len(self.cache_B.key_node_map), 0, "Cache B's key node map is not the correct size")

    def test_capacity_check(self):
        self.assertEqual(self.cache_A.is_at_capacity(), False, "Cache A is incorrectly listed as at capacity")
        self.assertEqual(self.cache_B.is_at_capacity(), False, "Cache B is incorrectly listed as at capacity")

class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.lru_cache = LRUCache(3)
        self.lru_cache.put_key_value(1,3)
        self.lru_cache.put_key_value(2,5)

    def test_get_value(self):
        self.assertEqual(self.lru_cache.get_value(1), 3, "Incorrect value for 1")
        self.assertEqual(self.lru_cache.get_value(2), 5, "Incorrect value for 2")
        self.assertEqual(self.lru_cache.get_value(3), None, "Incorrect value for key not in cache")

    def test_put_key_value(self):
        self.lru_cache.put_key_value(3,7)
        self.lru_cache.put_key_value(4,9)
        self.assertEqual(self.lru_cache.get_value(1), None, "Incorrect value for evicted key 1")
        self.assertEqual(self.lru_cache.get_value(2), 5, "Incorrect value for key 2")
        self.lru_cache.put_key_value(5,11)
        self.assertEqual(self.lru_cache.get_value(3), None, "Incorrect value for evicted key 3")
        self.assertEqual(self.lru_cache.get_value(4), 9, "Incorrect value for key 4")
        self.lru_cache.put_key_value(2,8)
        self.lru_cache.put_key_value(6,13)
        self.assertEqual(self.lru_cache.get_value(5), None, "Incorrect value for evicted key 5")

class TestLFUCache(unittest.TestCase):
    def setUp(self):
        self.lfu_cache_1 = LFUCache(1)
        self.lfu_cache_2 = LFUCache(2)
        self.lfu_cache_3 = LFUCache(3)

    def test_capacity_one_initialization(self):
        self.assertEqual(self.lfu_cache_1.size, 0, "Initial size of cache 1 is not 0")
        self.assertEqual(self.lfu_cache_1.capacity, 1, "Initial capacity of cache 1 is not 1")
        self.assertEqual(len(self.lfu_cache_1.key_node_map), 0, "Initial map size of cache 1 is not 0")
        self.assertEqual(len(self.lfu_cache_1.key_to_frequency_node), 0,\
            "Initial map size of key to frequency node in cache 1 is not 0")
        self.assertEqual(self.lfu_cache_1.head.key, 0, "Head key is not 0")
        self.assertEqual(self.lfu_cache_1.tail.key, 0, "Tail key is not 0")
        self.assertEqual(self.lfu_cache_1.head.next, self.lfu_cache_1.tail, "Head next does not match tail")
        self.assertEqual(self.lfu_cache_1.tail.prev, self.lfu_cache_1.head, "Tail prev does not match head")
        self.assertEqual(self.lfu_cache_1.head.prev, None, "Head does not have None prev")
        self.assertEqual(self.lfu_cache_1.tail.next, None, "Tail does not have None next")

        head_fc = self.lfu_cache_1.head.frequency_cache
        self.assertEqual(head_fc.capacity, 1, "Head frequency cache capacity is not 1")
        self.assertEqual(head_fc.size, 0, "Head frequency cache size is not 0")
        self.assertEqual(head_fc.top_level_frequency, 0, "Head frequency cache top level frequency is incorrect")

        tail_fc = self.lfu_cache_1.tail.frequency_cache
        self.assertEqual(tail_fc.capacity, 1, "Tail frequency cache capacity is not 1")
        self.assertEqual(tail_fc.size, 0, "Tail frequency cache size is not 0")
        self.assertEqual(tail_fc.top_level_frequency, 0, "Tail frequency cache top level frequency is incorrect")

    def test_capacity_one_operations(self):
        self.assertEqual(self.lfu_cache_1.get_value(3), None, "Entry not in cache has non-None value")
        self.lfu_cache_1.put_key_value(4, 9)
        self.assertEqual(self.lfu_cache_1.get_value(3), None, "Entry not in cache has non-None value")
        self.assertEqual(self.lfu_cache_1.get_value(4), 9, "Incorrect entry value")
        self.lfu_cache_1.put_key_value(2, 5)
        self.assertEqual(self.lfu_cache_1.get_value(3), None, "Entry not in cache has non-None value")
        self.assertEqual(self.lfu_cache_1.get_value(4), None, "Evicted entry value is not None")
        self.assertEqual(self.lfu_cache_1.get_value(2), 5, "Incorrect entry value")
        self.lfu_cache_1.get_value(2)
        self.lfu_cache_1.get_value(2)
        self.lfu_cache_1.put_key_value(3, 7)
        self.assertEqual(self.lfu_cache_1.get_value(2), None, "Evicted entry value is not None")
        self.assertEqual(self.lfu_cache_1.get_value(3), 7, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_1.get_value(4), None, "Evicted entry value is not None")
        self.lfu_cache_1.get_value(3)
        self.lfu_cache_1.put_key_value(3, 8)
        self.assertEqual(self.lfu_cache_1.get_value(3), 8, "Incorrect entry value")
        self.lfu_cache_1.put_key_value(3, 9)
        self.lfu_cache_1.put_key_value(3, 10)
        self.assertEqual(self.lfu_cache_1.get_value(3), 10, "Incorrect entry value")

    def test_capacity_two_operations(self):
        self.assertEqual(self.lfu_cache_2.get_value(1), None, "Entry not in cache has non-None value")
        self.lfu_cache_2.put_key_value(1, 3)
        self.assertEqual(self.lfu_cache_2.get_value(1), 3, "Incorrect entry value")
        self.lfu_cache_2.get_value(1)
        self.lfu_cache_2.put_key_value(2, 5)
        self.lfu_cache_2.put_key_value(3, 7)
        self.assertEqual(self.lfu_cache_2.get_value(1), 3, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_2.get_value(2), None, "Evicted entry value is not None")
        self.assertEqual(self.lfu_cache_2.get_value(3), 7, "Incorrect entry value")
        self.lfu_cache_2.put_key_value(3, 8)
        self.assertEqual(self.lfu_cache_2.get_value(3), 8, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_2.get_value(1), 3, "Incorrect entry value")
        self.lfu_cache_2.get_value(3)
        self.lfu_cache_2.put_key_value(4, 9)
        self.assertEqual(self.lfu_cache_2.get_value(1), None, "Evicted entry value is not None")
        self.assertEqual(self.lfu_cache_2.get_value(2), None, "Evicted entry value is not None")
        self.assertEqual(self.lfu_cache_2.get_value(3), 8, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_2.get_value(4), 9, "Incorrect entry value")

    def test_capacity_three_operations(self):
        self.assertEqual(self.lfu_cache_3.get_value(8), None, "Entry not in cache has non-None value")
        self.lfu_cache_3.put_key_value(8, 17)
        self.lfu_cache_3.put_key_value(7, 15)
        self.lfu_cache_3.put_key_value(6, 13)
        self.assertEqual(self.lfu_cache_3.get_value(8), 17, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_3.get_value(7), 15, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_3.get_value(6), 13, "Incorrect entry value")
        self.lfu_cache_3.put_key_value(5, 11)
        self.assertEqual(self.lfu_cache_3.get_value(8), None, "Evicted entry value is not None")
        self.assertEqual(self.lfu_cache_3.get_value(7), 15, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_3.get_value(6), 13, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_3.get_value(5), 11, "Incorrect entry value")
        self.lfu_cache_3.put_key_value(4, 9)
        self.assertEqual(self.lfu_cache_3.get_value(7), 15, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_3.get_value(6), 13, "Incorrect entry value")
        self.assertEqual(self.lfu_cache_3.get_value(5), None, "Evicted entry value is not None")
        self.assertEqual(self.lfu_cache_3.get_value(4), 9, "Incorrect entry value")

if __name__ == '__main__':
    unittest.main()
