# ruff: noqa: W291
from jira2markdown import convert


class TestUnorderedList:
    def test_bullets(self):
        assert (
            convert(
                """
* some
* bullet
** indented
** bullets
* points
        """,
            )
            == """
- some
- bullet
  - indented
  - bullets
- points
        """
        )
        assert (
            convert(
                """
- some
- bullet
-- indented
-- bullets
- points
        """,
            )
            == """
- some
- bullet
  - indented
  - bullets
- points
        """
        )

    def test_mixed_bullets(self):
        assert (
            convert(
                """
#* nested
#** bullet
#** list
        """,
            )
            == """
   - nested
     - bullet
     - list
        """
        )

    def test_match_start_conditions(self):
        assert convert("* Item") == "- Item"
        assert convert("\n* Item") == "\n- Item"
        assert convert("  * Item") == r"- Item"

    def test_multiline(self):
        assert (
            convert(
                """
* Item
Line
Next

Break
""",
            )
            == """
- Item
  Line
  Next

Break
"""
        )

    def test_start_indent(self):
        assert (
            convert(
                """
* First
** Second

** One
*** Two

* Last
** One
""",
            )
            == r"""
- First
  - Second

\*\* One
\*\*\* Two

- Last
  - One
"""
        )
        assert (
            convert(
                """
-- One
--- Two
""",
            )
            == """
– One
— Two
"""
        )

    def test_indent_step(self):
        assert (
            convert(
                """
* one
** two
**** four
""",
            )
            == r"""
- one
  - two
\*\*\*\* four
"""
        )

    def test_empty_list(self):
        assert (
            convert(
                """
* 
** 
- 
-- 
        """,
            )
            == """

- 
  - 
- 
  - 
        """
        )

    def test_text_indent(self):
        assert (
            convert(
                """
Some text
* 
""",
            )
            == """
Some text

- 
"""
        )

    def test_list_indent(self):
        assert (
            convert(
                """
  * One
      ** Two
 ** Three
""",
            )
            == """
- One
  - Two
  - Three
"""
        )


class TestOrderedList:
    def test_bullets(self):
        assert (
            convert(
                """
# a
# numbered
# list
## indented
## bullets
        """,
            )
            == """
1. a
1. numbered
1. list
   1. indented
   1. bullets
        """
        )

    def test_mixed_bullets(self):
        assert (
            convert(
                """
*# nested
*## numbered
*## list
        """,
            )
            == """
  1. nested
     1. numbered
     1. list
        """
        )

    def test_multiline(self):
        assert (
            convert(
                """
# Item
Line
Next

Break
""",
            )
            == """
1. Item
   Line
   Next

Break
"""
        )

    def test_start_indent(self):
        assert (
            convert(
                """
# First
## Second

## One
### Two

# Last
## One
""",
            )
            == """
1. First
   1. Second

## One
### Two

1. Last
   1. One
"""
        )

    def test_indent_step(self):
        assert (
            convert(
                """
# one
## two
#### four
""",
            )
            == r"""
1. one
   1. two
#### four
"""
        )

    def test_empty_list(self):
        assert (
            convert(
                """
# 
## 
        """,
            )
            == r"""
1. 
   1. 
        """
        )

    def test_list_indent(self):
        assert (
            convert(
                """
  # One
      ## Two
 ## Three
""",
            )
            == """
1. One
   1. Two
   1. Three
"""
        )
