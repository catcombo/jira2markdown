from pyparsing import CaselessLiteral, Combine, Forward, Optional, ParseResults, ParserElement, SkipTo, Suppress,\
    Word, alphanums


class MailTo:
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


class Link:
    def __init__(self, markup: Forward):
        self.markup = markup

    def action(self, tokens: ParseResults) -> str:
        name = getattr(tokens, "name", "")
        url = tokens.url

        if len(name) > 0:
            name = self.markup.transformString(name)
            return f"[{name}]({url})"
        else:
            return f"<{url}>"

    @property
    def expr(self) -> ParserElement:
        NAMED_LINK = SkipTo("|", failOn="]").setResultsName("name") + "|" + SkipTo("]").setResultsName("url")
        LINK = Combine("http" + SkipTo("]")).setResultsName("url")
        return Combine("[" + (LINK ^ NAMED_LINK) + "]").setParseAction(self.action)


class Attachment:
    def action(self, tokens: ParseResults) -> str:
        return f"[{tokens.filename}]({tokens.filename})"

    @property
    def expr(self) -> ParserElement:
        return Combine("[^" + SkipTo("]").setResultsName("filename") + "]").setParseAction(self.action)


class Mention:
    def __init__(self, usernames: dict):
        self.usernames = usernames

    def action(self, tokens: ParseResults) -> str:
        username = self.usernames.get(tokens.accountid)
        return f"@{tokens.accountid}" if username is None else f"@{username}"

    @property
    def expr(self) -> ParserElement:
        return Combine(
            "["
            + Optional(
                SkipTo("|", failOn="]") + Suppress("|"),
                default="",
            )
            + "~"
            + Optional(CaselessLiteral("accountid:"))
            + Word(alphanums + ":-").setResultsName("accountid")
            + "]",
        ).setParseAction(self.action)
