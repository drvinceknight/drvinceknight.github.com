# vknight.org

Personal website for [vknight.org](https://vknight.org), built with a small
Python static site generator.

All content lives in `src/*.md` as markdown files with YAML frontmatter.
A `tags` field determines how each file is rendered:

| Tag            | Output path                         | Description               |
| -------------- | ----------------------------------- | ------------------------- |
| `post`         | `posts/{slug}/index.html`           | Blog post (with comments) |
| `article`      | `posts/{slug}/index.html`           | Journal article           |
| `book`         | `posts/{slug}/index.html`           | Book                      |
| `software`     | `posts/{slug}/index.html`           | Software project          |
| `course`       | `posts/{slug}/index.html`           | Teaching course           |
| `collaborator` | `collaborators/{slug}/index.html`   | Research collaborator     |
| `student`      | `collaborators/{slug}/index.html`   | Research student          |
| `page`         | `{slug}/index.html`                 | Static page (e.g. CV)     |

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
uv sync --group dev
```

## Build

```bash
uv run python build.py
```

Outputs are written in-place (HTML to the repo root, LaTeX/bio to
`assets/cv/`).  Preview with:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

## Code quality

Format with [ruff](https://docs.astral.sh/ruff/):

```bash
uv run ruff format build.py migrate.py
```

Lint:

```bash
uv run ruff check build.py migrate.py
```

Type-check with [ty](https://github.com/astral-sh/ty):

```bash
uv run ty check build.py migrate.py
```

## Migration (one-off)

`migrate.py` converts the old Jekyll collection structure to the unified
`src/` layout.  It only needs to be run once:

```bash
uv run python migrate.py
```

## Deployment

GitHub Actions deploys on every push to `master`.  The workflow uploads the
entire repo root as a GitHub Pages artifact — no build step in CI.
