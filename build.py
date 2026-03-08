#!/usr/bin/env python3
"""Build script for vknight.org.

Reads all content from src/*.md and src/*.ipynb, renders Jinja2 templates,
and writes static HTML to the repo root.  Also generates LaTeX CV, short CV,
and bio text into assets/cv/.

Usage:
    uv run python build.py
"""

from __future__ import annotations

import collections
import html
import pathlib
import re
from typing import Any

import frontmatter
import jinja2
import markdown as md_module
import nbformat
import networkx as nx
import numpy as np

Post = dict[str, Any]

BLOG_TITLE = "Vincent Knight"
ROOT = "https://vknight.org"
DESCRIPTION = (
    "I am a professor of Mathematics at Cardiff University. "
    "My interests are in teaching, research software, "
    "Game Theory and applied stochastic modelling."
)

RESEARCH_INTERESTS: list[str] = [
    "Game Theory: Strategic behaviour in queues and the Iterated Prisoner's Dilemma",
    "Pedagogy: Active learning approaches",
    "Healthcare: Applied modelling of patient flow",
    "Markov modelling: Queueing processes and evolutionary dynamics",
]

# Maps lowercase degree tags to display strings.
DEGREE_NORMALISE: dict[str, str] = {
    "bsc.": "BSc",
    "bsc": "BSc",
    "msc": "MSc",
    "mmath": "MMath",
    "phd": "PhD",
    "summer": "Short placement",
    "google summer of code": "Short placement",
    "nuffield research placement": "Short placement",
}

_DEGREE_COLOURS: list[tuple[str, str]] = [
    ("PhD", "var(--accent)"),
    ("MSc", "var(--teal)"),
    ("MMath", "var(--green)"),
    ("BSc", "var(--yellow)"),
    ("Short placement", "var(--accent-warm)"),
]


def slugify(text: str) -> str:
    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def latex_escape(text: str) -> str:
    """Escape LaTeX special characters and strip non-ASCII (emoji etc.)."""
    text = str(text)
    for old, new in [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]:
        text = text.replace(old, new)
    return re.sub(r"[^\x00-\x7F]", "", text)


def stacked_bar_chart_svg(
    year_data: dict[int, dict[str, int]],
    categories: list[str],
    colours: list[str],
) -> str:
    """Inline SVG stacked bar chart.  year_data maps year → {category: count}."""
    if not year_data:
        return ""

    years = sorted(year_data.keys())
    W, H, pad_b, pad_t = 560, 220, 55, 20
    max_val = max(sum(year_data[y].values()) for y in years) or 1
    slot = W / len(years)
    bar_w = slot * 0.6
    gap = slot * 0.4

    parts: list[str] = []
    for i, year in enumerate(years):
        x = i * slot + gap / 2
        y_stack = H - pad_b
        for cat, colour in zip(categories, colours, strict=True):
            count = year_data[year].get(cat, 0)
            if not count:
                continue
            bar_h = (count / max_val) * (H - pad_b - pad_t)
            y_stack -= bar_h
            parts.append(
                f'<rect x="{x:.1f}" y="{y_stack:.1f}" width="{bar_w:.1f}" '
                f'height="{bar_h:.1f}" fill="{colour}" rx="2" opacity="0.85">'
                f"<title>{cat}: {count}</title></rect>"
            )
        parts.append(
            f'<text x="{x + bar_w / 2:.1f}" y="{H - pad_b + 14}" '
            f'text-anchor="middle" font-size="11" fill="currentColor">{year}</text>'
        )

    n = len(categories)
    item_w = 80
    legend_x = (W - n * item_w) / 2
    legend_y = H - 8
    for j, (cat, colour) in enumerate(zip(categories, colours, strict=True)):
        lx = legend_x + j * item_w
        parts.append(
            f'<rect x="{lx:.1f}" y="{legend_y - 9}" width="9" height="9" fill="{colour}" rx="2"/>'
        )
        parts.append(
            f'<text x="{lx + 13:.1f}" y="{legend_y}" font-size="10"'
            f' fill="currentColor">{cat}</text>'
        )

    return f'<svg viewBox="0 0 {W} {H}" style="width:100%;opacity:0.9">' + "".join(parts) + "</svg>"


def bar_chart_svg(
    data: list[tuple[str, int]],
    colour: str = "var(--accent)",
    colours: list[str] | None = None,
) -> str:
    """Inline SVG bar chart.  Pass *colours* for per-bar colouring."""
    if not data:
        return ""

    W, H, pad_b, pad_t = 560, 180, 40, 20
    max_val = max(v for _, v in data) or 1
    slot = W / len(data)
    bar_w = slot * 0.6
    gap = slot * 0.4

    rects: list[str] = []
    labels: list[str] = []
    for i, (label, val) in enumerate(data):
        bar_colour = colours[i] if colours and i < len(colours) else colour
        x = i * slot + gap / 2
        bar_h = (val / max_val) * (H - pad_b - pad_t)
        y = H - pad_b - bar_h
        rects.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" '
            f'height="{bar_h:.1f}" fill="{bar_colour}" rx="2"/>'
        )
        if val:
            rects.append(
                f'<text x="{x + bar_w / 2:.1f}" y="{y - 4:.1f}" '
                f'text-anchor="middle" font-size="11" fill="currentColor">{val}</text>'
            )
        labels.append(
            f'<text x="{x + bar_w / 2:.1f}" y="{H - 8}" '
            f'text-anchor="middle" font-size="11" fill="currentColor">{label}</text>'
        )

    return (
        f'<svg viewBox="0 0 {W} {H}" style="width:100%;opacity:0.9">'
        + "".join(rects)
        + "".join(labels)
        + "</svg>"
    )


def load_photos(
    photos_path: pathlib.Path = pathlib.Path("./assets/photos/"),
) -> list[dict[str, str]]:
    """Return yearly photos sorted newest-first.

    Expects files named YYYY.ext (e.g. 2025.jpeg) in assets/photos/.
    """
    if not photos_path.exists():
        return []
    photos = [
        {"year": p.stem, "url": f"/assets/photos/{p.name}"}
        for p in photos_path.iterdir()
        if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp") and p.stem.isdigit()
    ]
    return sorted(photos, key=lambda x: x["year"], reverse=True)


def pub_counts_for(people: list[Post], all_pubs: list[Post]) -> list[int]:
    """Number of shared publications for each person in *people*."""
    return [
        sum(1 for pub in all_pubs if p.get("title", "") in pub.get("authors", [])) for p in people
    ]


def _markdown_to_html(text: str) -> str:
    return md_module.markdown(
        text,
        extensions=["extra", "toc", "pymdownx.arithmatex"],
        extension_configs={"pymdownx.arithmatex": {"generic": True}},
    )


def read_post(path: pathlib.Path) -> Post:
    """Load a markdown source file and return a Post dict."""
    post = frontmatter.load(path)
    data: Post = dict(post.metadata)
    data["slug"] = path.stem
    data["content_html"] = _markdown_to_html(post.content)
    m = re.search(r"<p>(.*?)</p>", data["content_html"], re.DOTALL)
    data["excerpt"] = f"<p>{m.group(1)}</p>" if m else ""
    return data


def _notebook_output_to_html(output: Any) -> str:
    output_type = output.get("output_type", "")
    if output_type == "stream":
        text = html.escape("".join(output.get("text", [])))
        return f'<pre class="nb-output">{text}</pre>'
    if output_type in ("execute_result", "display_data"):
        data = output.get("data", {})
        if "text/html" in data:
            return f'<div class="nb-output nb-html">{"".join(data["text/html"])}</div>'
        if "image/png" in data:
            b64 = data["image/png"].strip()
            return f'<img class="nb-image" src="data:image/png;base64,{b64}" alt="plot"/>'
        if "text/plain" in data:
            text = html.escape("".join(data["text/plain"]))
            return f'<pre class="nb-output">{text}</pre>'
    if output_type == "error":
        ename = html.escape(output.get("ename", "Error"))
        evalue = html.escape(output.get("evalue", ""))
        return f'<pre class="nb-error">{ename}: {evalue}</pre>'
    return ""


def read_notebook(path: pathlib.Path) -> Post:
    """Load a .ipynb file and return a Post dict.

    Frontmatter is read from the first raw cell if it starts with ``---``.
    """
    with open(path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    cells = nb.cells
    data: Post = {}

    if cells and cells[0].cell_type == "raw":
        parsed = frontmatter.loads(cells[0].source)
        if parsed.metadata:
            data = dict(parsed.metadata)
            cells = cells[1:]

    parts: list[str] = []
    for cell in cells:
        if cell.cell_type == "markdown":
            parts.append(_markdown_to_html(cell.source))
        elif cell.cell_type == "code" and cell.source.strip():
            escaped = html.escape(cell.source)
            outputs = "".join(_notebook_output_to_html(o) for o in cell.get("outputs", []))
            parts.append(
                f'<div class="nb-cell">'
                f'<pre class="nb-input"><code>{escaped}</code></pre>'
                f"{outputs}"
                f"</div>"
            )

    content_html = "\n".join(parts)
    data["slug"] = path.stem
    data["content_html"] = content_html
    m = re.search(r"<p>(.*?)</p>", content_html, re.DOTALL)
    data["excerpt"] = f"<p>{m.group(1)}</p>" if m else ""
    return data


def parse_cv_sections(
    src_path: pathlib.Path = pathlib.Path("./src/cv.md"),
) -> dict[str, list[str]]:
    """Parse src/cv.md into a dict mapping section name → list of bullet strings."""
    if not src_path.exists():
        return {}

    text = frontmatter.load(src_path).content
    sections: dict[str, list[str]] = {}
    current_section: str | None = None
    current_items: list[str] = []

    for line in text.splitlines():
        heading = re.match(r"^## (.+)$", line)
        if heading:
            if current_section is not None:
                sections[current_section] = current_items
            current_section = heading.group(1).strip().lower()
            current_items = []
        elif line.startswith("- ") and current_section is not None:
            current_items.append(line[2:].strip())

    if current_section is not None:
        sections[current_section] = current_items

    return sections


def build_publication_stats(posts: list[Post]) -> dict[str, Any]:
    all_pubs = [p for p in posts if any(t in p.get("tags", []) for t in ("article", "book"))]

    year_counts: collections.Counter[int] = collections.Counter()
    total_coauthors = 0
    for p in all_pubs:
        year = p.get("published_date")
        if year:
            year_counts[int(str(year))] += 1
        total_coauthors += sum(1 for a in p.get("authors", []) if a != BLOG_TITLE)

    n = len(all_pubs)
    years = sorted(year_counts)
    return {
        "n_publications": n,
        "pub_by_year_svg": bar_chart_svg([(str(y), c) for y, c in sorted(year_counts.items())]),
        "avg_coauthors_per_paper": round(total_coauthors / n, 1) if n else 0.0,
        "years_publishing": (years[-1] - years[0] + 1) if len(years) >= 2 else (1 if years else 0),
    }


def build_student_stats(posts: list[Post]) -> dict[str, Any]:
    all_pubs = [p for p in posts if any(t in p.get("tags", []) for t in ("article", "book"))]
    students = [p for p in posts if "student" in p.get("tags", [])]

    degree_counts: collections.Counter[str] = collections.Counter()
    year_degree: dict[int, dict[str, int]] = {}
    for p in students:
        year_raw = p.get("year")
        year = int(str(year_raw)) if year_raw else None
        for tag in p.get("tags", []):
            if tag == "student":
                continue
            degree = DEGREE_NORMALISE.get(tag.lower(), tag)
            degree_counts[degree] += 1
            if year is not None:
                year_degree.setdefault(year, {})
                year_degree[year][degree] = year_degree[year].get(degree, 0) + 1

    student_pub_counts = pub_counts_for(students, all_pubs)
    colour_map = dict(_DEGREE_COLOURS)
    present_degrees = [d for d, _ in _DEGREE_COLOURS if degree_counts.get(d, 0) > 0]
    degree_chart_data = sorted(degree_counts.items(), key=lambda x: -x[1])

    return {
        "n_students": len(students),
        "degree_chart_svg": bar_chart_svg(
            degree_chart_data,
            colours=[colour_map[d] for d, _ in degree_chart_data],
        ),
        "students_by_year_svg": stacked_bar_chart_svg(
            year_degree, present_degrees, [colour_map[d] for d in present_degrees]
        ),
        "degree_counts": degree_chart_data,
        "avg_student_pubs": (
            round(sum(student_pub_counts) / len(student_pub_counts), 1)
            if student_pub_counts
            else 0.0
        ),
        "students_with_pubs": sum(1 for c in student_pub_counts if c > 0),
    }


def _coauthor_graph(posts: list[Post]) -> nx.Graph:
    """Co-authorship graph: nodes are collaborators, edges are shared papers."""
    all_pubs = [p for p in posts if any(t in p.get("tags", []) for t in ("article", "book"))]

    G = nx.Graph()
    for pub in all_pubs:
        authors = [a for a in pub.get("authors", []) if a != BLOG_TITLE]
        for i, a1 in enumerate(authors):
            G.add_node(a1)
            for a2 in authors[i + 1 :]:
                if G.has_edge(a1, a2):
                    G[a1][a2]["weight"] += 1
                else:
                    G.add_edge(a1, a2, weight=1)

    return G


def _spring_layout(G: nx.Graph, seed: int = 42) -> dict[str, tuple[float, float]]:
    n = G.number_of_nodes()
    k = 1.0 / (n**0.1) if n > 1 else 1.0
    raw: dict[str, np.ndarray] = nx.spring_layout(
        G, k=k, iterations=120, seed=seed, weight="weight"
    )
    return {node: (float(xy[0]), float(xy[1])) for node, xy in raw.items()}


def network_svg(G: nx.Graph, label_top: int = 10) -> str:
    """Render the co-authorship graph as an inline SVG.

    The top *label_top* nodes by degree are labelled; all nodes have a tooltip.
    """
    if G.number_of_nodes() == 0:
        return ""

    W, H, pad = 600, 380, 28
    pos = _spring_layout(G)

    coords = np.array(list(pos.values()))
    x0, x1 = coords[:, 0].min(), coords[:, 0].max()
    y0, y1 = coords[:, 1].min(), coords[:, 1].max()
    dx, dy = (x1 - x0) or 1.0, (y1 - y0) or 1.0

    def scale(x: float, y: float) -> tuple[float, float]:
        return pad + (x - x0) / dx * (W - 2 * pad), pad + (y - y0) / dy * (H - 2 * pad)

    degrees = dict(G.degree())
    max_deg = max(degrees.values()) if degrees else 1
    top_nodes = {name for name, _ in sorted(degrees.items(), key=lambda kv: -kv[1])[:label_top]}

    parts: list[str] = [f'<svg viewBox="0 0 {W} {H}" style="width:100%;opacity:0.9">']

    for u, v, data in G.edges(data=True):
        x1e, y1e = scale(*pos[u])
        x2e, y2e = scale(*pos[v])
        w = data.get("weight", 1)
        opacity = min(0.25 + 0.15 * w, 0.6)
        parts.append(
            f'<line x1="{x1e:.1f}" y1="{y1e:.1f}" x2="{x2e:.1f}" y2="{y2e:.1f}" '
            f'stroke="var(--text-muted)" stroke-width="{0.5 + 0.5 * w:.1f}"'
            f' opacity="{opacity:.2f}"/>'
        )

    for node in G.nodes():
        cx, cy = scale(*pos[node])
        deg = degrees[node]
        r = 3 + 7 * deg / max_deg
        parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'fill="var(--accent)" opacity="0.75">'
            f"<title>{node} ({deg} co-author connection{'s' if deg != 1 else ''})</title>"
            f"</circle>"
        )

    for node in top_nodes:
        cx, cy = scale(*pos[node])
        deg = degrees[node]
        r = 3 + 7 * deg / max_deg
        label = node.split()[-1] if len(node) > 12 else node
        parts.append(
            f'<text x="{cx:.1f}" y="{cy - r - 2:.1f}" '
            f'text-anchor="middle" font-size="9" fill="var(--text-muted)">{label}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def build_network_stats(posts: list[Post]) -> dict[str, Any]:
    G = _coauthor_graph(posts)

    if G.number_of_nodes() == 0:
        return {"network_svg": "", "net_nodes": 0, "net_edges": 0}

    components = list(nx.connected_components(G))
    degrees = sorted(G.degree(), key=lambda kv: -kv[1])

    return {
        "network_svg": network_svg(G),
        "net_nodes": G.number_of_nodes(),
        "net_edges": G.number_of_edges(),
        "net_density": f"{nx.density(G):.1%}",
        "net_components": len(components),
        "net_top": [(name, deg) for name, deg in degrees[:5]],
    }


def make_html_env() -> jinja2.Environment:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"), autoescape=False)
    env.filters["slugify"] = slugify
    return env


def make_latex_env() -> jinja2.Environment:
    """Jinja2 environment for LaTeX/text templates.

    Uses alternate delimiters to avoid clashing with LaTeX braces.
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates/"),
        block_start_string="(%",
        block_end_string="%)",
        variable_start_string="((",
        variable_end_string="))",
        comment_start_string="(#",
        comment_end_string="#)",
        autoescape=False,
    )
    env.filters["latex_escape"] = latex_escape
    env.filters["striptags"] = lambda s: re.sub(r"<[^>]+>", "", str(s))
    env.filters["regex_replace"] = lambda s, pat, repl: re.sub(pat, repl, str(s))
    return env


def write_post(post: Post, output_dir: pathlib.Path, env: jinja2.Environment) -> None:
    post_dir = output_dir / post["slug"]
    post_dir.mkdir(exist_ok=True, parents=True)
    page = env.get_template("post.html").render(
        post=post, publications=[], root=ROOT, blog_title=BLOG_TITLE
    )
    (post_dir / "index.html").write_text(page)


def write_collaborator(
    post: Post,
    collaborators_dir: pathlib.Path,
    all_posts: list[Post],
    env: jinja2.Environment,
) -> None:
    name = post.get("title", "")
    publications = [
        p
        for p in all_posts
        if any(t in p.get("tags", []) for t in ("article", "book")) and name in p.get("authors", [])
    ]
    collab_dir = collaborators_dir / post["slug"]
    collab_dir.mkdir(exist_ok=True, parents=True)
    page = env.get_template("post.html").render(
        post=post, publications=publications, root=ROOT, blog_title=BLOG_TITLE
    )
    (collab_dir / "index.html").write_text(page)


def _current_title_from_appointments(appointments: list[str]) -> str:
    for appt in appointments:
        if "present" in appt:
            m = re.match(r"[\d\-]+.*?:\s*(.+?)\s*[-\u2013]", appt)
            if m:
                return re.sub(r"[^\x00-\x7F]", "", m.group(1)).strip()
    return "Professor"


def _featured_book(books: list[Post]) -> Post | None:
    """Prefer a book with a named publisher over one released online only."""
    for book in books:
        details = book.get("details", "") or ""
        if details and "online" not in details.lower():
            return book
    return books[0] if books else None


def build_cv(posts: list[Post]) -> None:
    """Render LaTeX CV, short CV, and bio into assets/cv/."""
    cv_dir = pathlib.Path("./assets/cv/")
    cv_dir.mkdir(exist_ok=True, parents=True)

    cv_sections = parse_cv_sections()
    appointments = cv_sections.get("appointments", [])

    def by_date(tag: str, key: str = "published_date") -> list[Post]:
        return sorted(
            [p for p in posts if tag in p.get("tags", [])],
            key=lambda p: str(p.get(key, "")),
            reverse=True,
        )

    books = by_date("book")
    context = {
        "appointments": appointments,
        "awards": cv_sections.get("awards", []),
        "qualifications": cv_sections.get("qualifications", []),
        "examiner": cv_sections.get("examiner", []),
        "roles": cv_sections.get("roles", []),
        "funding": cv_sections.get("funding", []),
        "research_interests": RESEARCH_INTERESTS,
        "articles": by_date("article"),
        "books": books,
        "featured_book": _featured_book(books),
        "software_list": [p for p in posts if "software" in p.get("tags", [])],
        "students": by_date("student", key="year"),
        "current_title": _current_title_from_appointments(appointments),
    }

    latex_env = make_latex_env()
    for name in ("cv.tex", "cv-short.tex", "bio.txt"):
        (cv_dir / name).write_text(latex_env.get_template(name).render(**context), encoding="utf-8")


def main(
    src_path: pathlib.Path = pathlib.Path("./src/"),
    output_dir: pathlib.Path = pathlib.Path("./posts/"),
) -> None:
    output_dir.mkdir(exist_ok=True)
    collaborators_dir = output_dir.parent / "collaborators"
    collaborators_dir.mkdir(exist_ok=True)

    env = make_html_env()

    src_files = sorted(src_path.glob("**/*.md")) + sorted(src_path.glob("**/*.ipynb"))
    posts = [read_notebook(p) if p.suffix == ".ipynb" else read_post(p) for p in src_files]

    students = sorted(
        [p for p in posts if "student" in p.get("tags", [])],
        key=lambda p: str(p.get("year", "")),
        reverse=True,
    )

    student_stats = build_student_stats(posts)
    pub_stats = build_publication_stats(posts)
    photos = load_photos()
    latest_photo_url = photos[0]["url"] if photos else "/assets/vince-knight-lo.png"

    for post in posts:
        tags = post.get("tags", [])
        if "page" in tags:
            page_dir = output_dir.parent / post["slug"]
            page_dir.mkdir(exist_ok=True, parents=True)
            page = env.get_template("post.html").render(
                post=post,
                publications=[],
                students=students,
                root=ROOT,
                blog_title=BLOG_TITLE,
                photos=photos,
                **student_stats,
                **pub_stats,
            )
            (page_dir / "index.html").write_text(page)
        elif "collaborator" in tags or "student" in tags:
            write_collaborator(post, collaborators_dir, posts, env)
        else:
            write_post(post, output_dir, env)

    blog_posts = sorted(
        [p for p in posts if "post" in p.get("tags", [])],
        key=lambda p: str(p.get("date", "")),
        reverse=True,
    )
    courses = [p for p in posts if "course" in p.get("tags", [])]
    software_list = [p for p in posts if "software" in p.get("tags", [])]
    publications = sorted(
        [p for p in posts if any(t in p.get("tags", []) for t in ("article", "book"))],
        key=lambda p: str(p.get("published_date", "")),
        reverse=True,
    )

    # Map author name → slug for those with a dedicated /collaborators/ page
    author_to_slug = {
        p.get("title", ""): p["slug"]
        for p in posts
        if any(t in p.get("tags", []) for t in ("collaborator", "student"))
        and p.get("title", "") != BLOG_TITLE
    }

    author_pub_counts: collections.Counter[str] = collections.Counter()
    for pub in publications:
        for author in pub.get("authors", []):
            if author != BLOG_TITLE:
                author_pub_counts[author] += 1

    collaborator_index = sorted(
        [
            {"title": name, "slug": author_to_slug.get(name), "pub_count": count}
            for name, count in author_pub_counts.items()
        ],
        key=lambda p: (-p["pub_count"], p["title"].lower()),
    )

    (collaborators_dir / "index.html").write_text(
        env.get_template("collaborators.html").render(
            blog_title=BLOG_TITLE,
            collaborators=collaborator_index,
            root=ROOT,
            **pub_stats,
            **build_network_stats(posts),
        )
    )

    (output_dir.parent / "index.html").write_text(
        env.get_template("home.html").render(
            blog_title=BLOG_TITLE,
            blog_posts=blog_posts,
            courses=courses,
            software_list=software_list,
            publications=publications,
            root=ROOT,
            description=DESCRIPTION,
            latest_photo_url=latest_photo_url,
        )
    )

    (output_dir / "index.html").write_text(
        env.get_template("posts.html").render(
            blog_title=BLOG_TITLE, blog_posts=blog_posts, root=ROOT
        )
    )

    build_cv(posts)


if __name__ == "__main__":
    main()
