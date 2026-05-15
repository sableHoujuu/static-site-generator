import os
import shutil
import sys

from markdown_functions import extract_title, markdown_to_html_node
from textnode import TextNode, TextType


def copy_dir(source, dest):
    abs_dest = os.path.abspath(dest)
    abs_source = os.path.abspath(source)
    if os.path.exists(abs_dest):
        shutil.rmtree(abs_dest)
    os.mkdir(abs_dest)
    files = os.listdir(abs_source)
    for file in files:
        path = os.path.join(abs_source, file)
        if os.path.isfile(path):
            shutil.copy(path, os.path.join(dest, file))
            continue
        if os.path.isdir(path):
            copy_dir(path, os.path.join(abs_dest, file))


def generate_page(from_path, template_path, dest_path, root_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    abs_from = os.path.abspath(from_path)
    with open(abs_from) as f:
        from_contents = f.read()
    abs_template = os.path.abspath(template_path)
    with open(abs_template) as f:
        template_contents = f.read()
    html_node = markdown_to_html_node(from_contents)
    html_string = html_node.to_html()
    title = extract_title(from_contents)
    final_html = (
        template_contents.replace("{{ Title }}", title)
        .replace("{{ Content }}", html_string)
        .replace('href="/', f'href="{root_path}')
        .replace('src="/', f'src="{root_path}')
    )
    abs_dest = os.path.abspath(dest_path)
    os.makedirs(os.path.dirname(abs_dest), exist_ok=True)
    with open(abs_dest, mode="w") as f:
        f.write(final_html)


def generate_site(path_to_content, dest_path, root_path):
    abs_source = os.path.abspath(path_to_content)
    for file in os.listdir(abs_source):
        abs_file = os.path.join(abs_source, file)
        if os.path.isdir(abs_file):
            generate_site(
                abs_file, f"{dest_path}/{file.replace('.md', '.html')}", root_path
            )
        elif os.path.isfile(abs_file):
            generate_page(
                abs_file,
                "template.html",
                f"{dest_path}/{file.replace('.md', '.html')}",
                root_path,
            )


def main():
    root_path = "/"
    try:
        root_path = sys.argv[1]
    except Exception as _e:
        print(f"No path provided, falling back to default {root_path}")
    copy_dir("./static", "./docs")
    generate_site("content", "docs", root_path)


main()
