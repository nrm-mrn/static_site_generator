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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != Text_node_type.TXT:
            new_nodes.append(node)
            continue
        extracted_images = extract_markdown_images(node.text)
        if not extracted_images:
            new_nodes.append(node)
            continue
        text_to_split = node.text
        for image in extracted_images:
            pre_nodes = text_to_split.split(f"![{image[0]}]({image[1]})", 1)
            if pre_nodes[0] != "":
                new_nodes.append(TextNode(pre_nodes[0], Text_node_type.TXT))
            new_nodes.append(TextNode(image[0], Text_node_type.IMAGE, image[1]))
            text_to_split = pre_nodes[1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, Text_node_type.TXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != Text_node_type.TXT:
            new_nodes.append(node)
            continue
        extracted_links = extract_markdown_links(node.text)
        if not extracted_links:
            new_nodes.append(node)
            continue
        text_to_split = node.text
        for link in extracted_links:
            pre_nodes = text_to_split.split(f"[{link[0]}]({link[1]})", 1)
            if pre_nodes[0] != "":
                new_nodes.append(TextNode(pre_nodes[0], Text_node_type.TXT))
            new_nodes.append(TextNode(link[0], Text_node_type.LINK, link[1]))
            text_to_split = pre_nodes[1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, Text_node_type.TXT))
    return new_nodes
