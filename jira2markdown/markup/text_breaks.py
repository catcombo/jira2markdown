from pyparsing import Keyword, ParseResults, ParserElement, WordEnd, WordStart, replaceWith


class LineBreak:
    @property
    def expr(self) -> ParserElement:
        return Keyword("\\\\", identChars="\\").setParseAction(replaceWith("\n"))


class Ndash:
    @property
    def expr(self) -> ParserElement:
        return WordStart() + \
            Keyword("--", identChars="-").setParseAction(replaceWith("–")) + \
            WordEnd()


class Mdash:
    @property
    def expr(self) -> ParserElement:
        return WordStart() + \
            Keyword("---", identChars="-").setParseAction(replaceWith("—")) + \
            WordEnd()


class Ruler:
    def action(self, tokens: ParseResults) -> str:
        return "\n----\n"

    @property
    def expr(self) -> ParserElement:
        return WordStart() + \
            Keyword("----", identChars="-").setParseAction(self.action) + \
            WordEnd()
