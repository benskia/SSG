import unittest

from markdownblocks import markdown_to_blocks


class TestMarkdownBlocks(unittest.TestCase):

    def test_markdown_to_blocks_1(self):
        markdown = '''
This is a **bolded** paragraph.
This is another paragraph with _italic_ text and `code` here.
This is the same paragraph on a new line.
- This is a list
- with items
'''
        result = markdown_to_blocks(markdown)
        expect = [
            "This is a **bolded** paragraph.\nThis is another paragraph with _italic_ text and `code` here.\nThis is the same paragraph on a new line.\n- This is a list\n- with items",
        ]
        self.assertEqual(result, expect)

    def test_markdown_to_blocks_3(self):
        markdown = '''
This is a **bolded** paragraph.

This is another paragraph with _italic_ text and `code` here.
This is the same paragraph on a new line.

- This is a list
- with items
'''
        result = markdown_to_blocks(markdown)
        expect = [
            "This is a **bolded** paragraph.",
            "This is another paragraph with _italic_ text and `code` here.\nThis is the same paragraph on a new line.",
            "- This is a list\n- with items",
        ]
        self.assertEqual(result, expect)
