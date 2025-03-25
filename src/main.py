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


def main():
    source = "static"
    destination = "public"

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

    title = extract_title("# title")
    print(title)
    static_to_public(source, destination)


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
    print(f"Starting crawl through source {src}...")
    copy_helper(src, dst)


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


if __name__ == "__main__":
    main()
