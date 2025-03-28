# Uses markdown and static files to create a static site in /public
from gencontent import generate_pages_recursive
from copystatic import static_to_public


def main():
    source: str = "static"
    destination: str = "public"
    print("Copying static files to public ...")
    static_to_public(source, destination)

    src_path: str = "content"
    template_path: str = "template.html"
    dest_path: str = "public"
    print("Generating pages ...")
    generate_pages_recursive(src_path, template_path, dest_path)


if __name__ == "__main__":
    main()
