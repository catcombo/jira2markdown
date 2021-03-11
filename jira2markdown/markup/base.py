from pyparsing import Forward, ParserElement


class AbstractMarkup:
    is_inline_element: bool = True

    def __init__(self, inline_markup: Forward, markup: Forward, usernames: dict):
        self.inline_markup = inline_markup
        self.markup = markup
        self.usernames = usernames
        self.init_kwargs = dict(inline_markup=inline_markup, markup=markup, usernames=usernames)

    @property
    def expr(self) -> ParserElement:
        raise NotImplementedError
