from jira2markdown import convert


class TestNoformat:
    def test_basic_conversion(self):
        assert convert("{noformat}preformatted piece of text{noformat}") == "```\npreformatted piece of text\n```"

    def test_multiline(self):
        assert convert("{noformat}\npreformatted piece\nof text\n{noformat}") == "```\npreformatted piece\nof text\n```"
        assert (
            convert("{noformat}\n\n\n  preformatted piece\n   of text\n\n{noformat}")
            == "```\n  preformatted piece\n   of text\n```"
        )
        assert (
            convert("{noformat}  \n  \n  preformatted piece\n   of text\n{noformat}")
            == "```\n  \n  \n  preformatted piece\n   of text\n```"
        )

    def test_multiple_parameters(self):
        assert (
            convert(
                """
{noformat:borderStyle=dashed|borderColor=#ccc|title=My Title|titleBGColor=#F7D6C1|bgColor=#FFFFCE}
a block of code
surrounded with a noformat
{noformat}
"""
            )
            == """
```
a block of code
surrounded with a noformat
```
"""
        )


class TestCode:
    def test_default_language(self):
        assert (
            convert(
                """
{code}
def test_code():
    assert convert(...)
{code}
"""
            )
            == """
```Java
def test_code():
    assert convert(...)
```
"""
        )

    def test_explicit_language(self):
        assert (
            convert(
                """
{code:xml}
    <test>
        <another tag="attribute"/>
    </test>
{code}
"""
            )
            == """
```xml
    <test>
        <another tag="attribute"/>
    </test>
```
"""
        )

    def test_decorations(self):
        assert (
            convert(
                """
{code:title=Bar.java|borderStyle=solid}
// Some comments here
public String getFoo()
{
    return foo;
}
{code}
"""
            )
            == """
```Java
// Some comments here
public String getFoo()
{
    return foo;
}
```
"""
        )

    def test_multiple_parameters(self):
        assert (
            convert(
                """
{code:C++|title=test.cpp}
static int x = 10;

struct Foo {
    int x;
};
{code}
"""
            )
            == """
```C++
static int x = 10;

struct Foo {
    int x;
};
```
"""
        )


class TestPanel:
    def test_basic_conversion(self):
        assert (
            convert(
                """
{panel}
  Some text
       more line
{panel}
"""
            )
            == """
> Some text
> more line
"""
        )

    def test_title(self):
        assert (
            convert(
                """
{panel:title=My Title}
Some text with a title
{panel}
"""
            )
            == """
> **My Title**
> Some text with a title
"""
        )

    def test_multiple_parameters(self):
        assert (
            convert(
                """
{panel:borderStyle=dashed|borderColor=#ccc|title=My Title|titleBGColor=#F7D6C1|bgColor=#FFFFCE}
a block of text
surrounded with a panel
{panel}
"""
            )
            == """
> **My Title**
> a block of text
> surrounded with a panel
"""
        )
