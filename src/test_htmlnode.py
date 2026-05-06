import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode("a", "click here", props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html_multiple(self):
        node = HTMLNode("a", "click here", props={
            "href": "https://boot.dev",
            "target": "_blank"
        })
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("p", "hello", None, {"class": "text"})
        self.assertEqual(repr(node), "HTMLNode(p, hello, None, {'class': 'text'})")

    def test_defaults_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_raises(self):
        node = HTMLNode("p", "hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = LeafNode(None, "hello")
        self.assertEqual(node.to_html(), "hello")

    def test_to_html_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children(self):
        node = LeafNode("p", "hello")
        self.assertIsNone(node.children)

    def test_repr(self):
        node = LeafNode("p", "hello", {"class": "text"})
        self.assertEqual(repr(node), "LeafNode(p, hello, {'class': 'text'})")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_multiple_children(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_props(self):
        node = ParentNode("div", [LeafNode("p", "hello")], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p>hello</p></div>')

    def test_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("p", "hello")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children_raises(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_deeply_nested(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode("b", "deep")
                ])
            ])
        ])
        self.assertEqual(node.to_html(), "<div><section><p><b>deep</b></p></section></div>")

if __name__ == "__main__":
    unittest.main()