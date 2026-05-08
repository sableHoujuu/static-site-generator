import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "This block is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "# This block is a heading."
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "### This block is a heading."
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### This block is a heading."
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "####### This block is not a heading."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```This block is code.```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```This block is code.\n With multiple lines.\n But that should be fine.```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "``` ```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = ">This block is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> This block is a quote with a space."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = ">This block is a quote.\n>With multiple lines.\n> And mixed spaces."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = ">This block is not a quote.\nSee? There's no > symbol!"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "- This block is an unordered list."
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- This block is an unordered list.\n- With multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = (
            "- This block is an unordered list.\n-Oh, no it's not. It needs a space."
        )
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "-This block is not an unordered list."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. This block is an ordered list."
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. This block is an ordered list.\n2. With multiple lines.\n3. All the way to 3, even."
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. This block is an ordered list.\n2. With multiple lines.\n3. All the way to 3, even.\n3. Wait, didn't we just do 3?"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1.This block is not an ordered list. It needs a space."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. This block is an ordered list.\n2. With multiple lines.\n4. All the way to 4, even. Wait..."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "2. This block is an ordered list.\n3. With multiple lines.\n4. All the way to 3, even. Wait, this again? Oh..."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
