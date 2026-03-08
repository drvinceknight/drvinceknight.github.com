#!/usr/bin/env python3
"""One-time migration from Jekyll collections to a unified src/ directory.

Reads from the old Jekyll directories (_posts, _articles, _books, _software,
_courses, _collaborators) and writes normalised frontmatter files to src/.

Usage:
    uv run python migrate.py
"""

from __future__ import annotations

import pathlib
import re

import frontmatter
import yaml

SRC_DIR = pathlib.Path("./src")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fix_content(content: str) -> str:
    """Strip Jekyll template variables from markdown content."""
    content = content.replace("{{site.baseurl}}", "")
    content = content.replace("{{ site.baseurl }}", "")
    return content


def write_src(filename: str, metadata: dict, content: str = "") -> None:
    """Write a frontmatter file to src/."""
    SRC_DIR.mkdir(exist_ok=True)
    post = frontmatter.Post(content=content, **metadata)
    path = SRC_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
    print(f"  -> {path}")


# ---------------------------------------------------------------------------
# Migration steps
# ---------------------------------------------------------------------------


def migrate_posts() -> None:
    """Migrate _posts/*.md → src/ with tag: post."""
    print("Migrating posts...")
    for path in pathlib.Path("_posts").glob("*.md"):
        post = frontmatter.load(path)
        meta = dict(post.metadata)
        meta.pop("layout", None)
        meta["tags"] = ["post"]
        write_src(path.name, meta, fix_content(post.content))


def migrate_articles() -> None:
    """Migrate _articles/*.md → src/ with tag: article."""
    print("Migrating articles...")
    for path in pathlib.Path("_articles").glob("*.md"):
        post = frontmatter.load(path)
        meta = dict(post.metadata)
        meta.pop("layout", None)
        meta["tags"] = ["article"]
        write_src(path.name, meta, post.content)


def migrate_books() -> None:
    """Migrate _books/*.md → src/ with tag: book."""
    print("Migrating books...")
    for path in pathlib.Path("_books").glob("*.md"):
        post = frontmatter.load(path)
        meta = dict(post.metadata)
        meta.pop("layout", None)
        meta["tags"] = ["book"]
        write_src(path.name, meta, post.content)


def migrate_software() -> None:
    """Migrate _software/*.md → src/ with tag: software."""
    print("Migrating software...")
    for path in pathlib.Path("_software").glob("*.md"):
        post = frontmatter.load(path)
        meta = dict(post.metadata)
        meta.pop("layout", None)
        meta["tags"] = ["software"]
        write_src(path.name, meta, post.content)


def migrate_courses() -> None:
    """Migrate _courses/ → src/, merging .md and .yml files where both exist."""
    print("Migrating courses...")
    course_dir = pathlib.Path("_courses")
    processed_stems: set[str] = set()

    for md_path in course_dir.glob("*.md"):
        stem = md_path.stem
        processed_stems.add(stem)
        post = frontmatter.load(md_path)
        meta = dict(post.metadata)
        meta.pop("layout", None)
        meta["tags"] = ["course"]

        yml_path = course_dir / f"{stem}.yml"
        if yml_path.exists():
            with open(yml_path, encoding="utf-8") as f:
                yml_data: dict = yaml.safe_load(f) or {}
            for key in ("level", "url"):
                if key in yml_data and key not in meta:
                    meta[key] = yml_data[key]
            if "url" in yml_data and "direct_url" not in meta:
                meta["direct_url"] = yml_data["url"]

        write_src(md_path.name, meta, fix_content(post.content))

    # Handle .yml-only course files (no corresponding .md)
    for yml_path in course_dir.glob("*.yml"):
        stem = yml_path.stem
        if stem in processed_stems:
            continue
        with open(yml_path, encoding="utf-8") as f:
            yml_data = yaml.safe_load(f) or {}
        meta = dict(yml_data)
        meta["tags"] = ["course"]
        if "url" in meta:
            meta["direct_url"] = meta.pop("url")
        write_src(f"{stem}.md", meta, "")


def migrate_collaborators() -> None:
    """Migrate _collaborators/*.md → src/.

    Collaborators get tag: collaborator.
    Students (category: student) get tag: student plus their degree tags.
    """
    print("Migrating collaborators...")
    for path in pathlib.Path("_collaborators").glob("*.md"):
        post = frontmatter.load(path)
        meta = dict(post.metadata)
        meta.pop("layout", None)

        name = meta.pop("name", None)
        if name:
            meta["title"] = name

        category = meta.pop("category", None)
        old_tags: list[str] = list(meta.pop("tags", []))

        if category == "student":
            meta["tags"] = ["student"] + old_tags
        else:
            meta["tags"] = ["collaborator"]

        write_src(path.name, meta, fix_content(post.content))


def migrate_cv() -> None:
    """Migrate cv.md → src/cv.md, stripping Liquid template tags."""
    print("Migrating CV...")
    cv_path = pathlib.Path("cv.md")
    if not cv_path.exists():
        print("  (cv.md not found, skipping)")
        return
    post = frontmatter.load(cv_path)
    meta = dict(post.metadata)
    meta.pop("layout", None)
    meta.pop("permalink", None)
    meta["tags"] = ["page"]
    content = re.sub(r"\{%.*?%\}", "", post.content, flags=re.DOTALL)
    content = re.sub(r"\{\{.*?\}\}", "", content)
    write_src("cv.md", meta, content.strip())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Run all migration steps."""
    SRC_DIR.mkdir(exist_ok=True)
    migrate_posts()
    migrate_articles()
    migrate_books()
    migrate_software()
    migrate_courses()
    migrate_collaborators()
    migrate_cv()
    print("\nDone. Review src/, then run: uv run python build.py")


if __name__ == "__main__":
    main()
