from textnode import TextNode, TextType

def main():
    node = TextNode("anchor text", TextType.LINK, "https://boot.dev")
    print(node)

main()