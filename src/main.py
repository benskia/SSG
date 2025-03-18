# Reads markdown and template files to output static site files.
from textnode import (
    TextNode,
    TextType as tt
)


def main():
    node = TextNode("this is some anchor text", tt.LINK, "test://test.org")
    print(node)


if __name__ == "__main__":
    main()
