import re

from pyparsing import CaselessLiteral, Char, Combine, Forward, LineEnd, Literal, Optional, ParseResults, \
    ParserElement, PrecededBy, QuotedString, Regex, SkipTo, StringStart, Suppress, White, Word, WordEnd, WordStart, \
    alphanums, alphas, hexnums, nums, replaceWith

from jira2markdown.markup.links import Attachment, Mention


class Bold:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        return "**" + self.markup.transformString(tokens[0]) + "**"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("*")
        IGNORE = White() + TOKEN | Color(self.markup).expr
        return (StringStart() | PrecededBy(Regex(r"\W", flags=re.UNICODE), retreat=1)) + Combine(
            TOKEN
            + (~White() & ~TOKEN)
            + SkipTo(TOKEN, ignore=IGNORE, failOn=LineEnd())
            + TOKEN
            + ~Char(alphanums),
        ).setParseAction(self.action)


class Strikethrough:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        return "~~" + self.markup.transformString(tokens[0]) + "~~"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("-")
        IGNORE = White() + TOKEN | Color(self.markup).expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class Underline:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        return self.markup.transformString(tokens[0])

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("+")
        IGNORE = White() + TOKEN | Color(self.markup).expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class InlineQuote:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        return "<q>" + self.markup.transformString(tokens[0]) + "</q>"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("??")
        IGNORE = White() + TOKEN | Color(self.markup).expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class Superscript:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        return "<sup>" + self.markup.transformString(tokens[0]) + "</sup>"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("^")
        IGNORE = White() + TOKEN | Color(self.markup).expr | Attachment().expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class Subscript:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        return "<sub>" + self.markup.transformString(tokens[0]) + "</sub>"

    @property
    def expr(self) -> ParserElement:
        TOKEN = Suppress("~")
        IGNORE = White() + TOKEN | Color(self.markup).expr | Mention({}).expr
        return WordStart() + Combine(
            TOKEN
            + ~White()
            + SkipTo(TOKEN, ignore=IGNORE, failOn="\n")
            + TOKEN,
        ).setParseAction(self.action) + WordEnd()


class Color:
    def __init__(self, markup: Forward):
        self.markup = markup

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


class Quote:
    @property
    def expr(self) -> ParserElement:
        return ("\n" | StringStart()) + Literal("bq. ").setParseAction(replaceWith("> "))


class BlockQuote:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        text = self.markup.transformString(tokens[0].strip())
        return "\n".join([f"> {line.lstrip()}" for line in text.splitlines()])

    @property
    def expr(self) -> ParserElement:
        return QuotedString("{quote}", multiline=True).setParseAction(self.action)


class Monospaced:
    def action(self, tokens: ParseResults) -> str:
        return f"`{tokens[0]}`"

    @property
    def expr(self) -> ParserElement:
        return QuotedString("{{", endQuoteChar="}}").setParseAction(self.action)


class EscSpecialChars:
    """
    Escapes '*' characters that are not a part of any expression grammar
    """

    @property
    def expr(self) -> ParserElement:
        return Literal("*").setParseAction(replaceWith(r"\*"))
