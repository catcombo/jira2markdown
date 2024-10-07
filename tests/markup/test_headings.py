from jira2markdown.parser import convert


class TestHeadings:
    def test_basic_conversion(self):
        assert convert("h1. Title text") == "# Title text"

    def test_header_levels(self):
        assert convert("h6. Title") == "###### Title"
        assert convert("h7. Title") == "h7. Title"

    def test_match_start_conditions(self):
        assert convert("  h2. Title") == "  ## Title"
        assert convert(" A  h2. Title") == " A  h2. Title"

    def test_windows_line_breaks(self):
        assert (
            convert("Line before heading\r\nh1. Title text\r\nLine after heading")
            == "Line before heading\r\n# Title text\r\nLine after heading"
        )
