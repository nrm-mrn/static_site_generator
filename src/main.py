import os
from helpers import copy_content, generate_pages_recursively


def main():
    working_dir = os.getcwd()
    target_dir = "public"
    target_path = os.path.join(working_dir, target_dir)
    source_path = os.path.join(working_dir, "src", "static")

    copy_content(source_path, target_path)

    generate_pages_recursively(
        os.path.join(working_dir, "content"),
        os.path.join(working_dir, "template.html"),
        os.path.join(working_dir, "public"),
    )


main()
