from pyparsing import Combine, Forward, Group, LineEnd, LineStart, Literal, OneOrMore, Optional, ParseResults, \
    ParserElement, SkipTo, StringEnd, StringStart, White, ZeroOrMore

from jira2markdown.markup.images import Image
from jira2markdown.markup.links import Link, MailTo, Mention


class Table:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        lines = [line for line in tokens if len(line) > 0]
        max_columns_count = max(len(row) for row in tokens)

        # Converts multiline text to one line,
        # because markdown doesn't support multiline text in table cells
        output = [
            "|" + "|".join(
                map(
                    lambda cell: cell.replace("\n", "<br>"),
                    map(self.markup.transformString, row),
                ),
            ) + "|"
            for row in lines
        ]

        # Header row must have the maximum columns of the table
        output[0] += "|" * (max_columns_count - len(lines[0]))

        # Insert header delimiter after the first row
        output.insert(1, "|" + "-|" * max(max_columns_count, 1))

        return "\n".join(output) + "\n"

    @property
    def expr(self) -> ParserElement:
        NL = LineEnd().suppress()
        SEP = (Literal("||") | Literal("|")).suppress()
        ROW_BREAK = NL + SEP | NL + NL | StringEnd()
        IGNORE = Link(self.markup).expr | MailTo().expr | Image().expr | Mention({}).expr

        ROW = SEP + ZeroOrMore(
            SkipTo(SEP | ROW_BREAK, ignore=IGNORE) + Optional(SEP),
            stopOn=ROW_BREAK | NL + ~SEP,
        )

        EMPTY_LINE = Combine("\n" + White(" \t", min=0) + "\n")
        return ((StringStart() + Optional("\n")) ^ Optional(EMPTY_LINE, default="\n")) \
            + OneOrMore(LineStart() + Group(ROW) + NL).setParseAction(self.action) \
            + (StringEnd() | Optional(LineEnd(), default="\n"))
