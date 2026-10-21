[![Build Status][ci-badge]][ci-link]
[![codecov.io][codecov-badge]][codecov-link]
[![PyPI version][pypi-badge]][pypi-link]

# mdformat-myst

> Mdformat plugin for MyST compatibility

## Description

[Mdformat](https://github.com/executablebooks/mdformat) is a formatter for
[CommonMark](https://spec.commonmark.org/current/)
compliant Markdown.

Mdformat-myst is an mdformat plugin that changes the target specification to
[MyST](https://myst-parser.readthedocs.io/en/latest/using/syntax.html),
making the tool able to format the following syntax extensions:

- [tables](https://github.github.com/gfm/#tables-extension-)
- [directives](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-directives)
- [roles](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-roles)
- [inline and block "dollar math"](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#math-shortcuts)
- [comments](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-comments)
- [block breaks](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-blockbreaks)
- [targets](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-targets)
- [front matter](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#extended-block-tokens)
- [footnotes](https://pandoc.org/MANUAL.html#footnotes)

In addition, the following optional MyST syntax extensions are supported and
enabled by default:

- [`colon_fence`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#code-fences-using-colons) —
  colon-fenced directives (`:::{note}`). Directive bodies are recursively
  formatted as Markdown (except for well-known literal-content directives
  such as `{eval-rst}` or `{code-cell}`).
- [`deflist`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists) —
  definition lists (via the `mdformat-deflist` plugin).
- [`tasklist`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#task-lists) —
  GitHub-style task lists (`- [x] done`).
- [`fieldlist`](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#field-lists) —
  field lists (`:name: value`).

## Install

```sh
pip install mdformat-myst
```

## Usage

```sh
mdformat <filename>
```

### Disabling syntax extensions

Each optional syntax extension can be disabled individually, either with a
CLI flag:

```sh
mdformat --myst-no-colon-fence --myst-no-deflist --myst-no-tasklist --myst-no-fieldlist <filename>
```

or in the `.mdformat.toml` configuration file:

```toml
[plugin.myst]
colon_fence = false
deflist = false
tasklist = false
fieldlist = false
```

Note that mdformat's CLI enables *all installed* plugins by default, and
`mdformat-deflist` and `mdformat-gfm` (which provides task list support) are
installed as dependencies of this package. The toggles above only control
whether *this plugin* activates the corresponding syntax. To fully disable a
syntax when running the `mdformat` CLI, additionally restrict the enabled
plugins with an allowlist in `.mdformat.toml`, e.g.:

```toml
extensions = ["myst"]
```

[ci-badge]: https://github.com/executablebooks/mdformat-myst/actions/workflows/tests.yml/badge.svg?branch=master
[ci-link]: https://github.com/executablebooks/mdformat-myst/actions?query=workflow%3ATest+branch%3Amaster+event%3Apush
[codecov-badge]: https://codecov.io/gh/executablebooks/mdformat-myst/branch/master/graph/badge.svg
[codecov-link]: https://codecov.io/gh/executablebooks/mdformat-myst
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-myst.svg
[pypi-link]: https://pypi.org/project/mdformat-myst
