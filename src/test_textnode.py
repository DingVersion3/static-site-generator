import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("click here", TextType.LINK, "https://boot.dev")
        node2 = TextNode("click here", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("world", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("click", TextType.LINK, "https://boot.dev")
        node2 = TextNode("click", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_url_defaults_to_none(self):
        node = TextNode("hello", TextType.NORMAL)
        self.assertIsNone(node.url)

    def test_not_eq_url_vs_no_url(self):
        node = TextNode("click", TextType.LINK, "https://boot.dev")
        node2 = TextNode("click", TextType.LINK)
        self.assertNotEqual(node, node2)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("a cat", TextType.IMAGE, "https://cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://cat.png", "alt": "a cat"})

    def test_invalid_type_raises(self):
        node = TextNode("oops", None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ])

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ])

    def test_split_italic(self):
        node = TextNode("This is _italic_ text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.NORMAL),
        ])

    def test_split_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_split_missing_closing_delimiter_raises(self):
        node = TextNode("This is `broken markdown", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_multiple_delimiters(self):
        node = TextNode("a `b` c `d` e", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.NORMAL),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.NORMAL),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.NORMAL),
        ])

    def test_split_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.NORMAL),
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_images_multiple(self):
    matches = extract_markdown_images(
        "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    )
    self.assertListEqual([
        ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
        ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
    ], matches)

def test_extract_markdown_images_none(self):
    matches = extract_markdown_images("no images here")
    self.assertListEqual([], matches)

def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is a link [to boot dev](https://www.boot.dev)"
    )
    self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

def test_extract_markdown_links_multiple(self):
    matches = extract_markdown_links(
        "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    )
    self.assertListEqual([
        ("to boot dev", "https://www.boot.dev"),
        ("to youtube", "https://www.youtube.com/@bootdotdev")
    ], matches)

def test_extract_markdown_links_ignores_images(self):
    matches = extract_markdown_links(
        "![image](https://img.png) and [link](https://boot.dev)"
    )
    self.assertListEqual([("link", "https://boot.dev")], matches)

def test_extract_markdown_links_none(self):
    matches = extract_markdown_links("no links here")
    self.assertListEqual([], matches)

def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.NORMAL,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual([
        TextNode("This is text with an ", TextType.NORMAL),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.NORMAL),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
    ], new_nodes)

def test_split_images_none(self):
    node = TextNode("no images here", TextType.NORMAL)
    new_nodes = split_nodes_image([node])
    self.assertListEqual([TextNode("no images here", TextType.NORMAL)], new_nodes)

def test_split_images_non_text_unchanged(self):
    node = TextNode("already bold", TextType.BOLD)
    new_nodes = split_nodes_image([node])
    self.assertListEqual([TextNode("already bold", TextType.BOLD)], new_nodes)

def test_split_links(self):
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.NORMAL,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual([
        TextNode("This is text with a link ", TextType.NORMAL),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.NORMAL),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
    ], new_nodes)

def test_split_links_none(self):
    node = TextNode("no links here", TextType.NORMAL)
    new_nodes = split_nodes_link([node])
    self.assertListEqual([TextNode("no links here", TextType.NORMAL)], new_nodes)

def test_split_links_non_text_unchanged(self):
    node = TextNode("already italic", TextType.ITALIC)
    new_nodes = split_nodes_link([node])
    self.assertListEqual([TextNode("already italic", TextType.ITALIC)], new_nodes)

def test_split_image_at_start(self):
    node = TextNode("![image](https://img.png) then text", TextType.NORMAL)
    new_nodes = split_nodes_image([node])
    self.assertListEqual([
        TextNode("image", TextType.IMAGE, "https://img.png"),
        TextNode(" then text", TextType.NORMAL),
    ], new_nodes)

def test_split_link_at_end(self):
    node = TextNode("text then [link](https://boot.dev)", TextType.NORMAL)
    new_nodes = split_nodes_link([node])
    self.assertListEqual([
        TextNode("text then ", TextType.NORMAL),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ], new_nodes)

def test_text_to_textnodes(self):
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    nodes = text_to_textnodes(text)
    self.assertListEqual([
        TextNode("This is ", TextType.NORMAL),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.NORMAL),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.NORMAL),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.NORMAL),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ], nodes)

def test_text_to_textnodes_plain(self):
    nodes = text_to_textnodes("just plain text")
    self.assertListEqual([TextNode("just plain text", TextType.NORMAL)], nodes)

def test_text_to_textnodes_bold_only(self):
    nodes = text_to_textnodes("**bold**")
    self.assertListEqual([TextNode("bold", TextType.BOLD)], nodes)

def test_text_to_textnodes_multiple_types(self):
    nodes = text_to_textnodes("**bold** and _italic_")
    self.assertListEqual([
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
    ], nodes)

def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
    ])

def test_markdown_to_blocks_extra_newlines(self):
    md = "block one\n\n\n\nblock two"
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["block one", "block two"])

def test_markdown_to_blocks_strips_whitespace(self):
    md = "  block one  \n\n  block two  "
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["block one", "block two"])

def test_markdown_to_blocks_single_block(self):
    md = "just one block"
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["just one block"])

def test_markdown_to_blocks_empty(self):
    blocks = markdown_to_blocks("")
    self.assertEqual(blocks, [])


if __name__ == "__main__":
    unittest.main()