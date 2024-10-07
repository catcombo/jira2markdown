from pyparsing import LineEnd, ParseException, ParseImplReturnType


class UniversalLineEnd(LineEnd):
    def __init__(self):
        super().__init__()
        self.whiteChars.discard("\r\n")

    def parseImpl(self, instring, loc, do_actions=True) -> ParseImplReturnType:
        if loc < len(instring):
            if instring.startswith("\r\n", loc):
                return loc + 2, "\r\n"
            elif instring[loc] in ("\n", "\r"):
                return loc + 1, "\n"
            else:
                raise ParseException(instring, loc, self.errmsg, self)
        elif loc == len(instring):
            return loc + 1, []
        else:
            raise ParseException(instring, loc, self.errmsg, self)
