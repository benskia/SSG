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
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks]


def block_to_blocktype(block: str) -> BlockType:
    if len(block) == 0:
        return BlockType.PARAGRAPH

    # To hedge against processing large blocks repeatedly, we can start by
    # checking the first character.
    match block[0]:
        case "#":
            if is_heading(block):
                return BlockType.HEADING
        case "`":
            if is_code(block):
                return BlockType.CODE
        case ">":
            if is_quote(block):
                return BlockType.QUOTE
        case "-":
            if is_unordered_list(block):
                return BlockType.UNORDERED_LIST
        case "1":
            if is_ordered_list(block):
                return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


# A heading is a continuous string of "#" (up to 6) followed by a space.
def is_heading(s: str) -> bool:
    hashtags = s.split(maxsplit=1)[0]
    size = len(hashtags)
    if size < 1 or 6 < size:
        return False
    for ch in hashtags:
        if ch != "#":
            return False
    return True


# Code blocks must start and end with 3 backticks (`).
def is_code(s: str) -> bool:
    if len(s) < 6:
        return False
    for ch in s[:3]:
        if ch != "`":
            return False
    for ch in s[-3:]:
        if ch != "`":
            return False
    return True


# Every line in a quote must start with ">".
def is_quote(s: str) -> bool:
    lines = s.split("\n")
    for line in lines:
        if len(line) == 0 or line[0] != ">":
            return False
    return True


# Every line in an unordered list must start with "-" and a space.
def is_unordered_list(s: str) -> bool:
    lines = s.split("\n")
    for line in lines:
        if len(line) < 2 or line[:2] != "- ":
            return False
    return True


# Every line in an ordered list must start with numbers incrementing from 1
# a "." and a space.
def is_ordered_list(s: str) -> bool:
    lines = s.split("\n")
    for i, line in enumerate(lines):
        if len(line) < 3:
            return False
        if line[0] != f"{i+1}":
            return False
        if line[1:3] != ". ":
            return False
    return True
