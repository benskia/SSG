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
def textnode_to_htmlnode(text_node: TextNode) -> LeafNode:
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
            props = {"src": text_node.url}
            return LeafNode(text_node.text, "img", props)
        case _:
            raise Exception("text node has invalid text type")


# With a given list of TextNode (old_nodes), a delimiter ("**"), and TextType,
# splits the text of each node to create a list of new TextNodes with
# appropriate metadata.
def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        delimiter_count = node.text.count(delimiter)
        if delimiter_count == 0 or delimiter_count % 2 != 0:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        for index, text in enumerate(split_text):
            # Python splits tend to preserve splits at the beginning or end of
            # the input str by including an empty element in the output list.
            # We don't want valueless LeafNodes.
            if text == "":
                continue
            if index % 2 == 0:
                new_nodes.append(TextNode(text, node.text_type))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


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


# In a given list of TextNode (old_nodes), splits the text of each node on
# markdown images to create a list of new TextNodes with appropriate metadata.
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        node_text = node.text

        parsed_images = extract_markdown_images(node.text)
        if len(parsed_images) == 0:
            new_nodes.append(node)
            continue

        # If image(s) parsed, a successful split is guaranteed. Python's
        # split("", maxsplit=1), if guaranteed successful, likewise guarantees
        # an even number of elements in the resulting list. This means that
        # indexing at most 2 elements in split_text should be safe (read:
        # shouldn't require additional safeguards against invalid access).
        for alt_text, url in parsed_images:
            img_text = f"![{alt_text}]({url})"
            split_text = node_text.split(img_text, maxsplit=1)

            if split_text[0] != "":
                new_nodes.append(TextNode(
                    split_text[0],
                    node.text_type,
                    node.url
                ))

            new_nodes.append(TextNode(
                alt_text,
                TextType.IMAGE,
                url
            ))

            # Remove the processed text so any following images can be split
            # from the remaining text. Append any final text.
            node_text.replace(split_text[0] + img_text, "")
            if split_text[1] != "":
                new_nodes.append(TextNode(
                    split_text[1],
                    node.text_type,
                    node.url
                ))

    return new_nodes


# In a given list of TextNode (old_nodes), splits the text of each node on
# markdown links to create a list of new TextNodes with appropriate metadata.
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        node_text = node.text

        parsed_images = extract_markdown_links(node.text)
        if len(parsed_images) == 0:
            new_nodes.append(node)
            continue

        # If image(s) parsed, a successful split is guaranteed. Python's
        # split("", maxsplit=1), if guaranteed successful, likewise guarantees
        # an even number of elements in the resulting list. This means that
        # indexing at most 2 elements in split_text should be safe (read:
        # shouldn't require additional safeguards against invalid access).
        for alt_text, url in parsed_images:
            img_text = f"[{alt_text}]({url})"
            split_text = node_text.split(img_text, maxsplit=1)

            if split_text[0] != "":
                new_nodes.append(TextNode(
                    split_text[0],
                    node.text_type,
                    node.url
                ))

            new_nodes.append(TextNode(
                alt_text,
                TextType.LINK,
                url
            ))

            # Remove the processed text so any following images can be split
            # from the remaining text. Append any final text.
            node_text.replace(split_text[0] + img_text, "")
            if split_text[1] != "":
                new_nodes.append(TextNode(
                    split_text[1],
                    node.text_type,
                    node.url
                ))

    return new_nodes


# Combine all text parsing to convert a markdown string to a list of TextNodes.
def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.NORMAL)]

    for text_type, delimiter in DELIMITERS.items():
        text_nodes = split_nodes_delimiter(text_nodes, delimiter, text_type)

    with_images = split_nodes_image(text_nodes)
    return split_nodes_link(with_images)
