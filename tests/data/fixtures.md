Table
.
a | b | c
:- | -: | :-:
1 | 2 | 3
xxxxxx | yyyyyy | zzzzzz
.
| a      |      b |   c    |
| :----- | -----: | :----: |
| 1      |      2 |   3    |
| xxxxxx | yyyyyy | zzzzzz |
.

Table escape
.
| a |
\| - |
.
| a |
| \- |
.

MyST Role
.
Euler's identity, equation {math:numref}`euler`, was elected one of the
most beautiful mathematical formulas.
.
Euler's identity, equation {math:numref}`euler`, was elected one of the
most beautiful mathematical formulas.
.

MyST Role escape
.
Escaped role {math:numref\}`euler`, right there
.
Escaped role \{math:numref}`euler`, right there
.

MyST LineComment
.
a line
% a comment
another line
.
a line

% a comment

another line
.

MyST LineComment - multiline
.
a line
% a multiline
%comment
%      yep

% another comment
.
a line

% a multiline
%comment
%      yep

% another comment
.

MyST LineComment escape
.
a line
\% a comment
another line
.
a line
\% a comment
another line
.

MyST BlockBreak
.
a line
+++ a block break
another line
.
a line

+++ a block break

another line
.

MyST BlockBreak: empty content
.
a line
+++ 
another line
.
a line

+++

another line
.

MyST BlockBreak escape
.
a line
++\+ NOT a block break
another line
.
a line
\+++ NOT a block break
another line
.

MyST Target
.
(myst_target)=
That's a myst target^
.
(myst_target)=

That's a myst target^
.

MyST Target escape
.
(myst_target\)=
That's a myst target^
The escape has no effect
.
(myst_target\)=

That's a myst target^
The escape has no effect
.

Dollarmath inline
.
Inline math: $a=1$
.
Inline math: $a=1$
.

Dollarmath inline escape
.
Escaped inline math: $a=1\$
.
Escaped inline math: \$a=1\$
.

Dollarmath block
.
Block math:

$$
a=1
$$
.
Block math:

$$
a=1
$$
.

Dollarmath block escape
.
$$
a=1
$\$
.
\$$
a=1
$\$
.

Dollarmath block labeled
.
Labeled block math:

$$
a=1
$$ (eq1)
.
Labeled block math:

$$
a=1
$$ (eq1)
.

Blockquote with dollarmath block
.
> $$
a=1
$$
.
> $$
a=1
$$
.

Long blockquote with dollarmath block
.
> Some words
>
> Block math:
>
> $$
a=1
$$
>
> Some more words
.
> Some words
>
> Block math:
>
> $$
a=1
$$
>
> Some more words
.

Blockquote with dollarmath block labeled
.
> $$
a=1
$$ (eq1)
.
> $$
a=1
$$ (eq1)
.

Long blockquote with dollarmath block labeled
.
> Some words
>
> Block math:
>
> $$
a=1
$$ (eq1)
>
> Some more words
.
> Some words
>
> Block math:
>
> $$
a=1
$$ (eq1)
>
> Some more words
.

Indented dollarmath block
.
1. Indented math block

   $$
   a=1
   $$
.
1. Indented math block

   $$
   a=1
   $$
.

Indented dollarmath block labeled
.
1. Indented labeled math block

   $$
   a=1
   $$ (eq1)
.
1. Indented labeled math block

   $$
   a=1
   $$ (eq1)
.

Frontmatter
.
---
lastname: Blorothy
firstname: Dorothy
---
Thats YAML front matter^
.
---
lastname: Blorothy
firstname: Dorothy
---

Thats YAML front matter^
.

Frontmatter escape
.
--\-
not frontmatter
-\--

Thats not YAML front matter^
.
\---
not frontmatter
\---

Thats not YAML front matter^
.


Footnotes
.
# Now some markdown
Here is a footnote reference,[^1] and another.[^longnote]
[^1]: Here is the footnote.
[^longnote]: Here's one with multiple blocks.

    Subsequent paragraphs are indented to show that they
belong to the previous footnote.

    Third paragraph here.
.
# Now some markdown

Here is a footnote reference,[^1] and another.[^longnote]

[^1]: Here is the footnote.

[^longnote]: Here's one with multiple blocks.

    Subsequent paragraphs are indented to show that they
    belong to the previous footnote.

    Third paragraph here.
.

Move footnote definitions to the end (but before link ref defs)
.
[link]: https://www.python.org
[^1]: Here is the footnote.

# Now we reference them
Here is a footnote reference[^1]
Here is a [link]

.
# Now we reference them

Here is a footnote reference[^1]
Here is a [link]

[^1]: Here is the footnote.

[link]: https://www.python.org
.

footnote-indentation
.
[^a]

[^a]: first paragraph with
unindented next line.

    paragraph with
    indented next line

    paragraph with
unindented next line

    ```
    content
    ```
.
[^a]

[^a]: first paragraph with
    unindented next line.

    paragraph with
    indented next line

    paragraph with
    unindented next line

    ```
    content
    ```
.


MyST directive YAML
.
``` {some-directive} args
  :option1:  1
  :option2:   hello
Content
```

``` {some-directive} args
  :option1:  1
  :option2:   hello

Content
```

``` {some-directive} args
---
option1:  1
option2:   hello
---
Content
```

``` {some-directive} args
---
  option1:  1
  option2:   hello
---

Content
```
.
```{some-directive} args
:option1: 1
:option2: hello

Content
```

```{some-directive} args
:option1: 1
:option2: hello

Content
```

```{some-directive} args
:option1: 1
:option2: hello

Content
```

```{some-directive} args
:option1: 1
:option2: hello

Content
```
.


MyST directive empty YAML
.
``` {some-directive} args
  :
Content
```
.
```{some-directive} args
Content
```
.

MyST directive no content
.
``` {some-directive} args
  :letter: a

```
.
```{some-directive} args
:letter: a
```
.

MyST directive, no opts or content
.
``` {some-directive} args
```
.
```{some-directive} args
```
.

MyST colon fenced directive with title
.
:::{admonition} MyST colon fenced directive with a title
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua.
:::
.
:::{admonition} MyST colon fenced directive with a title
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua.
:::
.

MyST colon fenced directive with metadata
.
:::{admonition} MyST colon fenced directive with metadata
:class: foo
:truc: bla
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua.
:::
.
:::{admonition} MyST colon fenced directive with metadata
:class: foo
:truc: bla

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua.
:::
.

MyST colon fenced directive with nested directive
.
::::{admonition} Parent directive
:::{image} foo.png
---
class: foo
alt: An image
---
:::
::::
.
::::{admonition} Parent directive

:::{image} foo.png
:class: foo
:alt: An image
:::

::::
.

MyST colon fenced directive with multiple nested admonitions
.
::::{admonition} Multiple nested admonitions
:::{admonition}
First nested admonition content.
:::
:::{admonition}
Second nested admonition content.
:::
:::{admonition}
Third nested admonition content.
:::
::::
.
::::{admonition} Multiple nested admonitions

:::{admonition}
First nested admonition content.
:::

:::{admonition}
Second nested admonition content.
:::

:::{admonition}
Third nested admonition content.
:::

::::
.

MyST colon fenced directive with mixed content and nested directives
.
::::{hint} A hint with nested tips and paragraphs
This is some introductory text.
:::{tip}
A nested tip with content.
:::
More text between directives.
:::{tip}
Another nested tip.
:::
Concluding text.
::::
.
::::{hint} A hint with nested tips and paragraphs
This is some introductory text.

:::{tip}
A nested tip with content.
:::

More text between directives.

:::{tip}
Another nested tip.
:::

Concluding text.
::::
.

MyST colon fenced directive nested in list
.
- Item with directive
  :::{tip} Nested tip in list item
  Tip content inside a list item.
  :::
.
- Item with directive
  :::{tip} Nested tip in list item
  Tip content inside a list item.
  :::
.

MyST colon fenced directive info string is not escaped (issue 13)
.
:::{note}
A note.
:::
.
:::{note}
A note.
:::
.

MyST colon fenced directive body is formatted as Markdown
.
:::{note}
Heading
=======

*  bullet
:::
.
:::{note}
# Heading

- bullet
:::
.

MyST colon fenced directive, empty
.
:::{note}
:::
.
:::{note}
:::
.

Backtick eval-rst directive body is left untouched
.
```{eval-rst}
.. dargs::
   :module: deepmd.utils.argcheck
   :func: gen_args_multi_task
```
.
```{eval-rst}
.. dargs::
   :module: deepmd.utils.argcheck
   :func: gen_args_multi_task
```
.

Colon fenced eval-rst directive body is left untouched
.
:::{eval-rst}
.. note::
   indented RST
:::
.
:::{eval-rst}
.. note::
   indented RST
:::
.

Backtick code fence content starting with colons is not mangled
.
```text
:::
not a directive
```
.
```text
:::
not a directive
```
.

Paragraph line starting with three colons is escaped
.
foo
\::: bar
.
foo
\::: bar
.

Definition list, tight
.
Term 1
: Definition 1
.
Term 1
: Definition 1
.

Definition list, multiple definitions and terms
.
Term 1
: Definition 1a
: Definition 1b

Term 2
: Definition 2
.
Term 1
: Definition 1a
: Definition 1b

Term 2
: Definition 2
.

Definition list, loose with multi-paragraph definition
.
Term
: First paragraph.

  Second paragraph.
.
Term

: First paragraph.

  Second paragraph.
.

Definition list inside colon fenced directive
.
:::{note}
Term
: Definition
:::
.
:::{note}
Term
: Definition
:::
.

Paragraph line starting with a colon is escaped
.
foo
\: not a definition
.
foo
\: not a definition
.

Task list
.
- [ ] not done
- [x] done
.
- [ ] not done
- [x] done
.

Task list, checkmark normalized to lowercase
.
- [X] done
.
- [x] done
.

Task list nested in ordered list
.
1. [x] top
   - [ ] nested
   - [x] nested done
.
1. [x] top
   - [ ] nested
   - [x] nested done
.

Task list item with continuation paragraph
.
- [ ] task

  second paragraph with [x] literal
.
- [ ] task

  second paragraph with [x] literal
.

Task list inside colon fenced directive
.
:::{note}
- [ ] todo in note
:::
.
:::{note}
- [ ] todo in note
:::
.

Literal bracket-x list item is escaped
.
- \[x\] not a task
.
- \[x\] not a task
.

Field list, simple
.
:author: Jane Doe
:date: 2026-10-21
.
:author: Jane Doe
:date: 2026-10-21
.

Field list, empty body
.
:orphan:
.
:orphan:
.

Field list, multiline and multi-paragraph body
.
:abstract: First line
   continued line

   second paragraph
.
:abstract: First line
  continued line

  second paragraph
.

Field list, body indented more than first line
.
:name:
      Deeply indented body
.
:name: Deeply indented body
.

Field list, inline markup in name
.
:*emphasized* name: body
.
:*emphasized* name: body
.

Field list, non-paragraph body
.
:code:
  ```
  literal
  ```
.
:code:
  ```
  literal
  ```
.

Field list inside colon fenced directive
.
:::{py:function} foo

:param x: a parameter
:::
.
:::{py:function} foo

:param x: a parameter
:::
.

Colon fenced directive options are kept distinct from a field list body
.
:::{py:function} foo
:param x: a parameter
:::
.
:::{py:function} foo
:param x: a parameter
:::
.

Paragraph line resembling a field marker is escaped
.
para
\:not: a field
.
para
\:not: a field
.

Directive option without a value
.
:::{toctree}
:hidden:
item
:::
.
:::{toctree}
:hidden:

item
:::
.

Directive options with complex values keep the YAML style
.
:::{dir}
---
items:
  - a
  - b
---
body
:::
.
:::{dir}
---
items:
  - a
  - b
---
body
:::
.

Footnote used only in admonition
.
```{note}
Hello mdformat[^myref]
```

[^myref]: my ref here
.
```{note}
Hello mdformat[^myref]
```

[^myref]: my ref here
.

Link reference used only in admonition
.
```{note}
Hello [mdformat][myref]
```

[myref]: https://example.com
[unused]: https://unused.example
.
```{note}
Hello [mdformat][myref]
```

[myref]: https://example.com
.

Footnote used only in colon fenced directive
.
:::{note}
Hello[^fn]
:::

[^fn]: a footnote
.
:::{note}
Hello[^fn]
:::

[^fn]: a footnote
.

Link reference used only in colon fenced directive
.
:::{note}
Hello [mdformat][myref]
:::

[myref]: https://example.com
[unused]: https://unused.example
.
:::{note}
Hello [mdformat][myref]
:::

[myref]: https://example.com
.

Link reference used only in nested colon fenced directive
.
::::{admonition} Outer
:::{note}
See [docs][ref1]
:::
::::

[ref1]: https://example.com
.
::::{admonition} Outer

:::{note}
See [docs][ref1]
:::

::::

[ref1]: https://example.com
.

Reference link with code span in label inside colon fenced directive
.
:::{note}
Use the [`--trust` flag][trust-flag] to allow this.
:::

[trust-flag]: https://example.com/docs#trust
.
:::{note}
Use the [`--trust` flag][trust-flag] to allow this.
:::

[trust-flag]: https://example.com/docs#trust
.

Reference definition inside colon fenced directive moves to document end
.
:::{note}
See [docs][inner-ref].

[inner-ref]: https://inner.example
:::
.
:::{note}
See [docs][inner-ref].
:::

[inner-ref]: https://inner.example
.

Directive option with a long value stays in colon syntax
.
```{code-block} yaml
:caption: e.g. `/etc/salt/minion.d/github.yml` or `/srv/pillar/github.sls` with associated mapping in `top.sls`
# Requires a corresponding SDB profile in the minion configuration, see above
github:
  token: sdb://osenv/GITHUB_TOKEN
  owner: my_organization
```
.
```{code-block} yaml
:caption: e.g. `/etc/salt/minion.d/github.yml` or `/srv/pillar/github.sls` with associated mapping in `top.sls`

# Requires a corresponding SDB profile in the minion configuration, see above
github:
  token: sdb://osenv/GITHUB_TOKEN
  owner: my_organization
```
.

Autodoc directive body is left untouched
.
:::{automodule} mymodule
:members:

.. rubric:: Details
   with indented RST
:::
.
:::{automodule} mymodule
:members:

.. rubric:: Details
   with indented RST
:::
.
