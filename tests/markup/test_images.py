from jira2markdown import convert


def test_image():
    assert convert("!http://www.example.com/image.png!") == \
           "![http://www.example.com/image.png](http://www.example.com/image.png)"
    assert convert("!image.jpg|thumbnail!") == "![image.jpg](image.jpg)"


def test_image_constraints():
    assert convert("Hello!image.png!") == "Hello!image.png!"
    assert convert("}!image.png!") == "}![image.png](image.png)"
    assert convert("!http://example.\ncom/image.png!") == "!http://example.\ncom/image.png!"


def test_image_attributes():
    assert convert("!image.jpg|width=300!") == "![image.jpg](image.jpg){width=300}"
    assert convert("!image.jpg|width=300,height=200!") == "![image.jpg](image.jpg){width=300}{height=200}"
