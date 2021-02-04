# jira2markdown

`jira2markdown` is a text converter from [JIRA markup](https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=all) to [YouTrack Markdown](https://www.jetbrains.com/help/youtrack/standalone/youtrack-markdown-syntax-issues.html) using parsing expression grammars. The Markdown implementation in YouTrack follows the [CommonMark specification](https://spec.commonmark.org/0.29/) with extensions. Thus, `jira2markdown` can be used to convert text to any Markdown syntax with minimal modifications.

# Prerequisites

- Python 3.6+

# Installation

```
pip install jira2markdown
```

# Usage

```python
from jira2markdown import convert

convert("Some *Jira text* formatting [example|https://example.com].")
# >>> Some **Jira text** formatting [example](https://example.com).

# To convert user mentions provide a mapping Jira internal account id to username 
# as a second argument to convert function
convert("[Winston Smith|~accountid:internal-id] woke up with the word 'Shakespeare' on his lips", {
    "internal-id": "winston",
})
# >>> @winston woke up with the word 'Shakespeare' on his lips
```
