from markdown_to_html import markdown_to_html_node
import unittest
from generate_page import extract_title

class TestMarkdown(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_with_content(self):
        self.assertEqual(extract_title("# My Title\n\nsome content"), "My Title")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello   "), "Hello")

    def test_extract_title_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Not an h1\n\nsome content")