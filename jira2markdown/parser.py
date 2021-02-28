from typing import Optional

from pyparsing import Forward, ParserElement

from jira2markdown.markup.advanced import Code, Noformat, Panel
from jira2markdown.markup.headings import Headings
from jira2markdown.markup.images import Image
from jira2markdown.markup.links import Attachment, Link, MailTo, Mention
from jira2markdown.markup.lists import OrderedList, UnorderedList
from jira2markdown.markup.tables import Table
from jira2markdown.markup.text_breaks import LineBreak, Mdash, Ndash, Ruler
from jira2markdown.markup.text_effects import BlockQuote, Bold, Color, EscSpecialChars, InlineQuote, Monospaced, \
    Quote, Strikethrough, Subscript, Superscript, Underline

ParserElement.setDefaultWhitespaceChars(" \t")


def convert(text: str, usernames: Optional[dict] = None) -> str:
    usernames = usernames or {}
    markup = Forward()

    markup <<= UnorderedList().expr | \
        OrderedList().expr | \
        Code().expr | \
        Noformat().expr | \
        Monospaced().expr | \
        Mention(usernames).expr | \
        MailTo().expr | \
        Attachment().expr | \
        Link(markup).expr | \
        Image().expr | \
        Table(markup).expr | \
        Headings().expr | \
        Quote().expr | \
        BlockQuote(markup).expr | \
        Panel(markup).expr | \
        Bold(markup).expr | \
        Ndash().expr | \
        Mdash().expr | \
        Ruler().expr | \
        Strikethrough(markup).expr | \
        Underline(markup).expr | \
        InlineQuote(markup).expr | \
        Superscript(markup).expr | \
        Subscript(markup).expr | \
        Color(markup).expr | \
        LineBreak().expr | \
        EscSpecialChars().expr

    return markup.transformString(text)
