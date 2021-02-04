from pyparsing import ParseException, Token


class NotPrecededBy(Token):
    def __init__(self, chars: list):
        super().__init__()

        self.name = self.__class__.__name__
        self.mayReturnEmpty = True
        self.mayIndexError = False

        self.chars = chars
        self.errmsg = "Not at the start of a line or preceded by blacklisted characters"

    def parseImpl(self, instring, loc, doActions=True):
        if (loc != 0) and (instring[loc - 1] in self.chars):
            raise ParseException(instring, loc, self.errmsg, self)
        return loc, []
