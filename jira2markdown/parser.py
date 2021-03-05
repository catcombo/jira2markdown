from typing import Optional

from pyparsing import Forward, ParserElement

from jira2markdown.elements import MarkupElements

ParserElement.setDefaultWhitespaceChars(" \t")


def convert(text: str, usernames: Optional[dict] = None, elements: Optional[MarkupElements] = None) -> str:
    usernames = usernames or {}
    elements = elements or MarkupElements()

    markup = Forward()
    markup << elements.to_expression(markup, usernames)

    return markup.transformString(text)
