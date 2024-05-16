from enum import Enum
from htmlNode import LeafNode


class Text_node_type(Enum):
    TXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:

    def __init__(
        self, text: str, text_type: Text_node_type, url: str | None = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_TextNode):
        if (
            self.text == other_TextNode.text
            and self.text_type == other_TextNode.text_type
            and self.url == other_TextNode.url
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(node: TextNode) -> LeafNode:
    if node.text_type == Text_node_type.TXT:
        return LeafNode(None, node.text)
    if node.text_type == Text_node_type.BOLD:
        return LeafNode("b", node.text)
    if node.text_type == Text_node_type.ITALIC:
        return LeafNode("i", node.text)
    if node.text_type == Text_node_type.CODE:
        return LeafNode("code", node.text)
    if node.text_type == Text_node_type.LINK:
        return LeafNode("a", node.text, {"href": node.url})
    if node.text_type == Text_node_type.IMAGE:
        return LeafNode("img", "", {"src": node.url, "alt": node.text})
    raise Exception("Got wrong TextNode type")
