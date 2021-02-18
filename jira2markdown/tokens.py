import re

from pyparsing import ParseException, Token


class NotUnicodeAlphaNum(Token):
    """
    Matches if current position is at the beginning of a line or
    not preceded by unicode alpha numeric characters.
    """

    def __init__(self):
        super().__init__()

        self.name = self.__class__.__name__
        self.mayReturnEmpty = True
        self.mayIndexError = False

        self.pattern = re.compile(r"\w", re.UNICODE)
        self.errmsg = "Not at the start of a line or preceded by alpha numeric characters"

    def parseImpl(self, instring, loc, doActions=True):
        if (loc != 0) and self.pattern.match(instring[loc - 1]):
            raise ParseException(instring, loc, self.errmsg, self)
        return loc, []
