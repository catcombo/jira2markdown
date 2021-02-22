from pyparsing import Combine, Optional, ParseResults, ParserElement, SkipTo, Word, printables

from jira2markdown.tokens import NotUnicodeAlphaNum


class Image:
    def action(self, tokens: ParseResults) -> str:
        return f"![{tokens.url}]({tokens.url})"

    @property
    def expr(self) -> ParserElement:
        return NotUnicodeAlphaNum() + Combine(
            "!"
            + Word(printables + " ", min=3, excludeChars="|!").setResultsName("url")
            + Optional("|")
            + SkipTo("!", failOn="\n") + "!",
        ).setParseAction(self.action)
