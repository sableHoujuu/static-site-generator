# Functions that work with raw markdown

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


def text_to_children(text):
    children = []
    textnodes = text_to_textnodes(text)
    for node in textnodes:
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
                    tag=f"h{header_num}", children=text_to_children(block)
                )
            case BlockType.QUOTE:
                node = ParentNode(tag="blockquote", children=text_to_children(block))
            case BlockType.UNORDERED_LIST:
                children = text_to_children(block)
                for child in children:
                    child.tag = "li"
                node = ParentNode(tag="ul", children=children)
            case BlockType.ORDERED_LIST:
                children = text_to_children(block)
                for child in children:
                    child.tag = "li"
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
