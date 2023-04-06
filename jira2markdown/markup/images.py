import re
from typing import Dict, List

from pyparsing import (
    Combine,
    Literal,
    Optional,
    ParserElement,
    ParseResults,
    PrecededBy,
    Regex,
    StringStart,
    Word,
    ZeroOrMore,
    alphanums,
    printables,
)

from jira2markdown.markup.base import AbstractMarkup


class Image(AbstractMarkup):
    ALLOWED_ATTRS = ("width", "height")

    def _parse_attrs(self, attrs: List[List[str]]) -> Dict:
        return {name_value[0].lower().strip(): name_value[-1].strip() for name_value in attrs}

    def action(self, tokens: ParseResults) -> str:
        attrs_str = " ".join(
            f'{name}="{value}"'
            for name, value in self._parse_attrs(tokens.attrs or []).items()
            if name in self.ALLOWED_ATTRS
        )
        if attrs_str:
            return f'<img src="{tokens.url}" {attrs_str} />'
        else:
            return f"![{tokens.url}]({tokens.url})"

    @property
    def expr(self) -> ParserElement:
        image_attribute = (
            Word(alphanums + " ")
            + Optional(Literal("=").suppress() + Word(printables + " ", exclude_chars=",!"))
            + Optional(",").suppress()
        )
        return (StringStart() | PrecededBy(Regex(r"\W", flags=re.UNICODE), retreat=1)) + Combine(
            "!"
            + Word(printables + " ", min=3, exclude_chars="|!").set_results_name("url")
            + Optional("|" + ZeroOrMore(image_attribute.set_results_name("attrs", list_all_matches=True), stop_on="!"))
            + "!",
        ).set_parse_action(self.action)
