import unittest

from htmlNode import HtmlNode, LeafNode, ParentNode


class test_htmlNode(unittest.TestCase):
    def test_html_conversion(self):
        html_node1 = HtmlNode(
            "p1", "test node", None, {"href": "http://bootdev.com", "class": "main_p"}
        )
        html_node2 = HtmlNode(
            "a", "test node 2", None, {"href": "", "class": "heading_main"}
        )
        node1_props = ' href="http://bootdev.com" class="main_p"'
        node2_props = ' href="" class="heading_main"'
        self.assertEqual(html_node1.props_to_html(), node1_props)
        self.assertEqual(html_node2.props_to_html(), node2_props)


class test_leafNode(unittest.TestCase):
    def test_leafNode_to_html(self):
        html_node1 = LeafNode(
            "p", "test node", {"href": "http://bootdev.com", "class": "main_p"}
        )
        html_node2 = LeafNode("a", "test node 2", {"href": "", "class": "heading_main"})
        html_node3 = LeafNode("h1", "test node 3")

        node1_html = '<p href="http://bootdev.com" class="main_p">test node</p>'
        node2_html = '<a href="" class="heading_main">test node 2</a>'
        node3_html = "<h1>test node 3</h1>"

        self.assertEqual(html_node1.to_html(), node1_html)
        self.assertEqual(html_node2.to_html(), node2_html)
        self.assertEqual(html_node3.to_html(), node3_html)


class test_parentNode(unittest.TestCase):
    def test_parentNode_to_html(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        target_html_1 = (
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        self.assertEqual(node1.to_html(), target_html_1)

        node2 = ParentNode(
            "p",
            [
                LeafNode("a", "Bold text", {"href": "https://boot.dev"}),
                LeafNode(None, "Normal text"),
            ],
        )

        node3 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                node2,
                LeafNode(None, "Normal text"),
            ],
            {"class": "main_heading"},
        )
        target_html_2 = '<p class="main_heading"><b>Bold text</b>Normal text<p><a href="https://boot.dev">Bold text</a>Normal text</p>Normal text</p>'
        self.assertEqual(node3.to_html(), target_html_2)


if __name__ == "__main__":
    unittest.main()
