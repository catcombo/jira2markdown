from jira2markdown.parser import convert


def test_line_break():
    assert convert("abc\\\\def") == "abc\ndef"


def test_ndash():
    assert convert("--") == "–"
    assert convert("abc--def") == "abc--def"
    assert convert("abc -- def") == "abc – def"


def test_mdash():
    assert convert("---") == "—"
    assert convert("abc---def") == "abc---def"
    assert convert("abc --- def") == "abc — def"


def test_ruler():
    assert convert(" ---- ") == " \n----\n "
