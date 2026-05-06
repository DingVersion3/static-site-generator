from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes, markdown_to_blocks
from blocktype import BlockType, block_to_block_type


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        children.append(node)
    return ParentNode("div", children)


def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError(f"unknown block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]


def paragraph_to_html_node(block):
    # join lines into a single line
    lines = block.split("\n")
    text = " ".join(lines)
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]  # skip the "# " prefix
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    # strip the opening "```\n" and closing "```"
    text = block[4:-3]
    text_node = TextNode(text, TextType.CODE)
    code_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped = [line.lstrip(">").strip() for line in lines]
    text = " ".join(stripped)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    items = [ParentNode("li", text_to_children(line[2:])) for line in lines]
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        # strip "1. ", "2. " etc
        text = line.split(". ", 1)[1]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)