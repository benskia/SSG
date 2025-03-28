from markdownblock import (
    markdown_to_blocks,
    block_to_blocktype,
    BlockType,
)

from textnode import (
    text_to_textnodes,
    textnode_to_htmlnode,
)

from htmlnode import (
    ParentNode,
    LeafNode,
)


# Coverts a markdown document into a single ParentNode containing all HTMLNodes
# for all segments of the document.
def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    blocks: list[str] = markdown_to_blocks(markdown)
    for block in blocks:
        blocktype: BlockType = block_to_blocktype(block)
        match blocktype:
            case BlockType.PARAGRAPH:
                children.append(create_paragraph(block))
            case BlockType.HEADING:
                children.append(create_heading(block))
            case BlockType.CODE:
                children.append(create_code(block))
            case BlockType.QUOTE:
                children.append(create_quote(block))
            case BlockType.UNORDERED_LIST:
                children.append(create_unordered_list(block))
            case BlockType.ORDERED_LIST:
                children.append(create_ordered_list(block))
    return ParentNode("div", children)


def create_paragraph(block: str) -> ParentNode:
    # HTML Paragraphs don't implement breaks like markdown does, and we should
    # probably just represent paragraph blocks as continuous text that can then
    # be styled by CSS. Breaks typically act as word separators, so we can just
    # replace newline characters with spaces.
    without_newlines = block.replace("\n", " ")
    return ParentNode("p", get_leafnodes(without_newlines))


def create_heading(block: str) -> ParentNode:
    # At this point, we know the block is a heading, so we can safely split it
    # on the first space. The first element can be used to determine the
    # heading's rank. The second element can be converted into LeafNode(s) to
    # be stored in the heading ParentNode.
    hashtags, text = block.split(maxsplit=1)
    rank: int = len(hashtags)
    return ParentNode(f"h{rank}", get_leafnodes(text))


def create_code(block: str) -> ParentNode:
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


def create_quote(block: str) -> ParentNode:
    # Blocks are multiline, so we'll have to clean up the block and recombine
    # it into a workable, continuous string we can then convert into
    # LeafNode(s).
    lines = block.split("\n")
    cleaned_lines = [line.lstrip(">").strip() for line in lines]
    clean_block = "\n".join(cleaned_lines)
    return ParentNode("blockquote", get_leafnodes(clean_block))


def create_unordered_list(block: str) -> ParentNode:
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


def create_ordered_list(block: str) -> ParentNode:
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
