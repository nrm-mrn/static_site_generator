import unittest

from markdown_blocks import block_to_html_node, md_to_html
from htmlNode import ParentNode, LeafNode


class Test_md_to_html_node(unittest.TestCase):
    def test_md_to_html_node(self):
        tests = ["just a simple paragraph"]

        exp_res = [ParentNode("p", [LeafNode(None, tests[0])])]

        for i, test in enumerate(tests):
            res = block_to_html_node(test)
            self.assertIsInstance(res, ParentNode)
            self.assertEqual(res.tag, exp_res[i].tag)
            for ch_i, child in enumerate(res.children):
                self.assertIsInstance(child, LeafNode)
                self.assertEqual(child.tag, exp_res[i].children[ch_i].tag)
                self.assertEqual(child.value, exp_res[i].children[ch_i].value)


class Test_md_to_html(unittest.TestCase):
    def test_md_to_html(self):
        tests = [
            "# main heading\n\nSecond block is a paragraph\n\nThen a [link to google](https://google.com)\n\nAnd final\nmultiline p with\n**bold** and *italic* text."
        ]

        exp_res = [
            ParentNode(
                "div",
                [
                    ParentNode("h1", [LeafNode(None, "main heading")]),
                    ParentNode("p", [LeafNode(None, "Second block is a paragraph")]),
                    ParentNode(
                        "p",
                        [
                            LeafNode(None, "Then a "),
                            LeafNode(
                                "a", "link to google", {"href": "https://google.com"}
                            ),
                        ],
                    ),
                    ParentNode(
                        "p",
                        [
                            LeafNode(None, "And final multiline p with "),
                            LeafNode("b", "bold"),
                            LeafNode(None, " and "),
                            LeafNode("i", "italic"),
                            LeafNode(None, " text."),
                        ],
                    ),
                ],
            )
        ]

        for i, test in enumerate(tests):
            res = md_to_html(test)
            self.assertIsInstance(res, ParentNode)
            self.assertEqual(res.tag, exp_res[i].tag)
            for ch_i, child in enumerate(res.children):
                self.assertIsInstance(child, ParentNode)
                self.assertEqual(child.tag, exp_res[i].children[ch_i].tag)
                for leaf_i, leaf in enumerate(child.children):
                    self.assertIsInstance(leaf, LeafNode)
                    self.assertEqual(
                        leaf.tag, exp_res[i].children[ch_i].children[leaf_i].tag
                    )
                    self.assertEqual(
                        leaf.value, exp_res[i].children[ch_i].children[leaf_i].value
                    )
                    if leaf.props:
                        self.assertEqual(
                            leaf.props, exp_res[i].children[ch_i].children[leaf_i].props
                        )
