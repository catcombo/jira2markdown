from jira2markdown import convert


def test_unordered_list():
    assert convert("""
* some
* bullet
** indented
** bullets
-- dashed
- points
""") == """
- some
- bullet
  - indented
  - bullets
  - dashed
- points
"""
    assert convert("""
#* nested
#** bullet
#** list
""") == """
   - nested
     - bullet
     - list
"""
    assert convert("""
*bullet
**indented
-dashed
--points
- 
-- 
""") == r"""
\*bullet
\*\*indented
-dashed
--points
- 
– 
"""


def test_ordered_list():
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
    assert convert("""
*# nested
*## numbered
*## list
""") == """
  1. nested
     1. numbered
     1. list
"""
