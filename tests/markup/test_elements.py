from pyparsing import ParserElement

from jira2markdown.elements import MarkupElements


class ElementA(ParserElement):
    pass


class ElementB(ParserElement):
    pass


class ElementC(ParserElement):
    pass


class TestMarkupElements:
    def test_insert_after(self):
        elements = MarkupElements([ElementA, ElementB])
        elements.insert_after(ElementA, ElementC)
        assert list(elements) == [ElementA, ElementC, ElementB]

    def test_replace(self):
        elements = MarkupElements([ElementA, ElementB])
        elements.replace(ElementB, ElementC)
        assert list(elements) == [ElementA, ElementC]
