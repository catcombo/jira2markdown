from jira2markdown.parser import convert


class TestLineBreak:
    def test_word_break(self):
        assert convert("abc\\\\def") == "abc\ndef"


class TestNdash:
    def test_basic_conversion(self):
        assert convert("--") == "–"
        assert convert("abc -- def") == "abc – def"

    def test_word_connections(self):
        assert convert("abc--def") == "abc--def"
        assert convert("abc --def") == "abc --def"
        assert convert("abc-- def") == "abc-- def"


class TestMdash:
    def test_basic_conversion(self):
        assert convert("---") == "—"
        assert convert("abc --- def") == "abc — def"

    def test_word_connections(self):
        assert convert("abc---def") == "abc---def"
        assert convert("abc ---def") == "abc ---def"
        assert convert("abc--- def") == "abc--- def"


class TestRuler:
    def test_basic_conversion(self):
        assert convert("----") == "\n----"

    def test_indent(self):
        assert convert(" ---- ") == "\n----"

    def test_word_connections(self):
        assert convert("abc----def") == "abc----def"
        assert convert("abc ----def") == "abc ----def"
        assert convert("abc---- def") == "abc---- def"
        assert convert("abc ---- def") == "abc ---- def"
        assert convert("abc ---- ") == "abc ---- "
        assert convert(" ---- def") == " ---- def"
