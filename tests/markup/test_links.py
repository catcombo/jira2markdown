from jira2markdown.parser import convert


def test_mailto():
    assert convert("[mailto:service@atlassian.com]") == "<service@atlassian.com>"


def test_link():
    assert convert("[http://jira.atlassian.com]") == "<http://jira.atlassian.com>"
    assert convert("[Atlassian|http://atlassian.com]") == "[Atlassian](http://atlassian.com)"
    assert convert("[Text in square brackets]") == "[Text in square brackets]"


def test_attachment():
    assert convert("[^attachment.ext]") == "[attachment.ext](attachment.ext)"


def test_mention():
    usernames = {
        "1984:big-brother-101-love": "winston",
    }

    assert convert("[Firstname Lastname|~accountid:1984:big-brother-101-love]") == "@1984:big-brother-101-love"
    assert convert("[Firstname Lastname|~accountid:1984:big-brother-101-love]", usernames) == "@winston"

    assert convert("[~accountId:1984:big-brother-101-love]") == "@1984:big-brother-101-love"
    assert convert("[~accountid:1984:big-brother-101-love]", usernames) == "@winston"

    assert convert("[~1984:big-brother-101-love]") == "@1984:big-brother-101-love"
    assert convert("[~1984:big-brother-101-love]", usernames) == "@winston"
