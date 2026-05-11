import os
import shutil

from textnode import TextNode, TextType


def copy_dir(source, dest):
    abs_dest = os.path.abspath(dest)
    abs_source = os.path.abspath(source)
    if os.path.exists(abs_dest):
        shutil.rmtree(abs_dest)
        print("DELETING")
    os.mkdir(abs_dest)
    files = os.listdir(abs_source)
    for file in files:
        path = os.path.join(abs_source, file)
        if os.path.isfile(path):
            shutil.copy(path, os.path.join(dest, file))
            continue
        if os.path.isdir(path):
            copy_dir(path, os.path.join(abs_dest, file))


def main():
    object = TextNode("yeah", "image", "yep")
    copy_dir("./static", "./public")


main()
