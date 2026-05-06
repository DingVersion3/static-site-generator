from static import copy_static
from textnode import TextNode, TextType
from generate_page import generate_page, generate_pages_recursive

def main():
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")
main()