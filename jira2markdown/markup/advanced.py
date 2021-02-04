from pyparsing import Combine, FollowedBy, Optional, ParseResults, ParserElement, QuotedString, SkipTo, Word, alphanums


class Noformat:
    def action(self, tokens: ParseResults) -> str:
        text = tokens[0].strip("\n")
        return f"```\n{text}\n```"

    @property
    def expr(self) -> ParserElement:
        return QuotedString("{noformat}", multiline=True).setParseAction(self.action)


class Code:
    def action(self, tokens: ParseResults) -> str:
        lang = tokens.lang
        text = tokens.text.strip("\n")
        return f"```{lang}\n{text}\n```"

    @property
    def expr(self) -> ParserElement:
        return Combine(
            "{code"
            + Optional(
                ":"
                + Word(alphanums).setResultsName("lang")
                + FollowedBy("}"),
            )
            + ... + "}"
            + SkipTo("{code}").setResultsName("text")
            + "{code}",
        ).setParseAction(self.action)
