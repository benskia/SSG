import unittest

from textmarkdown import (
    markdown_to_html_node,
)


class TestTextToMarkdown(unittest.TestCase):

    def test_paragraph(self):
        md = """
A simple paragraph
        """
        result = markdown_to_html_node(md).to_html()
        expect = "<div><p>A simple paragraph</p></div>"
        self.assertEqual(result, expect)

    def test_paragraphs(self):
        md = """
One paragraph

Two paragraphs
        """
        result = markdown_to_html_node(md).to_html()
        expect = "<div><p>One paragraph</p><p>Two paragraphs</p></div>"
        self.assertEqual(result, expect)

    def test_paragraphs_with_inline(self):
        md = """
A **bolded** paragraph

An _italicized_ paragraph

A `coded` paragraph
Additional text
        """
        result = markdown_to_html_node(md).to_html()
        expect = "<div><p>A <b>bolded</b> paragraph</p><p>An <i>italicized</i> paragraph</p><p>A <code>coded</code> paragraph Additional text</p></div>"
        self.assertEqual(result, expect)

    def test_codeblock(self):
        md = """
```
Some **bolded** code
Within a _code block_
```
        """
        result = markdown_to_html_node(md).to_html()
        expect = "<div><pre><code>Some **bolded** code\nWithin a _code block_\n</code></pre></div>"
        self.assertEqual(result, expect)

    def test_paragraphs_newlines(self):
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

    def test_codeblock_sample(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
