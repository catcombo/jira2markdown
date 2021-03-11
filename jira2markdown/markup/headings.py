from pyparsing import Combine, LineEnd, ParseResults, ParserElement, SkipTo, StringEnd, StringStart, Word

from jira2markdown.markup.base import AbstractMarkup


class Headings(AbstractMarkup):
    is_inline_element = False

    def action(self, tokens: ParseResults) -> str:
        return "#" * int(tokens.level[1]) + " " + self.inline_markup.transformString(tokens.text)

    @property
    def expr(self) -> ParserElement:
        return ("\n" | StringStart()) + Combine(
            Word("h", "123456", exact=2).setResultsName("level")
            + ". "
            + SkipTo(LineEnd() | StringEnd()).setResultsName("text"),
        ).setParseAction(self.action)
