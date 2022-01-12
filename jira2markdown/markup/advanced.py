from pyparsing import Combine, FollowedBy, Group, Literal, OneOrMore, Optional, ParseResults, ParserElement, \
    SkipTo, Suppress, Word, alphanums, alphas

from jira2markdown.markup.base import AbstractMarkup


class Noformat(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        text = tokens.text.strip("\n")
        return f"```\n{text}\n```"

    @property
    def expr(self) -> ParserElement:
        return Combine(
            Literal("{noformat") + ... + Literal("}")
            + SkipTo("{noformat}").setResultsName("text")
            + "{noformat}",
        ).setParseAction(self.action)


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
                + Word(alphanums + "#+").setResultsName("lang")
                + FollowedBy(Literal("}") | Literal("|")),
            )
            + ... + "}"
            + SkipTo("{code}").setResultsName("text")
            + "{code}",
        ).setParseAction(self.action)


class Panel(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        for param, value in tokens.get("params", []):
            if param.lower() == "title":
                prefix = f"> **{value}**\n"
                break
        else:
            prefix = ""

        text = self.markup.transformString("\n".join([
            line.lstrip() for line in tokens.text.strip().splitlines()
        ]))
        return prefix + "\n".join([f"> {line}" for line in text.splitlines()])

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
