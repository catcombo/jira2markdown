from typing import Optional

from pyparsing import Forward, ParserElement

from jira2markdown.elements import MarkupElements

ParserElement.setDefaultWhitespaceChars(" \t")


def convert(text: str, usernames: Optional[dict] = None, elements: Optional[MarkupElements] = None) -> str:
    usernames = usernames or {}
    elements = elements or MarkupElements()

    inline_markup = Forward()
    markup = Forward()

    inline_markup << elements.expr(inline_markup, markup, usernames, filter(lambda e: e.is_inline_element, elements))
    markup << elements.expr(inline_markup, markup, usernames, elements)

    return markup.transformString(text)
