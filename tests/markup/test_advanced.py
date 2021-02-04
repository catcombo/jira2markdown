from jira2markdown import convert


def test_noformat():
    assert convert("""
{noformat}
preformatted piece of text
  so *no* further _formatting_ is done here
{noformat}
""") == """
```
preformatted piece of text
  so *no* further _formatting_ is done here
```
"""


def test_code():
    assert convert("""
{code}
def test_code():
    assert convert(...)
{code}
""") == """
```
def test_code():
    assert convert(...)
```
"""
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
    assert convert("""
{code:title=Bar.java|borderStyle=solid}
// Some comments here
public String getFoo()
{
    return foo;
}
{code}
""") == """
```
// Some comments here
public String getFoo()
{
    return foo;
}
```
"""
