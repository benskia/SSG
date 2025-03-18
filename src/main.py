# Reads markdown and template files to output static site files.
from textnode import (
    TextNode,
    TextType
)


def main():
    node = TextNode(
        "this is some anchor text",
        TextType.LINK,
        "test://test.org"
    )
    print(node)


if __name__ == "__main__":
    main()
