import unittest
from text import text_to_textnodes
from textnode import TextNode, Text_node_type


class Test_text_to_textnodes(unittest.TestCase):

    def test_text_to_textnodes1(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        exp = [
            TextNode("This is ", Text_node_type.TXT),
            TextNode("text", Text_node_type.BOLD),
            TextNode(" with an ", Text_node_type.TXT),
            TextNode("italic", Text_node_type.ITALIC),
            TextNode(" word and a ", Text_node_type.TXT),
            TextNode("code block", Text_node_type.CODE),
            TextNode(" and an ", Text_node_type.TXT),
            TextNode(
                "image",
                Text_node_type.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", Text_node_type.TXT),
            TextNode("link", Text_node_type.LINK, "https://boot.dev"),
        ]
        res = text_to_textnodes(text)
        self.assertEqual(len(res), len(exp))
        for i, item in enumerate(res):
            self.assertEqual(item.text, exp[i].text)
            self.assertEqual(item.text_type, exp[i].text_type)
            self.assertEqual(item.url, exp[i].url)
