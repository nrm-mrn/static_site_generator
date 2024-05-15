class HtmlNode:
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        children: list[any] | None,
        props: dict[str, str] | None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props = [""]
        for name, value in self.props.items():
            props.append(f'{name}="{value}"')
        return " ".join(props)

    def __repr__(self) -> str:
        return f"HtmlNode:\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}"


class LeafNode(HtmlNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.tag is None:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: str,
        children: list[HtmlNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("tag is not provided in parent node")
        if self.children is None:
            raise ValueError("No children in a parent node")
        children_html = ""
        props = self.props_to_html()
        for child in self.children:
            children_html += f"{child.to_html()}"
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"
