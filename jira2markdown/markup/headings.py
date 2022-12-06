from pyparsing import Combine, LineEnd, LineStart, Optional, ParserElement, ParseResults, SkipTo, StringEnd, White, Word

from jira2markdown.markup.base import AbstractMarkup


class Headings(AbstractMarkup):
    is_inline_element = False

    def action(self, tokens: ParseResults) -> str:
        return "#" * int(tokens.level[1]) + " " + self.inline_markup.transform_string(tokens.text)

    @property
    def expr(self) -> ParserElement:
        return (
            LineStart()
            + Optional(White())
            + Combine(
                Word("h", "123456", exact=2).set_results_name("level")
                + ". "
                + SkipTo(LineEnd() | StringEnd()).set_results_name("text"),
            ).set_parse_action(self.action)
        )
