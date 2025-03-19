# Models htmlnodes (element tags)

class HTMLNode():
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict[str:str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html_props = ""
        if not self.props:
            return html_props
        for prop, value in self.props.items():
            html_props += f' {prop}="{value}"'
        return html_props


class LeafNode(HTMLNode):
    def __init__(
        self,
        value: str,
        tag: str | None = None,
        props: dict[str:str] | None = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("all leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: dict[str:str] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("all parent nodes must have a tag")
        if not self.children:
            raise ValueError("all parent nodes must have children")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
