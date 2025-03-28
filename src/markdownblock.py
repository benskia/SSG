from enum import Enum

from htmlnode import ParentNode, LeafNode
from textnode import text_to_textnodes, textnode_to_htmlnode


class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDERED_LIST = "ul",
    ORDERED_LIST = "ol",


# Breaks a given markdown document into blocks - stripped of surrounding
# whitespace.
def markdown_to_blocks(markdown: str) -> list[str]:
    split_markdown: list[str] = markdown.split("\n\n")

    # We expect all LeafNodes to have a value, so blocks should not be empty.
    blocks: list[str] = []
    for block in split_markdown:
        if block != "":
            blocks.append(block.strip())
    return blocks


def block_to_blocktype(block: str) -> BlockType:
    lines = block.split("\n")
    # To hedge against processing large blocks repeatedly, we can start by
    # checking the first character.
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        for i, line in enumerate(lines):
            if not line.startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


# Coverts a markdown document into a single ParentNode containing all HTMLNodes
# for all segments of the document.
def markdown_to_htmlnode(markdown: str) -> ParentNode:
    children = []
    blocks: list[str] = markdown_to_blocks(markdown)
    for block in blocks:
        children.append(block_to_htmlnode(block))
    return ParentNode("div", children)


# Returns an appropriate ParentNode for the given block.
def block_to_htmlnode(block: str) -> ParentNode:
    blocktype: BlockType = block_to_blocktype(block)
    match blocktype:
        case BlockType.PARAGRAPH:
            return paragraph_to_htmlnode(block)
        case BlockType.HEADING:
            return heading_to_htmlnode(block)
        case BlockType.CODE:
            return code_to_htmlnode(block)
        case BlockType.QUOTE:
            return quote_to_htmlnode(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_htmlnode(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_htmlnode(block)


def paragraph_to_htmlnode(block: str) -> ParentNode:
    # HTML Paragraphs don't implement breaks like markdown does, and we should
    # probably just represent paragraph blocks as continuous text that can then
    # be styled by CSS. Breaks typically act as word separators, so we can just
    # replace newline characters with spaces.
    without_newlines = block.replace("\n", " ")
    return ParentNode("p", get_leafnodes(without_newlines))


def heading_to_htmlnode(block: str) -> ParentNode:
    # At this point, we know the block is a heading, so we can safely split it
    # on the first space. The first element can be used to determine the
    # heading's rank. The second element can be converted into LeafNode(s) to
    # be stored in the heading ParentNode.
    hashtags, text = block.split(maxsplit=1)
    rank: int = len(hashtags)
    return ParentNode(f"h{rank}", get_leafnodes(text))


def code_to_htmlnode(block: str) -> ParentNode:
    # Code blocks can be represented as a code LeafNode within a pre ParentNode
    # (preformatted). Code blocks don't render inline formatting. Given that
    # this is a code block, we expect it to be fenced in - not inline. Because
    # these are preformatted blocks, we must be careful when splitting/joining
    # on newlines as we might lose any that split to empty elements (such as
    # at the beginning and end of the block)
    lines: list[str] = block.split("\n")
    code: str = "\n".join(lines[1:-1]) + "\n"
    code_node = LeafNode(code, "code")
    return ParentNode("pre", [code_node])


def quote_to_htmlnode(block: str) -> ParentNode:
    # Blocks are multiline, so we'll have to clean up the block and recombine
    # it into a workable, continuous string we can then convert into
    # LeafNode(s).
    lines = block.split("\n")
    cleaned_lines = [line.lstrip(">").strip() for line in lines]
    clean_block = "\n".join(cleaned_lines)
    return ParentNode("blockquote", get_leafnodes(clean_block))


def unordered_list_to_htmlnode(block: str) -> ParentNode:
    # Unordered lists can be represented as a single 'ul' ParentNode containing
    # one or more 'li' ParentNode(s) that each have their progeny of LeafNodes.
    # Because we're representing multiple generations, we want to avoid
    # recombining the entire block back together after we clean up the markdown
    # tags ("- ").
    lines = block.split("\n")
    cleaned_lines = [line[2:] for line in lines]
    list_items = []
    for line in cleaned_lines:
        list_items.append(ParentNode("li", get_leafnodes(line)))
    return ParentNode("ul", list_items)


def ordered_list_to_htmlnode(block: str) -> ParentNode:
    # Ordered lists can be represented as a single 'ol' ParentNode containing
    # one or more 'li' ParentNode(s) that each have their progeny of LeafNodes.
    # Because HTML sorts out the numbering via the 'ol' tag, we need only
    # concern ourselves with cleaning up each line and not with numbering each
    # of the list items.
    lines = block.split("\n")
    cleaned_lines = [line[3:] for line in lines]
    list_items = []
    for line in cleaned_lines:
        list_items.append(ParentNode("li", get_leafnodes(line)))
    return ParentNode("ol", list_items)


def get_leafnodes(s: str) -> list[LeafNode]:
    leafnodes = []
    textnodes = text_to_textnodes(s)
    for textnode in textnodes:
        leafnodes.append(textnode_to_htmlnode(textnode))
    return leafnodes
