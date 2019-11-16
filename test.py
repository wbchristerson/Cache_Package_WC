import unittest

from CacheNode import CacheNode
from LRUNode import LRUNode
from LFUNode import LFUNode
from Cache import Cache

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
        self.assertEqual(repr(self.lfu_node), "(key: 5)", "LFU node's representation is inaccurate")

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

if __name__ == '__main__':
    unittest.main()
