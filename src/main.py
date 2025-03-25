# Uses markdown and static files to create a static site in /public
from os import (
    path,
    listdir,
    mkdir,
)
from shutil import (
    copy,
    rmtree,
)
# from sys import (
#     exit,
# )

from markdownblock import extract_title
from textmarkdown import markdown_to_html_node


def main():
    source: str = "static"
    destination: str = "public"

    # If user reverses the args, they could mistakenly delete all the static
    # files they prepared for this job. Make sure they want this. Currently
    # does nothing because directories are hard-coded.
    # src_dst_print = f"Source: {source}\nDestination: {destination}\n"
    # prompt = "This will result in deletion of files/dirs currently at the \
    #     destination.\nContinue? (y/N) "
    # confirmation = input(src_dst_print + prompt)
    # if not confirmation.lower() == "y":
    #     print("Exiting program without copying...")
    #     exit(0)

    static_to_public(source, destination)

    from_path: str = "content/index.md"
    template_path: str = "template.html"
    dest_path: str = "public/index.html"
    generate_page(from_path, template_path, dest_path)


# Copies the contents of /statis to /public after deleting everything in
# /public.
def static_to_public(src: str, dst: str) -> None:
    if not path.exists(src):
        print(f"Source, {src}, doesn't exist. Stopping")
        return
    if path.exists(dst):
        print(f"Destination already exists. Deleting {dst}")
        rmtree(dst)
    print(f"Creating new {dst} directory")
    mkdir("public")

    # shutil.copy() works on single files, and we must check each listdir()
    # item to see if it's a directory for mkdir() or file for copy(). We'll
    # do this recursively, so here's a helper function to avoid re-making
    # our destination directory over and over.
    def copy_helper(src: str, dst: str) -> None:
        items: list[str] = listdir(src)
        for item in items:
            current_src: str = path.join(src, item)
            current_dst: str = path.join(dst, item)
            if path.isfile(current_src):
                print(f"Found file. Copying {current_src} to {current_dst}")
                copy(current_src, current_dst)
            else:
                print(f"Found directory. Creating {current_dst}")
                mkdir(current_dst)
                print(f"Starting crawl through next directory {current_src}")
                copy_helper(current_src, current_dst)

    print(f"Starting crawl through source {src}...")
    copy_helper(src, dst)


# Reads the markdown file at from_path and, using the template, populates the
# {{ Content }} tag with HTML generated using the markdown document.
def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} \
            using {template_path}")

    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    content = markdown_to_html_node(md).to_html()
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


if __name__ == "__main__":
    main()
