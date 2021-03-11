from string import punctuation

from pyparsing import CaselessLiteral, Char, Combine, FollowedBy, Optional, ParseResults, ParserElement, \
    PrecededBy, SkipTo, StringEnd, StringStart, Suppress, White, Word, alphanums

from jira2markdown.markup.base import AbstractMarkup


class MailTo(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        alias = self.markup.transformString(getattr(tokens, "alias", ""))
        email = tokens.email

        if (alias == email) or (len(alias.strip()) == 0):
            return f"<{email}>"
        else:
            return f"[{alias}](mailto:{tokens.email})"

    @property
    def expr(self) -> ParserElement:
        return Combine(
            "["
            + Optional(SkipTo("|", failOn="]").setResultsName("alias") + "|")
            + "mailto:"
            + Word(alphanums + "@.-_").setResultsName("email")
            + "]",
        ).setParseAction(self.action)


class Link(AbstractMarkup):
    URL_PREFIXES = ["http", "ftp"]

    def action(self, tokens: ParseResults) -> str:
        alias = self.markup.transformString(getattr(tokens, "alias", ""))
        url = tokens.url

        if url.lower().startswith("www."):
            url = f"https://{url}"

        if not any(map(url.lower().startswith, self.URL_PREFIXES)):
            url = self.markup.transformString(url)
            return fr"[{alias}\|{url}]" if alias else f"[{url}]"

        return f"[{alias}]({url})" if len(alias) > 0 else f"<{url}>"

    @property
    def expr(self) -> ParserElement:
        return Combine(
            "["
            + Optional(SkipTo("|", failOn="]").setResultsName("alias") + "|")
            + SkipTo("]").setResultsName("url")
            + "]",
        ).setParseAction(self.action)


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
