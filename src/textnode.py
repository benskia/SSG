from enum import Enum
from re import findall

from htmlnode import LeafNode


class TextType(Enum):
    NORMAL = "normal",
    BOLD = "bold",
    ITALIC = "italic",
    CODE = "code",
    LINK = "link",
    IMAGE = "image",


DELIMITERS: dict[TextType:str] = {
    TextType.BOLD: "**",
    TextType.ITALIC: "_",
    TextType.CODE: "`",
}


# Models a unit of text within the html document (any of the above TextTypes).
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


# Converts the given TextNode into a LeafNode (HTMLNode with no children).
# These represent the innermost tag of nested HTML elements that contain some
# content.
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
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


# Provided a list of TextNodes, a delimiter ("**"), and a TextType, splits the
# text for each TextNode in old_nodes, creates appropriate TextNodes for each
# segment of the text, and returns the resulting list of TextNodes.
def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) == 0:
            handle_delimiter_not_found(node, delimiter, text_type)
            return old_nodes
        if node.text.count(delimiter) % 2 != 0:
            handle_delimiter_unbalanced(node, delimiter, text_type)
            return old_nodes

        split_text = node.text.split(delimiter)
        for index, text in enumerate(split_text):
            if index % 2 == 0:
                new_nodes.append(TextNode(text, node.text_type))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


# Warning handling when split_nodes_delimiter() returns the old nodes
def handle_delimiter_not_found(
    node: TextNode,
    delimiter: str,
    text_type: TextType
):
    print("delimiter not found in text node")
    print(node)
    print(f"\tdelimiter: {delimiter}")
    print(f"\ttext type: {text_type.value[0]}")


def handle_delimiter_unbalanced(
    node: TextNode,
    delimiter: str,
    text_type: TextType
):
    print("cannot split text node on unbalanced delimiter")
    print(node)
    print(f"\tdelimiter: {delimiter}")
    print(f"\ttext type: {text_type.value[0]}")


# Parses text for markdown images, and returns a list of (anchor text, url)
# tuples - to be converted into HTMLNodes.
# Markdown image format is: ![alt text](url)
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    expression = r"!\[(.*?)\]\((.*?)\)"
    matches = findall(expression, text)

    parsed_images = []
    for match in matches:
        parsed_images.append((match[0], match[1]))

    return parsed_images


# Parses text for markdown links, and returns a list of (anchor text, url)
# tuples - to be converted into HTMLNodes.
# Markdown link format is: [anchor text](url)
# Note, there is no preceding "!"
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    expression = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = findall(expression, text)

    parsed_links = []
    for match in matches:
        parsed_links.append((match[0], match[1]))

    return parsed_links
