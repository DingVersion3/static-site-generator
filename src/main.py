import sys
from static import copy_static
from textnode import TextNode, TextType
from generate_page import generate_page, generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "public", basepath)
main()