---
key: value
---

(myst_target)=

# Header

% a comment
%   with indentation

+++ a block break

MyST role: {name}`content`

MyST directive:

```{name} arguments
:option1: 1
:option2: hello

Content
```

table:

| a      |      b |   c    |
| :----- | -----: | :----: |
| 1      |      2 |   3    |
| xxxxxx | yyyyyy | zzzzzz |

dollar math:

$$
a=1
$$

colon fenced directive:

:::{note}
A note with *formatted* Markdown content.
:::

definition list:

Term 1
: Definition 1

task list:

- [ ] not done
- [x] done

field list:

:author: Jane Doe
:orphan:

Here is a footnote reference.[^a]

[^a]: First paragraph with
    two lines.

    ```
    content
    ```
