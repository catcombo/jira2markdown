from pyparsing import Combine, ParseResults, ParserElement, StringStart, Word

from jira2markdown.markup.base import AbstractMarkup


class Headings(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return "#" * int(tokens[0][1]) + " "

    @property
    def expr(self) -> ParserElement:
        return ("\n" | StringStart()) \
            + Combine(Word("h", "123456", exact=2) + ". ").setParseAction(self.action)
