class TextNode:

    def __init__(self, text:str, text_type:str, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_TextNode):
        if (
            self.text == other_TextNode.text and \
            self.text_type == other_TextNode.text_type and \
            self.url == other_TextNode.url
            ):
            return True
        return False

    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
