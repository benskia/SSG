from enum import Enum


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


# Pulls the title (# / H1) from a markdown document. Raises an exception when
# no title is found.
def extract_title(markdown: str) -> str:
    heading = markdown_to_blocks(markdown)[0]
    if not heading.startswith("# "):
        raise Exception("Markdown document must start with a title as H1 (#)")
    return heading.lstrip("#").strip()
