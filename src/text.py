from enum import Enum
from textnode import Text_node_type, TextNode
from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link


class text_types_delimiters(Enum):
    BOLD = "**"
    ITALIC = "*"
    CODE = "`"


def text_to_textnodes(text: str) -> list[TextNode]:
    resulting_nodes = [TextNode(text, Text_node_type.TXT)]
    for item in text_types_delimiters:
        resulting_nodes = split_nodes_delimiter(
            resulting_nodes, item.value, Text_node_type[item.name]
        )

    resulting_nodes = split_nodes_image(resulting_nodes)
    resulting_nodes = split_nodes_link(resulting_nodes)

    return resulting_nodes
