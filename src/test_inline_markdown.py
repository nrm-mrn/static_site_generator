import unittest
from textnode import TextNode, Text_node_type
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delim(self):
        node = TextNode("This is text with a `code block` word", Text_node_type.TXT)
        new_nodes = split_nodes_delimiter([node], "`", Text_node_type.CODE)

        exp_res = [
            TextNode("This is text with a ", Text_node_type.TXT),
            TextNode("code block", Text_node_type.CODE),
            TextNode(" word", Text_node_type.TXT),
        ]
        self.assertEqual(len(new_nodes), len(exp_res))
        self.assertEqual(new_nodes[0].text, exp_res[0].text)
        self.assertEqual(new_nodes[1].text_type, exp_res[1].text_type)

    def test_italic_delim(self):
        node = TextNode("**italic** word", Text_node_type.TXT)
        new_nodes = split_nodes_delimiter([node], "**", Text_node_type.ITALIC)

        exp_res = [
            TextNode("italic", Text_node_type.ITALIC),
            TextNode(" word", Text_node_type.TXT),
        ]
        self.assertEqual(len(new_nodes), len(exp_res))
        self.assertEqual(new_nodes[0].text, exp_res[0].text)
        self.assertEqual(new_nodes[1].text_type, exp_res[1].text_type)

    def test_bold_delim(self):
        node = TextNode("word*bold*", Text_node_type.TXT)
        new_nodes = split_nodes_delimiter([node], "*", Text_node_type.BOLD)

        exp_res = [
            TextNode("word", Text_node_type.TXT),
            TextNode("bold", Text_node_type.BOLD),
        ]
        self.assertEqual(len(new_nodes), len(exp_res))
        self.assertEqual(new_nodes[0].text, exp_res[0].text)
        self.assertEqual(new_nodes[1].text_type, exp_res[1].text_type)

    def test_code_delim_exc(self):
        node = TextNode("This is text with a *wrong MD syntax", Text_node_type.TXT)

        self.assertRaises(
            SyntaxError,
            split_nodes_delimiter,
            [node],
            "*",
            Text_node_type.BOLD,
        )


class TestExtractMdImages(unittest.TestCase):
    def test_extract_md_images(self):
        text = "This is text with an ![image](https://test.png) and ![another](https://test2.png)"
        extracted = extract_markdown_images(text)
        exp = [("image", "https://test.png"), ("another", "https://test2.png")]

        self.assertEqual(extracted, exp)

    def test_extract_md_links(self):
        text = "This is text with an [link](https://test.png) and [anotherLink](https://test2.png)"
        extracted = extract_markdown_links(text)
        exp = [("link", "https://test.png"), ("anotherLink", "https://test2.png")]

        self.assertEqual(extracted, exp)
