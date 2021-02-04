from jira2markdown.parser import convert


def test_table():
    assert convert("""
||header 1||header 2||header 3||
|cell 1-1|cell 1-2|cell 1-3|
|cell 2-1|cell 2-2|cell 2-3|
""") == """

|header 1|header 2|header 3|
|-|-|-|
|cell 1-1|cell 1-2|cell 1-3|
|cell 2-1|cell 2-2|cell 2-3|
"""


def test_mixed_column_separator():
    assert convert("""
|header 1||header 2|header 3|
|cell 1-1|cell 1-2||cell 1-3|
||cell 2-1|cell 2-2|cell 2-3|
""") == """

|header 1|header 2|header 3|
|-|-|-|
|cell 1-1|cell 1-2|cell 1-3|
|cell 2-1|cell 2-2|cell 2-3|
"""


def test_uneven_columns_count():
    assert convert("""
|header 1|header 2|
|cell 1-1|cell 1-2|cell 1-3|
|cell 2-1|
""") == """

|header 1|header 2||
|-|-|-|
|cell 1-1|cell 1-2|cell 1-3|
|cell 2-1|
"""


def test_open_end_row():
    assert convert("""
||header 1||header 2||header 3
|cell 1-1|cell 1-2
|cell 2-1
""") == """

|header 1|header 2|header 3|
|-|-|-|
|cell 1-1|cell 1-2|
|cell 2-1|
"""


def test_smallest_table():
    assert convert("""
|header
""") == """

|header|
|-|
"""


def test_multiline_text():
    assert convert("""
|multi
line 
header|
|multi
line 
row|sibling row|
|open 
end 
row
""") == """

|multi<br>line <br>header||
|-|-|
|multi<br>line <br>row|sibling row|
|open <br>end <br>row|
"""


def test_sibling_text():
    assert convert("""
text before table
||header 1||header 2||
|cell 1-1|cell 1-2|
text after table
""") == """
text before table

|header 1|header 2|
|-|-|
|cell 1-1|cell 1-2|

text after table
"""


def test_empty_rows():
    assert convert("""
|
||
|text|
|
|end|
""") == """

|text|
|-|
|end|
"""
