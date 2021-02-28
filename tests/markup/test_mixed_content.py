from jira2markdown import convert


class TestLineBreakIndent:
    def test_ruler(self):
        assert convert(r"Text\\ ---- ") == "Text\n\n----"


class TestRecursiveContent:
    def test_bold_color(self):
        assert convert("*text {color:red}*text inside*{color} outside*") == \
               '**text <font color="red">**text inside**</font> outside**'
        assert convert("*text {color:red}contains* token{color} outside*") == \
               r'**text <font color="red">contains\* token</font> outside**'

    def test_strikethrough_color(self):
        assert convert("-text {color:green}-text inside-{color} outside-") == \
               '~~text <font color="green">~~text inside~~</font> outside~~'
        assert convert("-text {color:green}contains- token{color} outside-") == \
               '~~text <font color="green">contains- token</font> outside~~'

    def test_underline_color(self):
        assert convert("+text {color:blue}+text inside+{color} outside+") == \
               'text <font color="blue">text inside</font> outside'
        assert convert("+text {color:blue}contains+ token{color} outside+") == \
               'text <font color="blue">contains+ token</font> outside'

    def test_inlinequote_color(self):
        assert convert("??text {color:blue}??text inside??{color} outside??") == \
               '<q>text <font color="blue"><q>text inside</q></font> outside</q>'
        assert convert("??text {color:blue}contains?? token{color} outside??") == \
               '<q>text <font color="blue">contains?? token</font> outside</q>'

    def test_superscript_color(self):
        assert convert("^text {color:blue}^text inside^{color} outside^") == \
               '<sup>text <font color="blue"><sup>text inside</sup></font> outside</sup>'
        assert convert("^text {color:blue}contains^ token{color} outside^") == \
               '<sup>text <font color="blue">contains^ token</font> outside</sup>'

    def test_superscript_attachment(self):
        assert convert("^text [^attachment.ext] outside^") == \
               "<sup>text [attachment.ext](attachment.ext) outside</sup>"

    def test_subscript_color(self):
        assert convert("~text {color:blue}~text inside~{color} outside~") == \
               '<sub>text <font color="blue"><sub>text inside</sub></font> outside</sub>'
        assert convert("~text {color:blue}contains~ token{color} outside~") == \
               '<sub>text <font color="blue">contains~ token</font> outside</sub>'

    def test_subscript_mention(self):
        assert convert("~text [~username] outside~") == "<sub>text @username outside</sub>"


class TestTableContent:
    def test_basic_markup(self):
        assert convert("| Table *bold header* and {color:red}colored title{color} |") == \
            '|Table **bold header** and <font color="red">colored title</font>|\n|-|\n'

    def test_cell_image(self):
        assert convert("|!image.png|width=300!") == "|![image.png](image.png)|\n|-|\n"

    def test_cell_link(self):
        assert convert("|[link|http://example.com]|") == "|[link](http://example.com)|\n|-|\n"

    def test_cell_mailto(self):
        assert convert("|[mailto:user@example.com]|") == "|<user@example.com>|\n|-|\n"
        assert convert("|[alias|mailto:user@example.com]|") == "|<user@example.com>|\n|-|\n"

    def test_cell_mention(self):
        assert convert("|[user|~uuid]|", {"uuid": "elliot"}) == "|@elliot|\n|-|\n"


class TestPanelContent:
    def test_text_formatting(self):
        assert convert("""
{panel:title=My Title|borderStyle=dashed|borderColor=#ccc|titleBGColor=#F7D6C1|bgColor=#FFFFCE}
a block of text surrounded with a *panel*
line with !image.png|width=300!
{panel}
""") == """
> **My Title**
> a block of text surrounded with a **panel**
> line with ![image.png](image.png)
"""
