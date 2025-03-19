# Reads markdown and template files to output static site files.
from textnode import (
    TextNode,
    TextType
)
from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode
)


def main():
    textnode = TextNode(
        "this is some anchor text",
        TextType.LINK,
        "test://test.org"
    )
    leafnode = LeafNode(
        "this is filler text",
        "p",
        {"href": "test://test.org", "font": "calibra"}
    )

    print(textnode)
    print(leafnode.to_html())


if __name__ == "__main__":
    main()
