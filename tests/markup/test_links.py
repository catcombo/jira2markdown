from jira2markdown.parser import convert


class TestMailTo:
    def test_basic_conversion(self):
        assert convert("[mailto:box@example.com]") == "<box@example.com>"

    def test_alias(self):
        assert convert("[box@example.com|mailto:box@example.com]") == "<box@example.com>"
        assert convert("[Some text|mailto:home_box@domain-name.com]") == "[Some text](mailto:home_box@domain-name.com)"


class TestLink:
    def test_basic_conversion(self):
        assert convert("[http://example.com]") == "<http://example.com>"
        assert convert("[ftp://example.com]") == "<ftp://example.com>"
        assert convert("[WWW.EXAMPLE.COM]") == "<https://WWW.EXAMPLE.COM>"

    def test_alias(self):
        assert convert("[Example text|http://example.com]") == "[Example text](http://example.com)"

    def test_text(self):
        assert convert("[Text in square brackets]") == "[Text in square brackets]"
        assert convert("[Some text|]") == r"[Some text\|]"
        assert convert("[Some text|More text]") == r"[Some text\|More text]"


class TestAttachment:
    def test_basic_conversion(self):
        assert convert("[^attachment.ext]") == "[attachment.ext](attachment.ext)"


class TestMention:
    USERNAMES = {
        "100:internal-id": "elliot",
    }

    def test_basic_conversion(self):
        assert convert("[~100:internal-id]") == "@100:internal-id"
        assert convert("[~100:internal-id]", self.USERNAMES) == "@elliot"

    def test_prefix(self):
        assert convert("[~accountId:100:internal-id]") == "@100:internal-id"
        assert convert("[~accountid:100:internal-id]", self.USERNAMES) == "@elliot"

    def test_alias(self):
        assert convert("[Firstname Lastname|~accountid:100:internal-id]") == "@100:internal-id"
        assert convert("[Firstname Lastname|~accountid:100:internal-id]", self.USERNAMES) == "@elliot"

    def test_spacing(self):
        assert convert("text[~userA]") == "text @userA"
        assert convert("[~userA]text") == "@userA text"
        assert convert("[~userA][~userB]") == "@userA @userB"
        assert convert("[~userA] [~userB]") == "@userA @userB"
        assert convert("[~userA]\t[~userB]") == "@userA\t@userB"
        assert convert("[~userA]\n[~userB]") == "@userA\n@userB"

    def test_punctuation(self):
        assert convert("[~userA].") == "@userA."
        assert convert("[~userA]:") == "@userA:"
        assert convert("[~userA]?") == "@userA?"
