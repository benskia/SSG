import unittest

from textnode import (
    TextNode,
    TextType,
    DELIMITERS,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
)


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_uneq_url(self):
        node = TextNode(
            "This is a text node",
            TextType.BOLD,
            "test://test.org"
        )
        node2 = TextNode(
            "This is a text node",
            TextType.BOLD,
            "test://test.io"
        )
        self.assertNotEqual(node, node2)

    def test_uneq_all(self):
        node = TextNode(
            "This is a text node",
            TextType.BOLD,
            "test://test.org"
        )
        node2 = TextNode(
            "This is a different node",
            TextType.ITALIC,
            "test://test.io"
        )
        self.assertNotEqual(node, node2)

    # text_node_to_html_node()
    def test_text(self):
        node = TextNode("a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "a text node")

    def test_to_html(self):
        node = TextNode("a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            "<b>a bold text node</b>"
        )

    # split_nodes_delimiter()
    def test_split_nodes_delimiter(self):
        nodes = [TextNode("text with an _italic_ word", TextType.NORMAL)]
        result = split_nodes_delimiter(
            nodes,
            DELIMITERS[TextType.ITALIC],
            TextType.ITALIC
        )
        expect = [
            TextNode("text with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(result, expect)

    def test_multiple_splits(self):
        nodes = [
            TextNode("a `few` words with `code` format", TextType.NORMAL)]
        result = split_nodes_delimiter(
            nodes,
            DELIMITERS[TextType.CODE],
            TextType.CODE
        )
        expect = [
            TextNode("a ", TextType.NORMAL),
            TextNode("few", TextType.CODE),
            TextNode(" words with ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" format", TextType.NORMAL),
        ]
        self.assertEqual(result, expect)

    def test_ending_delimiter(self):
        nodes = [TextNode("text with ending **delimiter**", TextType.NORMAL)]
        result = split_nodes_delimiter(
            nodes,
            DELIMITERS[TextType.BOLD],
            TextType.BOLD
        )
        expect = [
            TextNode("text with ending ", TextType.NORMAL),
            TextNode("delimiter", TextType.BOLD),
            TextNode("", TextType.NORMAL),
        ]
        self.assertEqual(result, expect)

    def test_delimiter_not_found(self):
        nodes = [TextNode("a normal text node", TextType.NORMAL)]
        result = split_nodes_delimiter(
            nodes,
            DELIMITERS[TextType.BOLD],
            TextType.BOLD
        )
        self.assertEqual(result, nodes)

    def test_delimiter_unbalanced(self):
        nodes = [TextNode("a text node with **bold within?", TextType.NORMAL)]
        result = split_nodes_delimiter(
            nodes,
            DELIMITERS[TextType.BOLD],
            TextType.BOLD
        )
        self.assertEqual(result, nodes)

    # extract_markdown_images()
    def test_extract_image(self):
        text = "an ![image](test://test.org) in text"
        result = extract_markdown_images(text)
        expect = [("image", "test://test.org")]
        self.assertEqual(result, expect)

    def test_extract_images(self):
        text = "multiple ![wow1](img1.org) in ![wow2](img2.org) text"
        result = extract_markdown_images(text)
        expect = [
            ("wow1", "img1.org"),
            ("wow2", "img2.org"),
        ]
        self.assertEqual(result, expect)

    def test_extract_image_fail(self):
        text = "not an [image](test://test.org) in text"
        result = extract_markdown_images(text)
        expect = []
        self.assertEqual(result, expect)

    def test_extract_link(self):
        text = "a [link](test://test.org) in text"
        result = extract_markdown_links(text)
        expect = [("link", "test://test.org")]
        self.assertEqual(result, expect)

    def test_extract_links(self):
        text = "multiple [wow1](link1.org) in [wow2](link2.org) text"
        result = extract_markdown_links(text)
        expect = [
            ("wow1", "link1.org"),
            ("wow2", "link2.org"),
        ]
        self.assertEqual(result, expect)

    def test_extract_link_fail(self):
        text = "not a ![link](test://test.org) in text"
        result = extract_markdown_links(text)
        expect = []
        self.assertEqual(result, expect)


if __name__ == "__main__":
    unittest.main()
