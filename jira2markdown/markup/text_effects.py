from pyparsing import Char, Combine, Forward, LineEnd, LineStart, Literal, ParseResults, \
    ParserElement, QuotedString, SkipTo, Suppress, White, Word, WordEnd, WordStart, alphanums, replaceWith

from jira2markdown.tokens import NotPrecededBy


class Bold:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        return "**" + self.markup.transformString(tokens[0]) + "**"

    @property
    def expr(self) -> ParserElement:
        BOLD = Suppress("*")
        IGNORE = White() + BOLD | Color(self.markup).expr
        return NotPrecededBy(alphanums) + Combine(
            BOLD
            + (~White() & ~BOLD)
            + SkipTo(BOLD, ignore=IGNORE, failOn=LineEnd())
            + BOLD
            + ~Char(alphanums),
        ).setParseAction(self.action)


class Strikethrough:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        return "~~" + self.markup.transformString(tokens[0]) + "~~"

    @property
    def expr(self) -> ParserElement:
        STRIKE = Suppress("-")
        IGNORE = White() + STRIKE | Color(self.markup).expr
        return WordStart() + Combine(
            STRIKE
            + ~White()
            + SkipTo(STRIKE, ignore=IGNORE)
            + STRIKE,
        ).setParseAction(self.action) + WordEnd()


class Color:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        text = self.markup.transformString(tokens.text)

        if len(text.strip()) > 0:
            return f'<font color="{tokens.color}">{text}</font>'
        else:
            return ""

    @property
    def expr(self) -> ParserElement:
        expr = Combine("{color:" + Word(alphanums + "#").setResultsName("color") + "}") + \
            SkipTo("{color}").setResultsName("text") + \
            Suppress("{color}")
        return expr.setParseAction(self.action)


class Quote:
    @property
    def expr(self) -> ParserElement:
        return LineStart() + Literal("bq. ").setParseAction(replaceWith("> "))


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
