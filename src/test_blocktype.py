import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("just some text"), BlockType.PARAGRAPH)

    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)

    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#nospace"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_code_missing_newline_is_paragraph(self):
        self.assertEqual(block_to_block_type("```some code```"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(block_to_block_type(">quote\n>another line"), BlockType.QUOTE)

    def test_quote_with_space(self):
        self.assertEqual(block_to_block_type("> quote line"), BlockType.QUOTE)

    def test_quote_missing_marker_is_paragraph(self):
        self.assertEqual(block_to_block_type(">quote\nnot a quote"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item one\n- item two"), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("-item\n-item"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start_is_paragraph(self):
        self.assertEqual(block_to_block_type("2. second\n3. third"), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_order_is_paragraph(self):
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()