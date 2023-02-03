from jira2markdown.parser import convert


class TestBold:
    def test_basic_conversion(self):
        assert convert("inside *some long* text") == "inside **some long** text"

    def test_line_endings(self):
        assert convert("*start string end*") == "**start string end**"
        assert convert("\n*start line end*\n") == "\n**start line end**\n"

    def test_match_start_conditions(self):
        assert convert("start * spacing*") == r"start \* spacing\*"
        assert convert("pre*bold*") == r"pre\*bold\*"
        assert convert("Я*bold*") == r"Я\*bold\*"
        assert convert("!*bold*") == "!**bold**"

    def test_match_end_conditions(self):
        assert convert("*bold *") == r"\*bold \*"
        assert convert("*word*connector") == r"\*word\*connector"
        assert convert("*skip *spacing * chars*") == r"**skip \*spacing \* chars**"

    def test_multiline(self):
        assert convert("*multiline\nbold*") == "\\*multiline\nbold\\*"

    def test_single_token(self):
        assert convert("single *char") == r"single \*char"

    def test_adjacent_tokens(self):
        assert convert("*some**text*") == "**some** **text**"
        assert convert("*some*   *text*") == "**some**   **text**"
        assert convert("**text**") == r"\***text**\*"
        assert convert("**some****text**") == r"\***some**\*\***text**\*"

    def test_empty_text(self):
        assert convert("**") == r"\*\*"
        assert convert("***") == r"\*\*\*"


class TestStrikethrough:
    def test_basic_conversion(self):
        assert convert("inside -some long- text") == "inside ~~some long~~ text"

    def test_line_endings(self):
        assert convert("-start string end-") == "~~start string end~~"
        assert convert("\n-start line end-\n") == "\n~~start line end~~\n"

    def test_match_start_conditions(self):
        assert convert("no - space after start-") == "no - space after start-"
        assert convert("word-connector- markup") == "word-connector- markup"

    def test_match_end_conditions(self):
        assert convert("-text -") == "-text -"
        assert convert("-word-connector") == "-word-connector"
        assert convert("-skip -spacing - chars-") == "~~skip -spacing - chars~~"

    def test_multiline(self):
        assert convert("-multiline\nstrikethrough-") == "-multiline\nstrikethrough-"

    def test_adjacent_tokens(self):
        assert convert("-some--text-") == "~~some~~ ~~text~~"
        assert convert("-some-   -text-") == "~~some~~   ~~text~~"
        assert convert("--text--") == "-~~text~~-"
        assert convert("--some----text--") == "-~~some~~--~~text~~-"


class TestUnderline:
    def test_basic_conversion(self):
        assert convert("inside +some long+ text") == "inside <u>some long</u> text"

    def test_line_endings(self):
        assert convert("+start string end+") == "<u>start string end</u>"
        assert convert("\n+start line end+\n") == "\n<u>start line end</u>\n"

    def test_match_start_conditions(self):
        assert convert("no + space after start+") == "no + space after start+"
        assert convert("word+connector+ markup") == "word+connector+ markup"

    def test_match_end_conditions(self):
        assert convert("+text +") == "+text +"
        assert convert("+word+connector") == "+word+connector"
        assert convert("+skip +spacing + char+") == "<u>skip +spacing + char</u>"

    def test_multiline(self):
        assert convert("+multiline\nunderline+") == "+multiline\nunderline+"


class TestInlineQuote:
    def test_basic_conversion(self):
        assert convert("inside ??some long?? text") == "inside <q>some long</q> text"

    def test_line_endings(self):
        assert convert("??start string end??") == "<q>start string end</q>"
        assert convert("\n??start line end??\n") == "\n<q>start line end</q>\n"

    def test_match_start_conditions(self):
        assert convert("no ?? space after start??") == "no ?? space after start??"
        assert convert("word??connector?? markup") == "word??connector?? markup"

    def test_match_end_conditions(self):
        assert convert("??text ??") == "??text ??"
        assert convert("??word??connector") == "??word??connector"
        assert convert("??skip ??spacing ?? char??") == "<q>skip ??spacing ?? char</q>"

    def test_multiline(self):
        assert convert("??multiline\nunderline??") == "??multiline\nunderline??"

    def test_adjacent_tokens(self):
        assert convert("??some????text??") == "<q>some</q> <q>text</q>"
        assert convert("??some??   ??text??") == "<q>some</q>   <q>text</q>"
        assert convert("????text????") == "??<q>text</q>??"
        assert convert("????some????????text????") == "??<q>some</q>????<q>text</q>??"


class TestSuperscript:
    def test_basic_conversion(self):
        assert convert("inside ^some long^ text") == "inside <sup>some long</sup> text"

    def test_line_endings(self):
        assert convert("^start string end^") == "<sup>start string end</sup>"
        assert convert("\n^start line end^\n") == "\n<sup>start line end</sup>\n"

    def test_match_start_conditions(self):
        assert convert("no ^ space after start^") == "no ^ space after start^"
        assert convert("word^connector^ markup") == "word^connector^ markup"

    def test_match_end_conditions(self):
        assert convert("^text ^") == "^text ^"
        assert convert("^word^connector") == "^word^connector"
        assert convert("^skip ^spacing ^ char^") == "<sup>skip ^spacing ^ char</sup>"

    def test_multiline(self):
        assert convert("^multiline\nunderline^") == "^multiline\nunderline^"

    def test_adjacent_tokens(self):
        assert convert("^some^^text^") == "<sup>some</sup> <sup>text</sup>"
        assert convert("^some^   ^text^") == "<sup>some</sup>   <sup>text</sup>"
        assert convert("^^text^^") == "^<sup>text</sup>^"
        assert convert("^^some^^^^text^^") == "^<sup>some</sup>^^<sup>text</sup>^"


class TestSubscript:
    def test_basic_conversion(self):
        assert convert("inside ~some long~ text") == "inside <sub>some long</sub> text"

    def test_line_endings(self):
        assert convert("~start string end~") == "<sub>start string end</sub>"
        assert convert("\n~start line end~\n") == "\n<sub>start line end</sub>\n"

    def test_match_start_conditions(self):
        assert convert("no ~ space after start~") == "no ~ space after start~"
        assert convert("word~connector~ markup") == "word~connector~ markup"

    def test_match_end_conditions(self):
        assert convert("~text ~") == "~text ~"
        assert convert("~word~connector") == "~word~connector"
        assert convert("~skip ~spacing ~ char~") == "<sub>skip ~spacing ~ char</sub>"

    def test_multiline(self):
        assert convert("~multiline\nunderline~") == "~multiline\nunderline~"

    def test_adjacent_tokens(self):
        assert convert("~some~~text~") == "<sub>some</sub> <sub>text</sub>"
        assert convert("~some~   ~text~") == "<sub>some</sub>   <sub>text</sub>"
        assert convert("~~text~~") == "~<sub>text</sub>~"
        assert convert("~~some~~~~text~~") == "~<sub>some</sub>~~<sub>text</sub>~"


class TestColor:
    def test_color_value(self):
        assert (
            convert("start {color:#0077ff}hex color{color} text") == 'start <font color="#0077ff">hex color</font> text'
        )
        assert convert("start {color:red}named color{color} text") == 'start <font color="red">named color</font> text'
        assert (
            convert("start {color:rgba(255, 127, 63, 0.3)}rgba color{color} text")
            == 'start <font color="#ff7f3f">rgba color</font> text'
        )

    def test_line_endings(self):
        assert convert("{color:#0077ff}colored{color}") == '<font color="#0077ff">colored</font>'
        assert convert("\n{color:#0077ff}colored{color}\n") == '\n<font color="#0077ff">colored</font>\n'

    def test_empty_text(self):
        assert convert("{color:#0077ff} {color}") == " "
        assert convert("{color:black}\n{color}") == "\n"

    def test_multiline(self):
        assert (
            convert(
                """
        {color:red}
            look ma, red text!
        {color}
        """
            )
            == """
        <font color="red">
            look ma, red text!
        </font>
        """
        )


class TestQuote:
    def test_basic_conversion(self):
        assert convert("bq. Some quote") == "> Some quote"

    def test_match_start_conditions(self):
        assert convert("  bq. Some quote") == "  > Some quote"
        assert convert("text  bq. Some quote") == "text  bq. Some quote"


class TestBlockQuote:
    def test_basic_conversion(self):
        assert (
            convert(
                """
{quote}
    here is quotable
        content to be quoted
{quote}
"""
            )
            == """
> here is quotable
> content to be quoted
"""
        )


class TestMonospaced:
    def test_basic_conversion(self):
        assert convert("{{some text inside}}") == "`some text inside`"
