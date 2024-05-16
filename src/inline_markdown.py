from textnode import TextNode, Text_node_type
import re


def split_nodes_delimiter(
    nodes: list[TextNode], delimiter: str, type_of_node: Text_node_type
) -> list[TextNode]:
    new_nodes = []
    for node in nodes:
        if node.text_type != Text_node_type.TXT:
            new_nodes.append(node)
            continue
        new_texts = node.text.split(delimiter)
        if not len(new_texts) % 2:
            raise SyntaxError("Invalid markdown syntax")
        for index, item in enumerate(new_texts):
            if item == "":
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(item, Text_node_type.TXT))
            else:
                new_nodes.append(TextNode(item, type_of_node))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
