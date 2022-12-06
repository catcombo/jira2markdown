import re

from pyparsing import (
    Combine,
    Optional,
    ParserElement,
    ParseResults,
    PrecededBy,
    Regex,
    SkipTo,
    StringStart,
    Word,
    printables,
)

from jira2markdown.markup.base import AbstractMarkup


class Image(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return f"![{tokens.url}]({tokens.url})"

    @property
    def expr(self) -> ParserElement:
        return (StringStart() | PrecededBy(Regex(r"\W", flags=re.UNICODE), retreat=1)) + Combine(
            "!"
            + Word(printables + " ", min=3, exclude_chars="|!").set_results_name("url")
            + Optional("|")
            + SkipTo("!", fail_on="\n")
            + "!",
        ).set_parse_action(self.action)
