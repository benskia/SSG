import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
