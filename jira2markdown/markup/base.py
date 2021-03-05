from pyparsing import Forward, ParserElement


class AbstractMarkup:
    def __init__(self, markup: Forward, usernames: dict):
        self.markup = markup
        self.usernames = usernames
        self.init_kwargs = dict(markup=markup, usernames=usernames)

    @property
    def expr(self) -> ParserElement:
        raise NotImplementedError
