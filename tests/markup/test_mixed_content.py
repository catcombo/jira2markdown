from jira2markdown import convert


def test_table_content():
    assert convert("""h2. Big -strikethrough- header
| Table * header *and 
*escaped chars* |
|!image.png|width=300! *and* more|
Next line

|[user|~uuid] mentions|Links [links|http://example.com] 
and part of a cell text
|!image.png!

Text after open line *{color:black}*nested bold*{color}*.
""", {"uuid": "john"}) == r"""## Big ~~strikethrough~~ header

|Table \* header \*and <br>**escaped chars**|
|-|
|![image.png](image.png){width=300} **and** more|

Next line


|@john mentions|Links [links](http://example.com) <br>and part of a cell text|
|-|-|
|![image.png](image.png)|

Text after open line **<font color="black">**nested bold**</font>**.
"""
