from jira2markdown import convert


class TestImage:
    def test_basic_conversion(self):
        assert (
            convert("!http://www.example.com/image.png!")
            == "![http://www.example.com/image.png](http://www.example.com/image.png)"
        )
        assert convert("!attached-image.gif!") == "![attached-image.gif](attached-image.gif)"

    def test_thumbnail(self):
        assert convert("!image.jpg|thumbnail!") == "![image.jpg](image.jpg)"

    def test_match_start_conditions(self):
        assert convert("Hello!image.png!") == "Hello!image.png!"
        assert convert("Я!image.png!") == "Я!image.png!"
        assert convert("}!image.png!") == "}![image.png](image.png)"

    def test_url_line_break(self):
        assert convert("!http://example.\ncom/image.png!") == "!http://example.\ncom/image.png!"

    def test_image_attributes(self):
        assert convert("!image.jpg|width=300!") == "![image.jpg](image.jpg){width=300}"
        assert convert("!image.jpg| WIDTH  =  300 , HEIGHT=200!") == "![image.jpg](image.jpg){width=300 height=200}"
        assert convert("!image.jpg|align=right, vspace=4!") == "![image.jpg](image.jpg)"
