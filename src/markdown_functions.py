# Functions that work with raw markdown
import re

from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode_functions import text_node_to_html_node, text_to_textnodes


def markdown_to_blocks(md: str):
    """
    Takes a markdown document as input and returns a list of blocks in the form of strings
    """
    candidate_blocks = md.split("\n\n")
    blocks = []
    for block in candidate_blocks:
        block = block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks


def text_to_children(text, is_list=False):
    children = []
    if is_list:
        items = text.splitlines("\n")
        for item in items:
            nodes = text_to_textnodes(item)
            item_node = ParentNode(
                tag="li", children=[text_node_to_html_node(node) for node in nodes]
            )
            children.append(item_node)
        return children
    textnodes = text_to_textnodes(text)
    for node in textnodes:
        if node.text == "" or node.text == "\n":
            continue
        children.append(text_node_to_html_node(node))
    return children


def markdown_to_html_node(md: str):
    blocks = markdown_to_blocks(md)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        node = None
        match type:
            case BlockType.HEADING:
                header_num = block.count("#")
                if header_num < 1 or header_num > 6:
                    raise TypeError(
                        "Headers cannot have less than 1 or more than 6 #'s."
                    )
                node = ParentNode(
                    tag=f"h{header_num}",
                    children=text_to_children(re.sub(r"^#{1,6} ", "", block)),
                )
            case BlockType.QUOTE:
                node = ParentNode(
                    tag="blockquote",
                    children=text_to_children(re.sub(r"\>\s*", "", block)),
                )
            case BlockType.UNORDERED_LIST:
                children = text_to_children(re.sub(r"\-\s*", "", block), is_list=True)
                node = ParentNode(tag="ul", children=children)
            case BlockType.ORDERED_LIST:
                children = text_to_children(re.sub(r"\d.\s*", "", block), is_list=True)
                node = ParentNode(tag="ol", children=children)
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                node = ParentNode(tag="p", children=text_to_children(block))
            case BlockType.CODE:
                block = block[4:-3]
                codenode = LeafNode(tag="code", value=block)
                node = ParentNode(tag="pre", children=[codenode])
        nodes.append(node)
    parent = ParentNode(tag="div", children=nodes)
    return parent


def extract_title(md):
    blocks = markdown_to_blocks(md)
    for block in blocks:
        type = block_to_block_type(block)
        if type is BlockType.HEADING and block.count("#") == 1:
            s1 = block.strip("# ")
            return s1
    raise Exception("No h1 header found.")
