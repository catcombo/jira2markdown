from pyparsing import Combine, Optional, ParseResults, ParserElement, \
    Word, alphanums, nums, printables

from jira2markdown.tokens import NotPrecededBy


class Image:
    def action(self, tokens: ParseResults) -> str:
        res = f"![{tokens.url}]({tokens.url})"
        if tokens.width:
            res += f"{{width={tokens.width}}}"
        if tokens.height:
            res += f"{{height={tokens.height}}}"
        return res

    @property
    def expr(self) -> ParserElement:
        return NotPrecededBy(alphanums) + Combine(
            "!"
            + Word(printables + " ", min=3, excludeChars="|!").setResultsName("url")
            + Optional(
                "|" + (
                    Optional("thumbnail")
                    ^ Optional(
                        "width=" + Word(nums).setResultsName("width")
                        + Optional(",height=" + Word(nums).setResultsName("height")),
                    )
                ),
            )
            + "!",
        ).setParseAction(self.action)
