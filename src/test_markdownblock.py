import unittest

from markdownblock import (
    markdown_to_blocks,
    block_to_blocktype,
    BlockType,
    extract_title,
)


class TestMarkdownBlocks(unittest.TestCase):

    # markdown_to_blocks()
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

    # block_to_blocktype()
    def test_blocktype_paragraph(self):
        result_1 = block_to_blocktype("a block of text")
        result_2 = block_to_blocktype("")
        expect = BlockType.PARAGRAPH
        self.assertEqual(result_1, expect)
        self.assertEqual(result_2, expect)

    def test_blocktype_heading(self):
        result_1 = block_to_blocktype("# H1")
        result_2 = block_to_blocktype("## H2")
        result_3 = block_to_blocktype("### H3")
        result_4 = block_to_blocktype("#### H4")
        result_5 = block_to_blocktype("##### H5")
        result_6 = block_to_blocktype("###### H6")
        result_fail_1 = block_to_blocktype("####### H7?")
        result_fail_2 = block_to_blocktype("#H1! right?")
        expect_success = BlockType.HEADING
        expect_fail = BlockType.PARAGRAPH
        self.assertEqual(result_1, expect_success)
        self.assertEqual(result_2, expect_success)
        self.assertEqual(result_3, expect_success)
        self.assertEqual(result_4, expect_success)
        self.assertEqual(result_5, expect_success)
        self.assertEqual(result_6, expect_success)
        self.assertEqual(result_fail_1, expect_fail)
        self.assertEqual(result_fail_2, expect_fail)

    def test_blocktype_code(self):
        code_block = """
```
some fence-in
code in a
block
```
        """
        not_code_block = """
``
not code
fenced-in
in double-backticks
``
        """
        not_code_inline = "```a code block?```"
        # These docstrings add newlines to the start and end. Normally,
        # markdown_to_blocks() handles this by stripping each block.
        result_success_block = block_to_blocktype(code_block.strip())
        result_fail_block = block_to_blocktype(not_code_block.strip())
        result_fail_inline = block_to_blocktype(not_code_inline)
        expect_success = BlockType.CODE
        expect_fail = BlockType.PARAGRAPH
        self.assertEqual(result_success_block, expect_success)
        self.assertEqual(result_fail_block, expect_fail)
        self.assertEqual(result_fail_inline, expect_fail)

    def test_blocktype_quote(self):
        result_success_one = block_to_blocktype(">A quoted line")
        result_success_more = block_to_blocktype(
            ">A quoted line\n>Another one\n>And another")
        result_fail = block_to_blocktype(
            ">This one is right\nBut this one is wrong")
        expect_success = BlockType.QUOTE
        expect_fail = BlockType.PARAGRAPH
        self.assertEqual(result_success_one, expect_success)
        self.assertEqual(result_success_more, expect_success)
        self.assertEqual(result_fail, expect_fail)

    def test_blocktype_unordered_list(self):
        result_success_one = block_to_blocktype("- a list item")
        result_success_more = block_to_blocktype(
            "- one item\n- two items\n- three items")
        result_fail_one = block_to_blocktype("-no space here?")
        result_fail_more = block_to_blocktype("- right\n-wrong\n- right")
        expect_success = BlockType.UNORDERED_LIST
        expect_fail = BlockType.PARAGRAPH
        self.assertEqual(result_success_one, expect_success)
        self.assertEqual(result_success_more, expect_success)
        self.assertEqual(result_fail_one, expect_fail)
        self.assertEqual(result_fail_more, expect_fail)

    def test_blocktype_ordered_list(self):
        result_success_one = block_to_blocktype("1. a list item")
        result_success_more = block_to_blocktype(
            "1. one item\n2. two items\n3. three items")
        result_fail_space_one = block_to_blocktype("1.no space here?")
        result_fail_space_more = block_to_blocktype("1. right\n2.wrong\n")
        result_fail_num_one = block_to_blocktype("3.wrong starting num")
        result_fail_num_more = block_to_blocktype("1. right\n3. wrong")
        expect_success = BlockType.ORDERED_LIST
        expect_fail = BlockType.PARAGRAPH
        self.assertEqual(result_success_one, expect_success)
        self.assertEqual(result_success_more, expect_success)
        self.assertEqual(result_fail_space_one, expect_fail)
        self.assertEqual(result_fail_space_more, expect_fail)
        self.assertEqual(result_fail_num_one, expect_fail)
        self.assertEqual(result_fail_num_more, expect_fail)

    # extract_title()
    def test_title(self):
        result = extract_title("# Title")
        expect = "Title"
        self.assertEqual(result, expect)

    def test_title_missing(self):
        md = "## Sub-heading\n\nSome `code` here"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_title_order(self):
        md = "## Sub-heading\n\n# Title"
        with self.assertRaises(Exception):
            extract_title(md)
