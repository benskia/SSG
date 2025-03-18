# Models textnodes (any text-type html object)

from enum import Enum


class TextType(Enum):
    NORMAL = "normal",
    BOLD = "bold",
    ITALIC = "italic",
    CODE = "code",


class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str):
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
        txt = self.text
        typ = self.text_type.value
        url = self.url
        return f"TextNode({txt}, {typ}, {url})"
