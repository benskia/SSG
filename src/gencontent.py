from os import listdir, mkdir, path

from markdownblock import markdown_to_htmlnode, markdown_to_blocks


# Reads the markdown file at from_path and, using the template, populates the
# {{ Content }} tag with HTML generated using the markdown document.
def generate_page(
    src_path: str,
    template_path: str,
    dest_path: str,
    base_path: str
) -> None:
    msg = f"Generating page from {src_path}"
    msg += f" to {dest_path}"
    msg += f" using {template_path}"
    print(msg)

    with open(src_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    content = markdown_to_htmlnode(md).to_html()
    title = extract_title(md)
    with_title = template.replace("{{ Title }}", title)
    with_content = with_title.replace("{{ Content }}", content)
    with_base_href = with_content.replace('href="/', f'href="/{base_path}/')
    with_base_src = with_base_href.replace('src="/', f'src="/{base_path}/')

    with open(dest_path, "w") as f:
        f.write(with_base_src)


# Recursively generates public html files from provided markdown files.
def generate_pages_recursive(
    src_path: str,
    template_path: str,
    dest_path: str,
    base_path: str
) -> None:
    items: list[str] = listdir(src_path)
    for item in items:
        current_src: str = path.join(src_path, item)
        current_dest: str = path.join(dest_path, item)
        if path.isfile(current_src):
            if current_src[-2:] != "md":
                print("skipping non-markdown content file")
            html_dest: str = current_dest[:-2] + "html"
            generate_page(current_src, template_path, html_dest, base_path)
            continue
        print(f"Creating destination directory {current_dest}")
        mkdir(current_dest)
        generate_pages_recursive(
            current_src,
            template_path,
            current_dest,
            base_path
        )


# Pulls the title (# / H1) from a markdown document. Raises an exception when
# no title is found. Expects Google's standard for document layout (the title
# is always the first line in the document).
def extract_title(markdown: str) -> str:
    heading = markdown_to_blocks(markdown)[0]
    if not heading.startswith("# "):
        raise ValueError("Markdown document must start with a title as H1 (#)")
    return heading[2:].strip()
