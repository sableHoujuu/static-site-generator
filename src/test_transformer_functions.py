import unittest

from transformer_functions import markdown_to_blocks


class TestTransformerFunctions(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line






- This is a list
- with items
        """  # Excessive newline test
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        md = """"""
        self.assertEqual(markdown_to_blocks(md), [])
        md = """
This is just a single line of text with nothing special
        """
        self.assertEqual(
            markdown_to_blocks(md),
            ["This is just a single line of text with nothing special"],
        )
