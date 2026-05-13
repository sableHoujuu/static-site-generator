import os
import shutil

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


def generate_page(from_path, template_path, dest_path):
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
    final_html = template_contents.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )
    abs_dest = os.path.abspath(dest_path)
    os.makedirs(os.path.dirname(abs_dest), exist_ok=True)
    with open(abs_dest, mode="w") as f:
        f.write(final_html)


def main():
    object = TextNode("yeah", "image", "yep")
    copy_dir("./static", "./public")
    generate_page("content/index.md", "template.html", "public/index.html")


main()
