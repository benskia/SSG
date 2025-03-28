from os import listdir, mkdir, path
from shutil import copy, rmtree


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
