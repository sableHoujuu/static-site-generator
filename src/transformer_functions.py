# Functions that take a text input and output text for use by other functions


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
