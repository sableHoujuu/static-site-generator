import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(md_block: str):
    """
    Takes a single block of markdown text as input and returns whichever BlockType it is
    """
    if re.findall(r"^#{1,6} ", md_block) != []:
        return BlockType.HEADING
    if md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE
    # Past the easy ones, now we go onto the harder ones
    lines = md_block.splitlines()
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(lines[i].startswith(f"{i + 1}. ") for i in range(len(lines))):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
