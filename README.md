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

# Conversion tables

## Headings

| Jira | Markdown |
|------|----------|
|`h1. Biggest heading`|`# Biggest heading`|
|`h2. Bigger heading`|`## Bigger heading`|
|`h3. Big heading`|`### Big heading`|
|`h4. Normal heading`|`#### Normal heading`|
|`h5. Small heading`|`##### Small heading`|
|`h6. Smallest heading`|`###### Smallest heading`|

## Text Effects

| Jira | Markdown |
|------|----------|
|`*strong*`|`**strong**`|
|`_emphasis_`|Not converted (the same syntax)|
|`??citation??`|`<q>citation</q>`|
|`-deleted-`|`~~deleted~~`|
|`+inserted+`|`inserted`|
|`^superscript^`|`<sup>superscript</sup>`|
|`~subscript~`|`<sub>subscript</sub>`|
|`{{monospaced}}`|`` `monospaced` ``|
|`bq. Some block quoted text`|`> Some block quoted text`|
|`{quote}Content to be quoted{quote}`|`> Content to be quoted`|
|`{color:red}red text!{color}`|`<font color="red">red text!</font>`|

## Text Breaks

| Jira | Markdown |
|------|----------|
|`\\`|Line break|
|`---`|`—`|
|`--`|`–`|

## Links

| Jira | Markdown |
|------|----------|
|`[#anchor]`|Not converted|
|`[^attachment.ext]`|`[attachment.ext](attachment.ext)`|
|`[http://www.example.com]`|`<http://www.example.com>`|
|`[Example\|http://example.com]`|`[Example](http://example.com)`|
|`[mailto:box@example.com]`|`<box@example.com>`|
|`[file:///c:/temp/foo.txt]`|Not converted|
|`{anchor:anchorname}`|Not converted|
|`[~username]`|`@username`|

## Lists

<table>
<tr>
<th>Jira</th>
<th>Markdown</th>
</tr>
<tr>
<td>

```
* some
* bullet
** indented
** bullets
* points
```
</td>
<td>

```
- some
- bullet
  - indented
  - bullets
- points
```
</td>
</tr>
<tr>
<td>

```
# a
# numbered
# list
```
</td>
<td>

```
1. a
1. numbered
1. list
```
</td>
</tr>
<tr>
<td>

```
# a
# numbered
#* with
#* nested
#* bullet
# list
```
</td>
<td>

```
1. a
1. numbered
   - with
   - nested
   - bullet
1. list
```
</td>
</tr>
<tr>
<td>

```
* a
* bulleted
*# with
*# nested
*# numbered
* list
```
</td>
<td>

```
- a
- bulleted
  1. with
  1. nested
  1. numbered
- list
```
</td>
</tr>
</table>

## Images

<table>
<tr>
<th>Jira</th>
<th>Markdown</th>
</tr>
<tr>
<td>

```
!image.jpg!
!image.jpg|thumbnail!
!image.gif|align=right, vspace=4!
```
</td>
<td>

```
![image.jpg](image.jpg)
```
</td>
</tr>
</table>

## Tables

<table>
<tr>
<th>Jira</th>
<th>Markdown</th>
</tr>
<tr>
<td>

```
||heading 1||heading 2||heading 3||
|col A1|col A2|col A3|
|col B1|col B2|col B3|

```
</td>
<td>

```
|heading 1|heading 2|heading 3|
|-|-|-|
|col A1|col A2|col A3|
|col B1|col B2|col B3|
```
</td>
</tr>
</table>

## Advanced Formatting

<table>
<tr>
<th>Jira</th>
<th>Markdown</th>
</tr>
<tr>
<td>

```
{noformat}
preformatted piece of text
 so *no* further _formatting_ is done here
{noformat}
```
</td>
<td>

````
```
preformatted piece of text
 so *no* further _formatting_ is done here
```
````
</td>
</tr>
<tr>
<td>

```
{panel:title=My Title}
Some text with a title
{panel}
```
</td>
<td>

```
> **My Title**
> Some text with a title
```
</td>
</tr>
<tr>
<td>

```
{code:xml}
    <test>
        <another tag="attribute"/>
    </test>
{code}
```
</td>
<td>

````
```xml
    <test>
        <another tag="attribute"/>
    </test>
```
````
</td>
</tr>
</table>
