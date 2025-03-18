import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(
            "h2",
            "Howdy",
            None,
            {"class": "greeting", "href": "test://test.org"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="test://test.org"'
        )

    def test_values(self):
        child = HTMLNode("p")
        node = HTMLNode(
            "div",
            "Wowee",
            child,
            {"font": "arial"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Wowee")
        self.assertEqual(node.children, child)
        self.assertEqual(node.props, {"font": "arial"})

    def test_repr(self):
        node = HTMLNode(
            "div",
            "Wowee",
            None,
            None
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(div, Wowee, None, None)"
        )


if __name__ == "__main__":
    unittest.main()
