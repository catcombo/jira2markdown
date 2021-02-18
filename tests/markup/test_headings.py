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
