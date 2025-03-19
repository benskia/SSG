# Models textnodes (any text-type html object)

from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    NORMAL = "normal",
    BOLD = "bold",
    ITALIC = "italic",
    CODE = "code",
    LINK = "link",
    IMAGE = "image",


class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value[0]}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(text_node.text)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i")
        case TextType.CODE:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            props = {"href": text_node.url}
            return LeafNode(text_node.text, "a", props)
        case TextType.IMAGE:
            props = {"src": text_node.url, "alt": text_node.text}
            return LeafNode("", "img", props)
        case _:
            raise Exception("text node has invalid text type")
