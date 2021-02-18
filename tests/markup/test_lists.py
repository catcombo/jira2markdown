from jira2markdown import convert


class TestUnorderedList:
    def test_bullets(self):
        assert convert("""
* some
* bullet
** indented
** bullets
* points
        """) == """
- some
- bullet
  - indented
  - bullets
- points
        """
        assert convert("""
- some
- bullet
-- indented
-- bullets
- points
        """) == """
- some
- bullet
  - indented
  - bullets
- points
        """

    def test_mixed_bullets(self):
        assert convert("""
#* nested
#** bullet
#** list
        """) == """
   - nested
     - bullet
     - list
        """

    def test_match_start_conditions(self):
        assert convert("* Item") == "- Item"
        assert convert("\n* Item") == "\n- Item"
        assert convert("  * Item") == r"  \* Item"

    def test_empty_list(self):
        assert convert("""
* 
** 
- 
-- 
        """) == r"""
\* 
\*\* 
- 
– 
        """


class TestOrderedList:
    def test_bullets(self):
        assert convert("""
# a
# numbered
# list
## indented
## bullets
        """) == """
1. a
1. numbered
1. list
   1. indented
   1. bullets
        """

    def test_mixed_bullets(self):
        assert convert("""
*# nested
*## numbered
*## list
        """) == """
  1. nested
     1. numbered
     1. list
        """
