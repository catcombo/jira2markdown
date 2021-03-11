import re

from pyparsing import CaselessLiteral, Char, Combine, FollowedBy, Literal, Optional, ParseResults, ParserElement, \
    PrecededBy, QuotedString, Regex, SkipTo, StringEnd, StringStart, Suppress, White, Word, alphas, hexnums, nums, \
    replaceWith

from jira2markdown.markup.base import AbstractMarkup
from jira2markdown.markup.images import Image
from jira2markdown.markup.links import Attachment, Link, Mention


class QuotedElement(AbstractMarkup):
    TOKEN = ""
    QUOTE_CHAR = ""
    END_QUOTE_CHAR = ""

    def action(self, tokens: ParseResults) -> str:
        return self.QUOTE_CHAR \
            + self.inline_markup.transformString(tokens[0]) \
            + (self.END_QUOTE_CHAR or self.QUOTE_CHAR)

    def get_ignore_expr(self) -> ParserElement:
        return Color(**self.init_kwargs).expr

    @property
    def expr(self) -> ParserElement:
        NON_ALPHANUMS = Regex(r"\W", flags=re.UNICODE)
        TOKEN = Suppress(self.TOKEN)
        IGNORE = White() + TOKEN | self.get_ignore_expr()
        ELEMENT = Combine(
            TOKEN
            + (~White() & ~Char(self.TOKEN))
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN
            + FollowedBy(NON_ALPHANUMS | StringEnd()),
        )

        return (StringStart() | PrecededBy(NON_ALPHANUMS, retreat=1)) \
            + Combine(ELEMENT.setParseAction(self.action) + Optional(~ELEMENT, default=" "))


class Bold(QuotedElement):
    TOKEN = "*"
    QUOTE_CHAR = "**"


class Strikethrough(QuotedElement):
    TOKEN = "-"
    QUOTE_CHAR = "~~"

    def get_ignore_expr(self) -> ParserElement:
        return Color(**self.init_kwargs).expr \
            | Attachment(**self.init_kwargs).expr \
            | Mention(**self.init_kwargs).expr \
            | Link(**self.init_kwargs).expr \
            | Image(**self.init_kwargs).expr


class Underline(QuotedElement):
    TOKEN = "+"


class InlineQuote(QuotedElement):
    TOKEN = "??"
    QUOTE_CHAR = "<q>"
    END_QUOTE_CHAR = "</q>"


class Superscript(QuotedElement):
    TOKEN = "^"
    QUOTE_CHAR = "<sup>"
    END_QUOTE_CHAR = "</sup>"

    def get_ignore_expr(self) -> ParserElement:
        return Color(**self.init_kwargs).expr | Attachment(**self.init_kwargs).expr


class Subscript(QuotedElement):
    TOKEN = "~"
    QUOTE_CHAR = "<sub>"
    END_QUOTE_CHAR = "</sub>"

    def get_ignore_expr(self) -> ParserElement:
        return Color(**self.init_kwargs).expr | Mention(**self.init_kwargs).expr


class Color(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        text = self.inline_markup.transformString(tokens.text)

        if tokens.red and tokens.green and tokens.blue:
            color = f"#{int(tokens.red):x}{int(tokens.green):x}{int(tokens.blue):x}"
        else:
            color = tokens.color[0]

        if len(text.strip()) > 0:
            return f'<font color="{color}">{text}</font>'
        else:
            return text

    @property
    def expr(self) -> ParserElement:
        INTENSITY = Word(nums)
        ALPHA = Word(nums + ".")
        SEP = "," + Optional(White())
        RGBA = CaselessLiteral("rgba(") \
            + INTENSITY.setResultsName("red") + SEP \
            + INTENSITY.setResultsName("green") + SEP \
            + INTENSITY.setResultsName("blue") + SEP \
            + ALPHA + ")"

        COLOR = Word("#", hexnums) ^ Word(alphas) ^ RGBA
        expr = Combine(
            "{color:" + COLOR.setResultsName("color") + "}"
            + SkipTo("{color}").setResultsName("text")
            + "{color}",
        )

        return expr.setParseAction(self.action)


class Quote(AbstractMarkup):
    is_inline_element = False

    @property
    def expr(self) -> ParserElement:
        return ("\n" | StringStart()) + Literal("bq. ").setParseAction(replaceWith("> "))


class BlockQuote(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        text = self.markup.transformString("\n".join([
            line.lstrip() for line in tokens[0].strip().splitlines()
        ]))
        return "\n".join([f"> {line}" for line in text.splitlines()])

    @property
    def expr(self) -> ParserElement:
        return QuotedString("{quote}", multiline=True).setParseAction(self.action)


class Monospaced(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return f"`{tokens[0]}`"

    @property
    def expr(self) -> ParserElement:
        return QuotedString("{{", endQuoteChar="}}").setParseAction(self.action)


class EscSpecialChars(AbstractMarkup):
    """
    Escapes '*' characters that are not a part of any expression grammar
    """

    @property
    def expr(self) -> ParserElement:
        return Literal("*").setParseAction(replaceWith(r"\*"))
