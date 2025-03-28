# Uses markdown and static files to create a static site in /public
from gencontent import generate_page
from copystatic import static_to_public


def main():
    source: str = "static"
    destination: str = "public"
    static_to_public(source, destination)

    from_path: str = "content/index.md"
    template_path: str = "template.html"
    dest_path: str = "public/index.html"
    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
