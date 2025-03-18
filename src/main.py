# Reads markdown and template files to output static site files.
from textnode import (
    TextNode,
    TextType
)
from htmlnode import (
    HTMLNode
)


def main():
    textnode = TextNode(
        "this is some anchor text",
        TextType.LINK,
        "test://test.org"
    )
    htmlnode = HTMLNode(
        "p",
        "this is filler text",
        [HTMLNode(), HTMLNode()],
        {"href": "test://test.org", "font": "calibra"}
    )

    print(textnode)
    print(htmlnode)


if __name__ == "__main__":
    main()
