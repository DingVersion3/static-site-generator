from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # code
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ordered list
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH