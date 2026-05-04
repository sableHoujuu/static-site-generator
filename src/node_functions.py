# Functions too general to put in any one node file.
import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(
                "Invalid markdown syntax! There cannot be an odd number of delimiters"
            )
        sections = node.text.split(delimiter)
        for i in range(len(sections)):
            if i % 2 == 0:
                new_node = TextNode(sections[i], TextType.TEXT)
            else:
                new_node = TextNode(sections[i], text_type)
            new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.+?)\]\((.+?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.+?)\]\((.+?)\)", text)
    return matches
