import unittest

from textnode import TextNode, Text_node_type, text_node_to_html_node
from inline_markdown import split_nodes_delimiter
from htmlNode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("test node", "italic")
        node2 = TextNode("test node", "italic")
        self.assertEqual(node1, node2)

    def testUnEq(self):
        node1 = TextNode("test node 1", "italic")
        node2 = TextNode("test node 2", "italic")
        self.assertNotEqual(node1, node2)


class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("Some plain text", Text_node_type.TXT)
        self.assertIsInstance(text_node_to_html_node(text_node), LeafNode)
        self.assertEqual(text_node_to_html_node(text_node).value, "Some plain text")
        self.assertEqual(text_node_to_html_node(text_node).tag, None)

    def test_bold(self):
        text_node = TextNode("Some bold text", Text_node_type.BOLD)
        self.assertIsInstance(text_node_to_html_node(text_node), LeafNode)
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), "<b>Some bold text</b>"
        )

    def test_italic(self):
        text_node = TextNode("Some italic text", Text_node_type.ITALIC)
        self.assertIsInstance(text_node_to_html_node(text_node), LeafNode)
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), "<i>Some italic text</i>"
        )

    def test_code(self):
        text_node = TextNode("Some code", Text_node_type.CODE)
        self.assertIsInstance(text_node_to_html_node(text_node), LeafNode)
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), "<code>Some code</code>"
        )

    def test_link(self):
        text_node = TextNode("Some link", Text_node_type.LINK, "https://bootdev.com")
        self.assertIsInstance(text_node_to_html_node(text_node), LeafNode)
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            '<a href="https://bootdev.com">Some link</a>',
        )

    def test_img(self):
        text_node = TextNode("Some img", Text_node_type.IMAGE, "https://bootdev.com")
        self.assertIsInstance(text_node_to_html_node(text_node), LeafNode)
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            '<img src="https://bootdev.com" alt="Some img"></img>',
        )


if __name__ == "__main__":
    unittest.main()
