from jira2markdown.parser import convert


def test_heading():
    assert convert("h1. Title text") == "# Title text"


def test_header_level():
    assert convert("h6. Title") == "###### Title"
    assert convert("h7. Title") == "h7. Title"
