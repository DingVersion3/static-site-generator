import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()