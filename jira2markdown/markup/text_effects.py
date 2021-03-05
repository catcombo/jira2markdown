import re

from pyparsing import CaselessLiteral, Char, Combine, LineEnd, Literal, Optional, ParseResults, ParserElement, \
    PrecededBy, QuotedString, Regex, SkipTo, StringStart, Suppress, White, Word, WordEnd, WordStart, \
    alphanums, alphas, hexnums, nums, replaceWith

from jira2markdown.markup.base import AbstractMarkup
from jira2markdown.markup.links import Attachment, Mention


class Bold(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return "**" + self.markup.transformString(tokens[0]) + "**"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("*")
        IGNORE = White() + TOKEN | Color(**self.init_kwargs).expr
        return (StringStart() | PrecededBy(Regex(r"\W", flags=re.UNICODE), retreat=1)) + Combine(
            TOKEN
            + (~White() & ~TOKEN)
            + SkipTo(TOKEN, ignore=IGNORE, failOn=LineEnd())
            + TOKEN
            + ~Char(alphanums),
        ).setParseAction(self.action)


class Strikethrough(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return "~~" + self.markup.transformString(tokens[0]) + "~~"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("-")
        IGNORE = White() + TOKEN | Color(**self.init_kwargs).expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class Underline(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return self.markup.transformString(tokens[0])

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("+")
        IGNORE = White() + TOKEN | Color(**self.init_kwargs).expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class InlineQuote(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return "<q>" + self.markup.transformString(tokens[0]) + "</q>"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("??")
        IGNORE = White() + TOKEN | Color(**self.init_kwargs).expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class Superscript(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return "<sup>" + self.markup.transformString(tokens[0]) + "</sup>"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("^")
        IGNORE = White() + TOKEN | Color(**self.init_kwargs).expr | Attachment(**self.init_kwargs).expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class Subscript(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return "<sub>" + self.markup.transformString(tokens[0]) + "</sub>"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("~")
        IGNORE = White() + TOKEN | Color(**self.init_kwargs).expr | Mention(**self.init_kwargs).expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class Color(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        text = self.markup.transformString(tokens.text)

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
    @property
    def expr(self) -> ParserElement:
        return ("\n" | StringStart()) + Literal("bq. ").setParseAction(replaceWith("> "))


class BlockQuote(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        text = self.markup.transformString(tokens[0].strip())
        return "\n".join([f"> {line.lstrip()}" for line in text.splitlines()])

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
