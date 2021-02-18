from jira2markdown import convert


class TestLineBreakIndent:
    def test_ruler(self):
        assert convert(r"Text\\ ---- ") == "Text\n\n----"


class TestRecursiveContent:
    def test_bold_color_bold(self):
        assert convert("*text {color:red}*text inside*{color} outside*") == \
               '**text <font color="red">**text inside**</font> outside**'
        assert convert("*text {color:red}contains* token{color} outside*") == \
               r'**text <font color="red">contains\* token</font> outside**'

    def test_strikethrough_color_strikethrough(self):
        assert convert("-text {color:green}-text inside-{color} outside-") == \
               '~~text <font color="green">~~text inside~~</font> outside~~'
        assert convert("-text {color:green}contains- token{color} outside-") == \
               '~~text <font color="green">contains- token</font> outside~~'

    def test_underline_color_underline(self):
        assert convert("+text {color:blue}+text inside+{color} outside+") == \
               'text <font color="blue">text inside</font> outside'
        assert convert("+text {color:blue}contains+ token{color} outside+") == \
               'text <font color="blue">contains+ token</font> outside'


class TestTableContent:
    def test_basic_markup(self):
        assert convert("| Table *bold header* and {color:red}colored title{color} |") == \
            '\n\n|Table **bold header** and <font color="red">colored title</font>|\n|-|\n\n'

    def test_cell_image(self):
        assert convert("|!image.png|width=300!") == "\n\n|![image.png](image.png){width=300}|\n|-|\n\n"

    def test_cell_link(self):
        assert convert("|[link|http://example.com]|") == "\n\n|[link](http://example.com)|\n|-|\n\n"

    def test_cell_mailto(self):
        assert convert("|[mailto:user@example.com]|") == "\n\n|<user@example.com>|\n|-|\n\n"
        assert convert("|[alias|mailto:user@example.com]|") == "\n\n|<user@example.com>|\n|-|\n\n"

    def test_cell_mention(self):
        assert convert("|[user|~uuid]|", {"uuid": "elliot"}) == "\n\n|@elliot|\n|-|\n\n"
