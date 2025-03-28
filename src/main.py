# Uses markdown and static files to create a static site in /public .
# The page is served from a configurable root, given as argv.
from sys import argv

from gencontent import generate_pages_recursive
from copystatic import static_to_public


def main():
    basepath: str = get_basepath(argv)

    static_src: str = "static"
    dest_path: str = "docs"
    print("Copying static files to public ...")
    static_to_public(static_src, dest_path)

    content_src: str = "content"
    template_path: str = "template.html"
    print("Generating pages ...")
    generate_pages_recursive(content_src, template_path, dest_path, basepath)


def get_basepath(args: list[str]) -> str:
    if len(args) == 2:
        return args[1]

    default = "/"
    if len(args) < 2:
        print("No arg found for the server's base path.")
    elif len(args) > 2:
        print("Program expects at most 1 arg.")
    print(f"Using default basepath {default} .")
    return default


if __name__ == "__main__":
    main()
