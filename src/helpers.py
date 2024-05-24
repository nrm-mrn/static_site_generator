import os, shutil, re
from markdown_blocks import md_to_html


def copy_content(source_path, target_path):
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    os.mkdir(target_path)
    for obj in os.listdir(source_path):
        obj_path = os.path.join(source_path, obj)
        if os.path.isfile(obj_path):
            shutil.copy(obj_path, target_path)
        else:
            new_target_path = os.path.join(target_path, obj)
            copy_content(obj_path, new_target_path)


def extract_title(markdown: str) -> str:
    title = re.match(r"(?:^# {1})(.+)", markdown).group(1)
    if not title:
        raise ValueError(f"No h1 for title found in markdown file {markdown}")
    return title


def write_to_file(dest_path: str, content: str):
    (directory, target_file) = os.path.split(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, target_file), "w", encoding="utf-8") as f:
        f.write(content)
        f.close()


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page\nfrom {from_path}\nto {dest_path}\nusing {template_path}")

    with open(from_path, "r", encoding="UTF-8") as f:
        md_content = f.read()
        f.close()

    with open(template_path, "r", encoding="UTF-8") as f:
        template = f.read()
        f.close()

    md_title = extract_title(md_content)

    html_content = md_to_html(md_content).to_html()

    inserted_title = template.replace("{{ Title }}", md_title)
    html_doc = inserted_title.replace("{{ Content }}", html_content)

    write_to_file(dest_path, html_doc)


def generate_pages_recursively(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Content path {dir_path_content} is empty")
    for obj in os.listdir(dir_path_content):
        cur_path = os.path.join(dir_path_content, obj)
        if os.path.isfile(cur_path) and obj.endswith(".md"):
            filename = obj[:-3] + ".html"
            dest_path = os.path.join(dest_dir_path, filename)
            generate_page(cur_path, template_path, dest_path)
        else:
            new_path = cur_path
            dest_path = os.path.join(dest_dir_path, obj)
            generate_pages_recursively(new_path, template_path, dest_path)
