from pyparsing import Keyword, LineEnd, ParserElement, StringStart, WordEnd, WordStart, replaceWith


class LineBreak:
    @property
    def expr(self) -> ParserElement:
        return Keyword("\\\\", identChars="\\").setParseAction(replaceWith("\n"))


class Ndash:
    @property
    def expr(self) -> ParserElement:
        return WordStart() \
            + Keyword("--", identChars="-").setParseAction(replaceWith("–")) \
            + WordEnd()


class Mdash:
    @property
    def expr(self) -> ParserElement:
        return WordStart() \
            + Keyword("---", identChars="-").setParseAction(replaceWith("—")) \
            + WordEnd()


class Ruler:
    @property
    def expr(self) -> ParserElement:
        return ("\n" | StringStart() | LineBreak().expr) \
            + Keyword("----", identChars="-").setParseAction(replaceWith("\n----")) \
            + LineEnd()
