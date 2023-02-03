import pytest

from jira2markdown import convert


class TestLineBreakIndent:
    def test_ruler(self):
        assert convert(r"Text\\ ---- ") == "Text\n\n----"


class TestBlockQuoteContent:
    def test_list(self):
        assert (
            convert(
                """
{quote}
* Item
** Line
{quote}
"""
            )
            == """
> - Item
>   - Line
"""
        )


class TestRecursiveContent:
    def test_bold_color(self):
        assert (
            convert("*text {color:red}*text inside*{color} outside*")
            == '**text <font color="red">**text inside**</font> outside**'
        )
        assert (
            convert("*text {color:red}contains* token{color} outside*")
            == r'**text <font color="red">contains\* token</font> outside**'
        )

    def test_strikethrough_color(self):
        assert (
            convert("-text {color:green}-text inside-{color} outside-")
            == '~~text <font color="green">~~text inside~~</font> outside~~'
        )
        assert (
            convert("-text {color:green}contains- token{color} outside-")
            == '~~text <font color="green">contains- token</font> outside~~'
        )

    def test_underline_color(self):
        assert (
            convert("+text {color:blue}+text inside+{color} outside+")
            == '<u>text <font color="blue"><u>text inside</u></font> outside</u>'
        )
        assert (
            convert("+text {color:blue}contains+ token{color} outside+")
            == '<u>text <font color="blue">contains+ token</font> outside</u>'
        )

    def test_inlinequote_color(self):
        assert (
            convert("??text {color:blue}??text inside??{color} outside??")
            == '<q>text <font color="blue"><q>text inside</q></font> outside</q>'
        )
        assert (
            convert("??text {color:blue}contains?? token{color} outside??")
            == '<q>text <font color="blue">contains?? token</font> outside</q>'
        )

    def test_superscript_color(self):
        assert (
            convert("^text {color:blue}^text inside^{color} outside^")
            == '<sup>text <font color="blue"><sup>text inside</sup></font> outside</sup>'
        )
        assert (
            convert("^text {color:blue}contains^ token{color} outside^")
            == '<sup>text <font color="blue">contains^ token</font> outside</sup>'
        )

    def test_superscript_attachment(self):
        assert convert("^text [^attachment.ext] outside^") == "<sup>text [attachment.ext](attachment.ext) outside</sup>"

    def test_subscript_color(self):
        assert (
            convert("~text {color:blue}~text inside~{color} outside~")
            == '<sub>text <font color="blue"><sub>text inside</sub></font> outside</sub>'
        )
        assert (
            convert("~text {color:blue}contains~ token{color} outside~")
            == '<sub>text <font color="blue">contains~ token</font> outside</sub>'
        )

    def test_subscript_mention(self):
        assert convert("~text [~username] outside~") == "<sub>text @username outside</sub>"


@pytest.mark.parametrize(
    "token,test_input,expected",
    [
        ("headings", "h2. %s", "## %s"),
        ("bold", "*%s*", "**%s**"),
        ("strikethrough", "-%s-", "~~%s~~"),
        ("underline", "+%s+", "<u>%s</u>"),
        ("inlinequote", "??%s??", "<q>%s</q>"),
        ("superscript", "^%s^", "<sup>%s</sup>"),
        ("subscript", "~%s~", "<sub>%s</sub>"),
        ("color", "{color:red}%s{color}", '<font color="red">%s</font>'),
        ("quote", "bq. %s", "> %s"),
    ],
    ids=["headings", "bold", "strikethrough", "underline", "inlinequote", "superscript", "subscript", "color", "quote"],
)
class TestInlineElements:
    def test_headings(self, token, test_input, expected):
        assert convert(test_input % "h2. Heading") == expected % "h2. Heading"

    def test_limited_markup(self, token, test_input, expected):
        if token == "subscript":
            pytest.skip(f"Skip nested tests for {token} token")
        else:
            assert convert(test_input % "h2. ~Heading~") == expected % "h2. <sub>Heading</sub>"

    def test_quote(self, token, test_input, expected):
        assert convert(test_input % "bq. Quote") == expected % "bq. Quote"

    def test_table(self, token, test_input, expected):
        assert convert(test_input % "|Table") == expected % "|Table"

    def test_list(self, token, test_input, expected):
        if token == "bold":
            pytest.skip(f"Skip nested tests for {token} token")
        else:
            assert convert(test_input % "* Item") == expected % r"\* Item"

    def test_ruler(self, token, test_input, expected):
        if token == "strikethrough":
            pytest.skip(f"Skip nested tests for {token} token")
        else:
            assert convert(test_input % "----") == expected % "----"

    def test_bold(self, token, test_input, expected):
        if token == "bold":
            pytest.skip(f"Skip nested tests for {token} token")
        else:
            assert convert(test_input % "*Bold text*") == expected % "**Bold text**"

    def test_color(self, token, test_input, expected):
        if token == "color":
            pytest.skip(f"Skip nested tests for {token} token")
        else:
            assert convert(test_input % "{color:red}Red text{color}") == expected % '<font color="red">Red text</font>'

    def test_blockquote(self, token, test_input, expected):
        assert convert(test_input % "{quote}Quote text{quote}") == expected % "> Quote text"

    def test_monospaced(self, token, test_input, expected):
        assert convert(test_input % "{{monospaced}}") == expected % "`monospaced`"

    def test_image(self, token, test_input, expected):
        assert convert(test_input % "!attached-image.gif!") == expected % "![attached-image.gif](attached-image.gif)"

    def test_link(self, token, test_input, expected):
        assert convert(test_input % "[http://example.com]") == expected % "<http://example.com>"

    def test_mention(self, token, test_input, expected):
        assert convert(test_input % "[~username]") == expected % "@username"


@pytest.mark.parametrize(
    "token,test_input,expected",
    [
        ("blockquote", "{quote}%s{quote}", ["> %s", "> %s"]),
        ("panel", "{panel}%s{panel}", ["> %s", "> %s"]),
        ("table", "|%s\n|row", ["|%s|\n|-|\n|row|\n"]),
        ("unordered_list", "* %s", ["- %s", "  %s"]),
        ("ordered_list", "# %s", ["1. %s", "   %s"]),
    ],
    ids=["blockquote", "panel", "table", "unordered_list", "ordered_list"],
)
class TestBlockElements:
    def render_expected(self, expected, text):
        if len(expected) == 1:
            return expected[0] % text

        first_line, next_line = expected
        return "\n".join(
            [first_line % line if i == 0 else next_line % line for i, line in enumerate(text.splitlines())]
        )

    def test_headings(self, token, test_input, expected):
        assert convert(test_input % "h2. Heading") == self.render_expected(expected, "## Heading")

    def test_quote(self, token, test_input, expected):
        assert convert(test_input % "bq. Quote") == self.render_expected(expected, "> Quote")

    def test_table(self, token, test_input, expected):
        if token == "table":
            pytest.skip(f"Skip nested tests for {token} token")
        else:
            assert convert(test_input % "|Table") == self.render_expected(expected, "|Table|\n|-|\n")

    def test_list(self, token, test_input, expected):
        if token in ["unordered_list", "ordered_list"]:
            pytest.skip(f"Skip nested tests for {token} token")
        else:
            assert convert(test_input % "* Item") == self.render_expected(expected, "- Item")

    def test_bold(self, token, test_input, expected):
        assert convert(test_input % "*Bold text*") == self.render_expected(expected, "**Bold text**")

    def test_color(self, token, test_input, expected):
        assert convert(test_input % "{color:red}Red text{color}") == self.render_expected(
            expected, '<font color="red">Red text</font>'
        )

    def test_blockquote(self, token, test_input, expected):
        if token == "blockquote":
            pytest.skip(f"Skip nested tests for {token} token")
        else:
            assert convert(test_input % "{quote}Quote text{quote}") == self.render_expected(expected, "> Quote text")

    def test_monospaced(self, token, test_input, expected):
        assert convert(test_input % "{{monospaced}}") == self.render_expected(expected, "`monospaced`")

    def test_image(self, token, test_input, expected):
        assert convert(test_input % "!attached-image.gif!") == self.render_expected(
            expected, "![attached-image.gif](attached-image.gif)"
        )

    def test_link(self, token, test_input, expected):
        assert convert(test_input % "[http://example.com]") == self.render_expected(expected, "<http://example.com>")

    def test_mention(self, token, test_input, expected):
        assert convert(test_input % "[~username]") == self.render_expected(expected, "@username")


class TestStrikethroughContent:
    def test_color(self):
        assert convert("-{color:red}-text-{color}-") == '~~<font color="red">~~text~~</font>~~'

    def test_attachment(self):
        assert convert("-[^file-name.ext]-") == "~~[file-name.ext](file-name.ext)~~"

    def test_mention(self):
        assert convert("-[~user-name]-") == "~~@user-name~~"

    def test_link(self):
        assert convert("-[http://site-name.tld]-") == "~~<http://site-name.tld>~~"

    def test_image(self):
        assert convert("-!attached-image.gif!-") == "~~![attached-image.gif](attached-image.gif)~~"


class TestTableContent:
    def test_basic_markup(self):
        assert (
            convert("| Table *bold header* and {color:red}colored title{color} |")
            == '| Table **bold header** and <font color="red">colored title</font> |\n|-|\n'
        )

    def test_cell_image(self):
        assert convert("|!image.png|width=300!") == "|![image.png](image.png)|\n|-|\n"

    def test_cell_link(self):
        assert convert("|[link|http://example.com]|") == "|[link](http://example.com)|\n|-|\n"

    def test_cell_mailto(self):
        assert convert("|[mailto:user@example.com]|") == "|<user@example.com>|\n|-|\n"
        assert convert("|[-alias-|mailto:user@example.com]|") == "|[~~alias~~](mailto:user@example.com)|\n|-|\n"

    def test_cell_mention(self):
        assert convert("|[user|~uuid]|", {"uuid": "elliot"}) == "|@elliot|\n|-|\n"


class TestPanelContent:
    def test_text_formatting(self):
        assert (
            convert(
                """
{panel:title=My Title|borderStyle=dashed|borderColor=#ccc|titleBGColor=#F7D6C1|bgColor=#FFFFCE}
a block of text surrounded with a *panel*
line with !image.png|width=300!
{panel}
"""
            )
            == """
> **My Title**
> a block of text surrounded with a **panel**
> line with ![image.png](image.png)
"""
        )

    def test_list(self):
        assert (
            convert(
                """
{panel}
* Item
** Line
{panel}
"""
            )
            == """
> - Item
>   - Line
"""
        )


class TestListContent:
    def test_broken_list_markup(self):
        assert (
            convert(
                """
----- Hello, -World-! -----
"""
            )
            == """
----- Hello, ~~World~~! -----
"""
        )
        assert (
            convert(
                """
-- 
Hello
{quote}
World
{quote}
"""
            )
            == """
– 
Hello
> World
"""
        )
        assert (
            convert(
                """
--------- 

-- 
"""
            )
            == """
--------- 

– 
"""
        )

    def test_list_blockquote(self):
        assert (
            convert(
                """
* Item
** Second
*** {quote}


Some quote
{quote}
**** Four
"""
            )
            == """
- Item
  - Second
    - > Some quote
      - Four
"""
        )
        assert (
            convert(
                """
# Item
## Second
### {quote}


Some quote
{quote}
#### Four
"""
            )
            == """
1. Item
   1. Second
      1. > Some quote
         1. Four
"""
        )

    def test_list_panel_list(self):
        assert (
            convert(
                """
* Item
** Second
*** {panel}


Some quote
{panel}
**** Four
"""
            )
            == """
- Item
  - Second
    - > Some quote
      - Four
"""
        )
        assert (
            convert(
                """
# Item
## Second
### {panel}


Some quote
{panel}
#### Four
"""
            )
            == """
1. Item
   1. Second
      1. > Some quote
         1. Four
"""
        )

    def test_list_color_list(self):
        assert (
            convert(
                """
* Item
** Second
*** {color:red}


Some text
{color}
**** Four
"""
            )
            == """
- Item
  - Second
    - <font color="red">
      
      
      Some text
      </font>
      - Four
"""
        )
        assert (
            convert(
                """
# Item
## Second
### {color:red}


Some text
{color}
#### Four
"""
            )
            == """
1. Item
   1. Second
      1. <font color="red">
         
         
         Some text
         </font>
         1. Four
"""
        )


class TestLink:
    def test_alias_markup(self):
        assert (
            convert("[+box@example.com+|mailto:box@example.com]") == "[<u>box@example.com</u>](mailto:box@example.com)"
        )
        assert convert("[box+tag@example.com|mailto:box+tag@example.com]") == "<box+tag@example.com>"

    def test_text_markup(self):
        assert convert("[Text in -square- brackets]") == "[Text in ~~square~~ brackets]"
        assert convert("[Some *text*|More ^text^]") == r"[Some **text**\|More <sup>text</sup>]"
