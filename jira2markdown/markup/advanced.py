from pyparsing import Combine, FollowedBy, Group, Literal, OneOrMore, Optional, ParseResults, ParserElement, \
    QuotedString, SkipTo, Suppress, Word, alphanums, alphas

from jira2markdown.markup.base import AbstractMarkup


class Noformat(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        text = tokens[0].strip("\n")
        return f"```\n{text}\n```"

    @property
    def expr(self) -> ParserElement:
        return QuotedString("{noformat}", multiline=True).setParseAction(self.action)


class Code(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        lang = tokens.lang or "Java"
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


class Panel(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        text = self.markup.transformString(tokens.text.strip())

        for param, value in tokens.get("params", []):
            if param.lower() == "title":
                text = f"**{value}**\n{text}"

        return "\n".join([f"> {line.lstrip()}" for line in text.splitlines()])

    @property
    def expr(self) -> ParserElement:
        PARAM = Word(alphas) \
            + Suppress("=") \
            + SkipTo(Literal("|") | Literal("}")) \
            + Optional("|").suppress()

        return Combine(
            "{panel"
            + Optional(
                ":" + OneOrMore(Group(PARAM), stopOn="}").setResultsName("params"),
            )
            + "}"
            + SkipTo("{panel}").setResultsName("text")
            + "{panel}",
        ).setParseAction(self.action)
