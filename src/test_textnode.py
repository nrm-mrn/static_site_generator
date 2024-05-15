import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("test node", 'italic')
        node2 = TextNode("test node", 'italic')
        self.assertEqual(node1, node2)

    def testUnEq(self):
        node1 = TextNode('test node 1', 'italic')
        node2 = TextNode('test node 2', 'italic')
        self.assertNotEqual(node1, node2)

if __name__ == '__main__':
    unittest.main()
