from pyparsing import Keyword, LineEnd, ParserElement, StringStart, WordEnd, WordStart, replaceWith

from jira2markdown.markup.base import AbstractMarkup


class LineBreak(AbstractMarkup):
    @property
    def expr(self) -> ParserElement:
        return Keyword("\\\\", identChars="\\").setParseAction(replaceWith("\n"))


class Ndash(AbstractMarkup):
    @property
    def expr(self) -> ParserElement:
        return WordStart() \
            + Keyword("--", identChars="-").setParseAction(replaceWith("–")) \
            + WordEnd()


class Mdash(AbstractMarkup):
    @property
    def expr(self) -> ParserElement:
        return WordStart() \
            + Keyword("---", identChars="-").setParseAction(replaceWith("—")) \
            + WordEnd()


class Ruler(AbstractMarkup):
    is_inline_element = False

    @property
    def expr(self) -> ParserElement:
        # Text with dashed below it turns into a heading. To prevent this
        # add a line break before the dashes.
        return ("\n" | StringStart() | LineBreak(**self.init_kwargs).expr) \
            + Keyword("----", identChars="-").setParseAction(replaceWith("\n----")) \
            + LineEnd()
