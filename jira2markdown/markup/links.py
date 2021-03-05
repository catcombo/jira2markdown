from string import punctuation

from pyparsing import CaselessLiteral, Char, Combine, FollowedBy, Optional, ParseResults, ParserElement, \
    PrecededBy, SkipTo, StringEnd, StringStart, Suppress, White, Word, alphanums

from jira2markdown.markup.base import AbstractMarkup


class MailTo(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return f"<{tokens.email}>"

    @property
    def expr(self) -> ParserElement:
        return Combine(
            "["
            + Optional(
                SkipTo("|", failOn="]") + Suppress("|"),
            )
            + "mailto:"
            + Word(alphanums + "@.-").setResultsName("email")
            + "]",
        ).setParseAction(self.action)


class Link(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        alias = getattr(tokens, "alias", "")
        url = tokens.url

        if len(alias) > 0:
            alias = self.markup.transformString(alias)
            return f"[{alias}]({url})"
        else:
            return f"<{url}>"

    @property
    def expr(self) -> ParserElement:
        ALIAS_LINK = SkipTo("|", failOn="]").setResultsName("alias") + "|" + SkipTo("]").setResultsName("url")
        LINK = Combine("http" + SkipTo("]")).setResultsName("url")
        return Combine("[" + (LINK ^ ALIAS_LINK) + "]").setParseAction(self.action)


class Attachment(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return f"[{tokens.filename}]({tokens.filename})"

    @property
    def expr(self) -> ParserElement:
        return Combine("[^" + SkipTo("]").setResultsName("filename") + "]").setParseAction(self.action)


class Mention(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        username = self.usernames.get(tokens.accountid)
        return f"@{tokens.accountid}" if username is None else f"@{username}"

    @property
    def expr(self) -> ParserElement:
        MENTION = Combine(
            "["
            + Optional(
                SkipTo("|", failOn="]") + Suppress("|"),
                default="",
            )
            + "~"
            + Optional(CaselessLiteral("accountid:"))
            + Word(alphanums + ":-").setResultsName("accountid")
            + "]",
        )
        return (StringStart() | Optional(PrecededBy(White(), retreat=1), default=" ")) \
            + MENTION.setParseAction(self.action) \
            + (StringEnd()
               | Optional(FollowedBy(White() | Char(punctuation, excludeChars="[") | MENTION), default=" "))
