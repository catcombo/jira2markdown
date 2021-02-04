from pyparsing import Combine, LineStart, OneOrMore, Optional, ParseResults, ParserElement, Suppress, White


class UnorderedList:
    def action(self, tokens: ParseResults) -> str:
        count = len(tokens.nested) * 3 + len(tokens.chars) * 2 - 2
        return " " * count + "- "

    @property
    def expr(self) -> ParserElement:
        return LineStart() + Combine(
            Optional("#", default="").setResultsName("nested")
            + (OneOrMore("*") | OneOrMore("-")).setResultsName("chars")
            + Suppress(" "),
        ).setParseAction(self.action) + ~White()


class OrderedList:
    def action(self, tokens: ParseResults) -> str:
        count = len(tokens.nested) * 2 + len(tokens.chars) * 3 - 3
        return " " * count + "1. "

    @property
    def expr(self) -> ParserElement:
        return LineStart() + Combine(
            Optional("*", default="").setResultsName("nested")
            + OneOrMore("#").setResultsName("chars")
            + Suppress(" "),
        ).setParseAction(self.action) + ~White()
