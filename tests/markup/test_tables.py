from jira2markdown.parser import convert


class TestTable:
    def test_basic_conversion(self):
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

    def test_mixed_column_separator(self):
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

    def test_uneven_columns_count(self):
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

    def test_open_end_row(self):
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

    def test_smallest_table(self):
        assert convert("""
|header
""") == """

|header|
|-|
"""

    def test_multiline_text(self):
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

    def test_table_adjacent_text(self):
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

    def test_empty_rows(self):
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
