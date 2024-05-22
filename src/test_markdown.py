import unittest
from markdown_blocks import (
    markdown_to_blocks,
    Block_type,
    block_to_block_type,
    quote_block_to_HTML_node,
    ul_block_to_HTML_node,
    ol_block_to_HTML_node,
)
from htmlNode import LeafNode, ParentNode
from textnode import TextNode, Text_node_type


class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        test_text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is a list item\n* This is another list item"
        exp = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
        ]
        res = markdown_to_blocks(test_text)
        self.assertEqual(res, exp)

    def test_markdown_to_blocks2(self):
        test_text = "\n\n\nThis is **bolded** paragraph\n\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items\n\n\n"
        exp = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        res = markdown_to_blocks(test_text)
        self.assertEqual(res, exp)


class Test_block_to_type(unittest.TestCase):
    def test_block_to_type_heading(self):
        test_lines = [
            "# h1",
            "## h2",
            "##not h",
            "#also not h",
            "###### h6",
            "####### not h",
            "not h",
            "### M-line h\n### anotoher line",
        ]
        exp = [
            Block_type.HEADING,
            Block_type.HEADING,
            Block_type.PARAGRAPH,
            Block_type.PARAGRAPH,
            Block_type.HEADING,
            Block_type.PARAGRAPH,
            Block_type.PARAGRAPH,
            Block_type.HEADING,
        ]
        res = [block_to_block_type(line) for line in test_lines]
        self.assertEqual(res, exp)

    def test_block_to_type_code(self):
        test_lines = [
            "```cdsdc qwd```",
            "```",
            "``asd`",
        ]
        exp = [
            Block_type.CODE,
            Block_type.PARAGRAPH,
            Block_type.PARAGRAPH,
        ]
        res = [block_to_block_type(line) for line in test_lines]
        self.assertEqual(res, exp)

    def test_block_to_type_quote(self):
        test_lines = [
            ">cdsdc qwd```",
            ">>```",
            "``asd`",
        ]
        exp = [
            Block_type.QUOTE,
            Block_type.QUOTE,
            Block_type.PARAGRAPH,
        ]
        res = [block_to_block_type(line) for line in test_lines]
        self.assertEqual(res, exp)

    def test_block_to_type_ul(self):
        test_lines = [
            "* ",
            "- line 1\n- line 2\n- line 3 and - not line 4",
            "* line 1\n- line 2\n* line 3",
            "*line 1\n- line 2\n* line 3",
        ]
        exp = [
            Block_type.UNORDERED_LIST,
            Block_type.UNORDERED_LIST,
            Block_type.PARAGRAPH,
            Block_type.PARAGRAPH,
        ]
        res = [block_to_block_type(line) for line in test_lines]
        self.assertEqual(res, exp)

    def test_block_to_type_ol(self):
        test_lines = [
            "1. ",
            "1. line 1\n2. line 2\n3. line 3 and 4. not line 4",
            "2. line 1\n3. line 2\n4. line 3",
            "1. line 1\n2 line 2\n3. line 3",
            "1.",
        ]
        exp = [
            Block_type.ORDERED_LIST,
            Block_type.ORDERED_LIST,
            Block_type.PARAGRAPH,
            Block_type.PARAGRAPH,
            Block_type.PARAGRAPH,
        ]
        res = [block_to_block_type(line) for line in test_lines]
        self.assertEqual(res, exp)


class Test_markdown_to_Html_node(unittest.TestCase):
    def test_md_quote_to_HTML_node1(self):
        tests = [
            "> This is a quote",
            "> This is a quote\n > Multiline\n> Third line",
            "> This is a quote\n >> Nested\n>>> More nesting",
        ]

        exp_res = [
            ParentNode("blockquote", [LeafNode(None, tests[0][2:])]),
            ParentNode(
                "blockquote", [LeafNode(None, "This is a quote Multiline Third line")]
            ),
            ParentNode(
                "blockquote", [LeafNode(None, "This is a quote Nested More nesting")]
            ),
        ]

        for index, line in enumerate(tests):
            res = quote_block_to_HTML_node(line)
            self.assertIsInstance(res, ParentNode)
            self.assertEqual(res.tag, exp_res[index].tag)
            self.assertIsInstance(res.children[0], LeafNode)
            self.assertEqual(res.children[0].value, exp_res[index].children[0].value)

    def test_md_quote_to_HTML_node2(self):
        test = "> This is a **bold** quote with ```code``` and *italic* words"

        exp_res = ParentNode(
            "blockquote",
            [
                LeafNode(None, "This is a "),
                LeafNode("b", "bold"),
                LeafNode(None, " quote with "),
                LeafNode("code", "code"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " words"),
            ],
        )

        res = quote_block_to_HTML_node(test)
        self.assertIsInstance(res, ParentNode)
        self.assertEqual(res.tag, exp_res.tag)
        for index, child in enumerate(exp_res.children):
            self.assertIsInstance(child, LeafNode)
            self.assertEqual(res.children[index].tag, exp_res.children[index].tag)
            self.assertEqual(res.children[index].value, exp_res.children[index].value)

    def test_md_ul_to_HTML_node(self):
        tests = [
            "* item1\n * item2\n* item3",
            "- item1\n- item2\n- item3",
            "* **bold** item 1\n* *italic* item 2\n* ```code``` item 3",
        ]

        exp_res = [
            ParentNode(
                "ul",
                [
                    ParentNode("li", [LeafNode(None, "item1")]),
                    ParentNode("li", [LeafNode(None, "item2")]),
                    ParentNode("li", [LeafNode(None, "item3")]),
                ],
            ),
            ParentNode(
                "ul",
                [
                    ParentNode("li", [LeafNode(None, "item1")]),
                    ParentNode("li", [LeafNode(None, "item2")]),
                    ParentNode("li", [LeafNode(None, "item3")]),
                ],
            ),
            ParentNode(
                "ul",
                [
                    ParentNode(
                        "li", [LeafNode("b", "bold"), LeafNode(None, " item 1")]
                    ),
                    ParentNode(
                        "li", [LeafNode("i", "italic"), LeafNode(None, " item 2")]
                    ),
                    ParentNode(
                        "li", [LeafNode("code", "code"), LeafNode(None, " item 3")]
                    ),
                ],
            ),
        ]

        for i, test in enumerate(tests):
            res = ul_block_to_HTML_node(test)
            self.assertIsInstance(res, ParentNode)
            self.assertEqual(res.tag, exp_res[i].tag)
            for i_ch, child in enumerate(res.children):
                self.assertIsInstance(child, ParentNode)
                self.assertEqual(child.tag, exp_res[i].children[i_ch].tag)
                self.assertEqual(child.value, exp_res[i].children[i_ch].value)

    def test_md_ol_to_HTML_node(self):
        tests = [
            "1. item1\n2. item2\n3. item3",
            "1. - item1",
            "1. **bold** item 1\n2. *italic* item 2\n3. ```code``` item 3",
        ]

        exp_res = [
            ParentNode(
                "ol",
                [
                    ParentNode("li", [LeafNode(None, "1. item1")]),
                    ParentNode("li", [LeafNode(None, "2. item2")]),
                    ParentNode("li", [LeafNode(None, "3. item3")]),
                ],
            ),
            ParentNode(
                "ol",
                [
                    ParentNode("li", [LeafNode(None, "1. - item1")]),
                ],
            ),
            ParentNode(
                "ol",
                [
                    ParentNode(
                        "li",
                        [
                            LeafNode(None, "1. "),
                            LeafNode("b", "bold"),
                            LeafNode(None, " item 1"),
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode(None, "2. "),
                            LeafNode("i", "italic"),
                            LeafNode(None, " item 2"),
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode(None, "3. "),
                            LeafNode("code", "code"),
                            LeafNode(None, " item 3"),
                        ],
                    ),
                ],
            ),
        ]

        for i, test in enumerate(tests):
            res = ol_block_to_HTML_node(test)
            self.assertIsInstance(res, ParentNode)
            self.assertEqual(res.tag, exp_res[i].tag)
            for i_ch, child in enumerate(res.children):
                self.assertIsInstance(child, ParentNode)
                self.assertEqual(child.tag, exp_res[i].children[i_ch].tag)
                self.assertEqual(child.value, exp_res[i].children[i_ch].value)
