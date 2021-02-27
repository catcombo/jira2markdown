from jira2markdown.parser import convert


class TestMailTo:
    def test_basic_conversion(self):
        assert convert("[mailto:service@atlassian.com]") == "<service@atlassian.com>"

    def test_alias(self):
        assert convert("[Some text|mailto:service@atlassian.com]") == "<service@atlassian.com>"


class TestLink:
    def test_basic_conversion(self):
        assert convert("[http://jira.atlassian.com]") == "<http://jira.atlassian.com>"

    def test_alias(self):
        assert convert("[Atlassian|http://atlassian.com]") == "[Atlassian](http://atlassian.com)"

    def test_exceptions(self):
        assert convert("[Text in square brackets]") == "[Text in square brackets]"


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
