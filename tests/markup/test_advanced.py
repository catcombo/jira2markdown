from jira2markdown import convert


class TestNoformat:
    def test_basic_conversion(self):
        assert convert("{noformat}preformatted piece of text{noformat}") == "```\npreformatted piece of text\n```"

    def test_multiline(self):
        assert convert("{noformat}\npreformatted piece\nof text\n{noformat}") == \
               "```\npreformatted piece\nof text\n```"
        assert convert("{noformat}\n\n\n  preformatted piece\n   of text\n\n{noformat}") == \
               "```\n  preformatted piece\n   of text\n```"
        assert convert("{noformat}  \n  \n  preformatted piece\n   of text\n{noformat}") == \
               "```\n  \n  \n  preformatted piece\n   of text\n```"


class TestCode:
    def test_default_language(self):
        assert convert("""
{code}
def test_code():
    assert convert(...)
{code}
""") == """
```Java
def test_code():
    assert convert(...)
```
"""

    def test_explicit_language(self):
        assert convert("""
{code:xml}
    <test>
        <another tag="attribute"/>
    </test>
{code}
""") == """
```xml
    <test>
        <another tag="attribute"/>
    </test>
```
"""

    def test_decorations(self):
        assert convert("""
{code:title=Bar.java|borderStyle=solid}
// Some comments here
public String getFoo()
{
    return foo;
}
{code}
""") == """
```Java
// Some comments here
public String getFoo()
{
    return foo;
}
```
"""
