from pyparsing import MatchFirst


class StepBack(MatchFirst):
    def parseImpl(self, instring, loc, doActions=True):
        loc, tokens = super().parseImpl(instring, loc, doActions)
        return loc - 1, tokens
