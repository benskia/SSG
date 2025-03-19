import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node
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


if __name__ == "__main__":
    unittest.main()
