import unittest

from node_functions import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestNodeFunctions(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("This should be _italic_, preferably", TextType.TEXT)]
        expected_result = [
            TextNode("This should be ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", preferably", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "_", TextType.ITALIC), expected_result
        )
        old_nodes = [TextNode("This should be **bold**, preferably", TextType.TEXT)]
        expected_result = [
            TextNode("This should be ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", preferably", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD), expected_result
        )
        old_nodes = [TextNode("This should be 'code', preferably", TextType.TEXT)]
        expected_result = [
            TextNode("This should be ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", preferably", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "'", TextType.CODE), expected_result
        )

    def test_split_nodes_delimiter_only_text(self):
        old_nodes = [TextNode("This is just text.", TextType.TEXT) for _ in range(4)]
        expected_result = [
            TextNode("This is just text.", TextType.TEXT) for _ in range(4)
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "_", TextType.ITALIC), expected_result
        )

    def test_split_nodes_delimiter_invalid_syntax(self):
        old_nodes = [TextNode("This is an **invalid string.", TextType.TEXT)]
        self.assertRaises(
            Exception, split_nodes_delimiter, (old_nodes, "**", TextType.BOLD)
        )

    def test_split_nodes_delimiter_no_nodes(self):
        old_nodes = []
        self.assertEqual(split_nodes_delimiter(old_nodes, "", TextType.TEXT), [])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )
        text = "This is text with no images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_text(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )
        text = "This is text with no links."
        self.assertEqual(extract_markdown_links(text), [])
