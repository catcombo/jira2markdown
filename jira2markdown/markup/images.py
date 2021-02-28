import re

from pyparsing import Combine, Optional, ParseResults, ParserElement, PrecededBy, Regex, SkipTo, StringStart, Word, \
    printables


class Image:
    def action(self, tokens: ParseResults) -> str:
        return f"![{tokens.url}]({tokens.url})"

    @property
    def expr(self) -> ParserElement:
        return (StringStart() | PrecededBy(Regex(r"\W", flags=re.UNICODE), retreat=1)) + Combine(
            "!"
            + Word(printables + " ", min=3, excludeChars="|!").setResultsName("url")
            + Optional("|")
            + SkipTo("!", failOn="\n") + "!",
        ).setParseAction(self.action)
