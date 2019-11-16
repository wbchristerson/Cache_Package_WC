import unittest

from CacheNode import CacheNode
from LRUNode import LRUNode
from LFUNode import LFUNode

class TestCacheNode(unittest.TestCase):
    def setUp(self):
        self.node_A = CacheNode(3, None, None)
        self.node_B = CacheNode(4)
        self.node_C = CacheNode(5)
        self.node_D = CacheNode(6)

    def test_initialization(self):
        self.assertEqual(self.node_A.key, 3, "Node A has an incorrect key")
        self.assertEqual(self.node_B.key, 4, "Node B has an incorrect key")
        self.assertEqual(self.node_C.key, 5, "Node C has an incorrect key")
        self.assertEqual(self.node_D.key, 6, "Node D has an incorrect key")

    def test_add_and_remove(self):
        self.node_B.add_node_after(self.node_A)
        self.assertEqual(self.node_A.next, self.node_B, "Node A is not linked next to Node B")
        self.node_C.add_node_after(self.node_B)
        self.assertEqual(self.node_B.next, self.node_C, "Node B is not linked next to Node C")
        self.node_B.remove_node()
        self.assertEqual(self.node_B.prev, None, "Node B is linked previously to a non-null node")
        self.assertEqual(self.node_B.next, None, "Node B is linked forward to a non-null node")
        self.assertEqual(self.node_A.next, self.node_C, "Node A is not linked forward to node C")
        self.assertEqual(self.node_C.prev, self.node_A, "Node C is not linked backwards to node A")

if __name__ == '__main__':
    unittest.main()
