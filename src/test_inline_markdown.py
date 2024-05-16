import unittest
from textnode import TextNode, Text_node_type
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
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

    def test_extract_md_images2(self):
        text = (
            "![image](https://test.png) and another ![another](https://test2.png) image"
        )
        extracted = extract_markdown_images(text)
        exp = [("image", "https://test.png"), ("another", "https://test2.png")]

        self.assertEqual(extracted, exp)

    def test_extract_md_links(self):
        text = "This is text with an [link](https://test.png) and [anotherLink](https://test2.png)"
        extracted = extract_markdown_links(text)
        exp = [("link", "https://test.png"), ("anotherLink", "https://test2.png")]

        self.assertEqual(extracted, exp)


class TestSplitImages(unittest.TestCase):
    def test_split_image(self):
        text1 = "image"
        text2 = "second image"
        url1 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"
        url2 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        node = TextNode(
            f"This is text with an ![{text1}]({url1}) and another ![{text2}]({url2})",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, Text_node_type.TXT)
        self.assertEqual(new_nodes[1].text, text1)
        self.assertEqual(new_nodes[1].text_type, Text_node_type.IMAGE)
        self.assertEqual(new_nodes[1].url, url1)
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[2].text_type, Text_node_type.TXT)
        self.assertEqual(new_nodes[3].text, text2)
        self.assertEqual(new_nodes[3].text_type, Text_node_type.IMAGE)
        self.assertEqual(new_nodes[3].url, url2)

    def test_split_image2(self):
        text1 = "image"
        text2 = "second image"
        url1 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"
        url2 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        node = TextNode(
            f"![{text1}]({url1}) and another ![{text2}]({url2}) image",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, text1)
        self.assertEqual(new_nodes[0].text_type, Text_node_type.IMAGE)
        self.assertEqual(new_nodes[0].url, url1)
        self.assertEqual(new_nodes[1].text, " and another ")
        self.assertEqual(new_nodes[1].text_type, Text_node_type.TXT)
        self.assertEqual(new_nodes[2].text, text2)
        self.assertEqual(new_nodes[2].text_type, Text_node_type.IMAGE)
        self.assertEqual(new_nodes[2].url, url2)
        self.assertEqual(new_nodes[3].text, " image")
        self.assertEqual(new_nodes[3].text_type, Text_node_type.TXT)

    def test_split_image3(self):
        text1 = "image"
        text2 = "second image"
        text3 = "third image"
        url1 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"
        url2 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        url3 = "https://test.com"
        node = TextNode(
            f"![{text1}]({url1})![{text2}]({url2})![{text3}]({url3}) images",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, text1)
        self.assertEqual(new_nodes[0].text_type, Text_node_type.IMAGE)
        self.assertEqual(new_nodes[0].url, url1)
        self.assertEqual(new_nodes[1].text, text2)
        self.assertEqual(new_nodes[1].text_type, Text_node_type.IMAGE)
        self.assertEqual(new_nodes[1].url, url2)
        self.assertEqual(new_nodes[2].text, text3)
        self.assertEqual(new_nodes[2].text_type, Text_node_type.IMAGE)
        self.assertEqual(new_nodes[2].url, url3)
        self.assertEqual(new_nodes[3].text, " images")
        self.assertEqual(new_nodes[3].text_type, Text_node_type.TXT)

    def test_split_image4(self):
        text1 = "Just a plain text"
        node = TextNode(
            f"{text1}",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)

        self.assertEqual(new_nodes[0].text, text1)
        self.assertEqual(new_nodes[0].text_type, Text_node_type.TXT)

    def test_split_image5(self):
        text1 = ""
        node = TextNode(
            f"{text1}",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)

        self.assertEqual(new_nodes[0].text, text1)
        self.assertEqual(new_nodes[0].text_type, Text_node_type.TXT)


class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        text1 = "link"
        text2 = "second link"
        url1 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"
        url2 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        node = TextNode(
            f"This is text with a [{text1}]({url1}) link and another [{text2}]({url2})",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, Text_node_type.TXT)
        self.assertEqual(new_nodes[1].text, text1)
        self.assertEqual(new_nodes[1].text_type, Text_node_type.LINK)
        self.assertEqual(new_nodes[1].url, url1)
        self.assertEqual(new_nodes[2].text, " link and another ")
        self.assertEqual(new_nodes[2].text_type, Text_node_type.TXT)
        self.assertEqual(new_nodes[3].text, text2)
        self.assertEqual(new_nodes[3].text_type, Text_node_type.LINK)
        self.assertEqual(new_nodes[3].url, url2)

    def test_split_links2(self):
        text1 = "link"
        text2 = "second link"
        url1 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"
        url2 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        node = TextNode(
            f"[{text1}]({url1}) and another [{text2}]({url2}) link",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, text1)
        self.assertEqual(new_nodes[0].text_type, Text_node_type.LINK)
        self.assertEqual(new_nodes[0].url, url1)
        self.assertEqual(new_nodes[1].text, " and another ")
        self.assertEqual(new_nodes[1].text_type, Text_node_type.TXT)
        self.assertEqual(new_nodes[2].text, text2)
        self.assertEqual(new_nodes[2].text_type, Text_node_type.LINK)
        self.assertEqual(new_nodes[2].url, url2)
        self.assertEqual(new_nodes[3].text, " link")
        self.assertEqual(new_nodes[3].text_type, Text_node_type.TXT)

    def test_split_links3(self):
        text1 = "link"
        text2 = "second link"
        text3 = "third link"
        url1 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"
        url2 = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        url3 = "https://test.com"
        node = TextNode(
            f"[{text1}]({url1})[{text2}]({url2})[{text3}]({url3}) links",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, text1)
        self.assertEqual(new_nodes[0].text_type, Text_node_type.LINK)
        self.assertEqual(new_nodes[0].url, url1)
        self.assertEqual(new_nodes[1].text, text2)
        self.assertEqual(new_nodes[1].text_type, Text_node_type.LINK)
        self.assertEqual(new_nodes[1].url, url2)
        self.assertEqual(new_nodes[2].text, text3)
        self.assertEqual(new_nodes[2].text_type, Text_node_type.LINK)
        self.assertEqual(new_nodes[2].url, url3)
        self.assertEqual(new_nodes[3].text, " links")
        self.assertEqual(new_nodes[3].text_type, Text_node_type.TXT)

    def test_split_links4(self):
        text1 = "Just a plain text"
        node = TextNode(
            f"{text1}",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)

        self.assertEqual(new_nodes[0].text, text1)
        self.assertEqual(new_nodes[0].text_type, Text_node_type.TXT)

    def test_split_links5(self):
        text1 = ""
        node = TextNode(
            f"{text1}",
            Text_node_type.TXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)

        self.assertEqual(new_nodes[0].text, text1)
        self.assertEqual(new_nodes[0].text_type, Text_node_type.TXT)
