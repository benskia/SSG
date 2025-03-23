import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)


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

    def test_leaf_to_html(self):
        node = LeafNode("Hello, world!", "p")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("Hello, world!", "p", {"href": "test://test.org"})
        self.assertEqual(
            node.to_html(), '<p href="test://test.org">Hello, world!</p>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode("wow no tag")
        self.assertEqual(node.to_html(), "wow no tag")

    def test_to_html_with_children(self):
        child1 = LeafNode("wowee", "div2")
        node = ParentNode("div1", [child1])
        self.assertEqual(
            node.to_html(),
            "<div1><div2>wowee</div2></div1>"
        )

    def test_to_html_with_grandchildren(self):
        child2 = LeafNode("wowee", "p")
        child1 = ParentNode("div2", [child2])
        node = ParentNode("div1", [child1])
        self.assertEqual(
            node.to_html(),
            "<div1><div2><p>wowee</p></div2></div1>"
        )

    def test_to_html_with_greatgrandchildren(self):
        child3 = LeafNode("wowee", "p")
        child2 = ParentNode("div3", [child3])
        child1 = ParentNode("div2", [child2])
        node = ParentNode("div1", [child1])
        self.assertEqual(
            node.to_html(),
            "<div1><div2><div3><p>wowee</p></div3></div2></div1>"
        )

    def test_to_html_with_props(self):
        child2 = LeafNode("wowee", "p", {"font": "calibri"})
        child1 = ParentNode("div2", [child2])
        node = ParentNode("div1", [child1])
        self.assertEqual(
            node.to_html(),
            '<div1><div2><p font="calibri">wowee</p></div2></div1>'
        )


if __name__ == "__main__":
    unittest.main()
