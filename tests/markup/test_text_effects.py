from jira2markdown.parser import convert


def test_bold():
    assert convert("*bold*") == "**bold**"
    assert convert("*bold* and more") == "**bold** and more"
    assert convert("*multiline\nbold*") == "\\*multiline\nbold\\*"
    assert convert("single *char") == r"single \*char"
    assert convert("*bold *") == r"\*bold \*"
    assert convert("start * spaced*") == r"start \* spaced\*"
    assert convert("pre*bold*") == r"pre\*bold\*"
    assert convert("*bold*post") == r"\*bold\*post"
    assert convert("*bold**") == r"**bold**\*"
    assert convert("**bold**") == r"\***bold**\*"
    assert convert("**") == r"\*\*"
    assert convert("***") == r"\*\*\*"


def test_strikethrough():
    assert convert("-strikethrough-") == "~~strikethrough~~"
    assert convert("-multiline\nstrikethrough-") == "~~multiline\nstrikethrough~~"
    assert convert("must-word- start") == "must-word- start"
    assert convert("must -word-end") == "must -word-end"
    assert convert("no - space after start-") == "no - space after start-"
    assert convert("-skip -spaced - char-") == "~~skip -spaced - char~~"


def test_underline():
    assert convert("+underline+") == "underline"
    assert convert("+multiline\nunderline+") == "+multiline\nunderline+"
    assert convert("must+word+ start") == "must+word+ start"
    assert convert("must +word+end") == "must +word+end"
    assert convert("no + space after start+") == "no + space after start+"
    assert convert("+skip +spaced + char+") == "skip +spaced + char"


def test_color():
    assert convert("{color:#0077ff}colored text{color}") == '<font color="#0077ff">colored text</font>'
    assert convert("""
{color:red}
    look ma, red text!
{color}
""") == """
<font color="red">
    look ma, red text!
</font>
"""
    assert convert("{color:#0077ff}{color}") == ""
    assert convert("{color:black}\n{color}") == "\n"
    assert convert("{color:#0077ff}  spaces around  {color}") == '<font color="#0077ff">  spaces around  </font>'
    assert convert("{color:rgba(255, 127, 63, 0.3)}text{color}") == '<font color="#ff7f3f">text</font>'


def test_quote():
    assert convert("bq. Some text") == "> Some text"


def test_block_quote():
    assert convert("""
{quote}
    here is quotable
        content to be quoted
{quote}
""") == """
> here is quotable
> content to be quoted
"""


def test_monospaced():
    assert convert("{{some text inside}}") == "`some text inside`"
