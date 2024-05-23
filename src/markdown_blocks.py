import re
from enum import Enum
from htmlNode import LeafNode, ParentNode, HtmlNode
from text import text_to_textnodes
from textnode import text_node_to_html_node


def text_to_children(text: str) -> list[HtmlNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def quote_block_to_HTML_node(block: str) -> HtmlNode:
    quotes = block.split("\n")
    new_lines = []
    for line in quotes:
        line = line.strip()
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ul_block_to_HTML_node(block: str) -> HtmlNode:
    list_items = []
    lines = block.split("\n")
    for line in lines:
        cleaned_line = line.strip().lstrip("-*")
        children = text_to_children(cleaned_line)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)


def ol_block_to_HTML_node(block: str) -> HtmlNode:
    list_items = []
    lines = block.split("\n")
    for line in lines:
        children = text_to_children(line)
        list_items.append(ParentNode("li", children))
    parent = ParentNode("ol", list_items)
    return parent


def code_block_to_HTML_node(block: str) -> HtmlNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError(f"Invalid code block: {block}")
    content = block.strip("`")
    children = text_to_children(content)
    pre_block = ParentNode("code", children)
    parent = ParentNode("pre", [pre_block])
    return parent


def h_block_to_HTML_node(block: str) -> HtmlNode:
    heading = re.findall(r"^#{0,6} ", block)
    if not heading:
        raise ValueError(f"Invalid heading line: {block}")
    heading_level = heading[0].count("#")
    children = text_to_children(block.lstrip("# "))
    parent = ParentNode(f"h{heading_level}", children)
    return parent


def p_block_to_HTML_node(block: str) -> HtmlNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


class Block_type(Enum):
    PARAGRAPH = p_block_to_HTML_node
    HEADING = h_block_to_HTML_node
    CODE = code_block_to_HTML_node
    QUOTE = quote_block_to_HTML_node
    UNORDERED_LIST = ul_block_to_HTML_node
    ORDERED_LIST = ol_block_to_HTML_node


def block_to_block_type(input_block: str) -> Block_type:
    match_headings = re.findall(r"^#{0,6} ", input_block)

    def check_quote(multiline: str) -> bool:
        lines = multiline.split("\n")
        for line in lines:
            if line[0] != ">":
                return False
        return True

    def check_ul(multiline: str) -> bool:
        lines = multiline.split("\n")
        if multiline[0:2] == "* ":
            for line in lines:
                if line[:2] != "* ":
                    return False
            return True
        if multiline[0:2] == "- ":
            for line in lines:
                if line[:2] != "- ":
                    return False
            return True
        return False

    def check_ol(multiline: str) -> bool:
        lines = multiline.split("\n")
        for index, line in enumerate(lines):
            if line[:3] == f"{index + 1}. ":
                continue
            return False
        return True

    if match_headings:
        return Block_type.HEADING
    if len(input_block) > 5 and input_block[0:3] == "```" and input_block[-3:] == "```":
        return Block_type.CODE
    if check_quote(input_block):
        return Block_type.QUOTE
    if check_ul(input_block):
        return Block_type.UNORDERED_LIST
    if check_ol(input_block):
        return Block_type.ORDERED_LIST
    else:
        return Block_type.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in raw_blocks:
        block = block.strip(" \n")
        if block != "":
            clean_blocks.append(block)
    return clean_blocks


def block_to_html_node(block: str) -> HtmlNode:
    block_type = block_to_block_type(block)
    return block_type(block)


def md_to_html(markdown: str) -> HtmlNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        child = block_to_html_node(block)
        children.append(child)
    return ParentNode("div", children)
