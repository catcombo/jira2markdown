from string import punctuation

from pyparsing import (
    CaselessLiteral,
    Char,
    Combine,
    FollowedBy,
    Optional,
    ParserElement,
    ParseResults,
    PrecededBy,
    SkipTo,
    StringEnd,
    StringStart,
    Suppress,
    White,
    Word,
    alphanums,
)

from jira2markdown.markup.base import AbstractMarkup


class MailTo(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        alias = self.markup.transform_string(getattr(tokens, "alias", ""))
        email = tokens.email

        if (alias == email) or (len(alias.strip()) == 0):
            return f"<{email}>"
        else:
            return f"[{alias}](mailto:{tokens.email})"

    @property
    def expr(self) -> ParserElement:
        return Combine(
            "["
            + Optional(SkipTo("|", fail_on="]").set_results_name("alias") + "|")
            + "mailto:"
            + Word(alphanums + "@.-_+").set_results_name("email")
            + "]",
        ).set_parse_action(self.action)


class Link(AbstractMarkup):
    URL_PREFIXES = ["http", "ftp"]

    def action(self, tokens: ParseResults) -> str:
        alias = self.markup.transform_string(getattr(tokens, "alias", ""))
        url = tokens.url

        if url.lower().startswith("www."):
            url = f"https://{url}"

        if not any(map(url.lower().startswith, self.URL_PREFIXES)):
            url = self.markup.transform_string(url)
            return rf"[{alias}\|{url}]" if alias else f"[{url}]"

        return f"[{alias}]({url})" if len(alias) > 0 else f"<{url}>"

    @property
    def expr(self) -> ParserElement:
        return Combine(
            "["
            + Optional(SkipTo("|", fail_on="]").set_results_name("alias") + "|")
            + SkipTo("]").set_results_name("url")
            + "]",
        ).set_parse_action(self.action)


class Attachment(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        return f"[{tokens.filename}]({tokens.filename})"

    @property
    def expr(self) -> ParserElement:
        return Combine("[^" + SkipTo("]").set_results_name("filename") + "]").set_parse_action(self.action)


class Mention(AbstractMarkup):
    def action(self, tokens: ParseResults) -> str:
        username = self.usernames.get(tokens.accountid)
        return f"@{tokens.accountid}" if username is None else f"@{username}"

    @property
    def expr(self) -> ParserElement:
        MENTION = Combine(
            "["
            + Optional(
                SkipTo("|", fail_on="]") + Suppress("|"),
                default="",
            )
            + "~"
            + Optional(CaselessLiteral("accountid:"))
            + Word(alphanums + ":-").set_results_name("accountid")
            + "]",
        )
        return (
            (StringStart() | Optional(PrecededBy(White(), retreat=1), default=" "))
            + MENTION.set_parse_action(self.action)
            + (
                StringEnd()
                | Optional(FollowedBy(White() | Char(punctuation, exclude_chars="[") | MENTION), default=" ")
            )
        )
