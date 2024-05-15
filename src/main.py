from textnode import TextNode, Text_node_type
from htmlNode import LeafNode


def text_node_to_html_node(node: TextNode):
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
    else:
        raise Exception("Got wrong TextNode type")


def main():
    test_node = TextNode("Test text node, bold", "bold", "https://www.boot.dev")
    print(test_node)


main()
