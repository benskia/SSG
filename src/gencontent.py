from os import mkdir, path

from markdownblock import markdown_to_htmlnode, markdown_to_blocks


# Reads the markdown file at from_path and, using the template, populates the
# {{ Content }} tag with HTML generated using the markdown document.
def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    msg = f"Generating page from {from_path}"
    msg += f" to {dest_path}"
    msg += f" using {template_path}"
    print(msg)

    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    content = markdown_to_htmlnode(md).to_html()
    title = extract_title(md)
    with_title = template.replace("{{ Title }}", title)
    html = with_title.replace("{{ Content }}", content)

    current_path = ""
    for dir in dest_path.split("/"):
        if dir == "":
            continue
        current_path += dir
        if not path.exists(current_path):
            mkdir(current_path)

    with open(dest_path, "w") as f:
        f.write(html)


# Pulls the title (# / H1) from a markdown document. Raises an exception when
# no title is found. Expects Google's standard for document layout (the title
# is always the first line in the document).
def extract_title(markdown: str) -> str:
    heading = markdown_to_blocks(markdown)[0]
    if not heading.startswith("# "):
        raise ValueError("Markdown document must start with a title as H1 (#)")
    return heading[2:].strip()
