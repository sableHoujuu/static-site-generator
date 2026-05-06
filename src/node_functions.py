# Functions too general to put in any one node file, because they can act on multiple node types
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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images == []:  # No images, we go on
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for i in range(len(images)):
            sections = remaining_text.split(f"![{images[i][0]}]({images[i][1]})", 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if links == []:  # No links, we go on
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for i in range(len(links)):
            sections = remaining_text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
