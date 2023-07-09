# HPS 2023 Team 10 Conventional commits

The commit message should be structured as follows:

```git
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

The commit contains the following structural elements, to communicate intent to the consumers of your library:

1. fix: a commit of the *type* `fix` patches a bug in your codebase .
2. feat: a commit of the *type* `feat` introduces a new feature to the codebase.
3. BREAKING CHANGE: a commit that has a footer `BREAKING CHANGE:`, or appends a `!` after the type/scope, introduces a breaking API change. A BREAKING CHANGE can be part of commits of any *type*.
4. *types* other than `fix`: and `feat`: are allowed, for example `build:`, `chore:`, `ci:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, and others.
5. *footers* other than `BREAKING CHANGE: <description>` may be provided.

Additional types are not mandated by the Conventional Commits specification, and have no implicit effect in Semantic Versioning (unless they include a `BREAKING CHANGE`). A scope may be provided to a commit’s type, to provide additional contextual information and is contained within parenthesis, e.g., `feat(parser): add ability to parse arrays.`

For examples and further guides, follow:
https://www.conventionalcommits.org/en/v1.0.0/.