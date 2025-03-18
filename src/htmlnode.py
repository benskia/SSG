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

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        txt = self.text
        typ = self.text_type.value[0]
        url = self.url
        return f"TextNode({txt}, {typ}, {url})"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html_props = ""
        for prop, value in self.props.items():
            html_props += f' {prop}: "{value}"'
        return html_props
