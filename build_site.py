from __future__ import annotations

import csv
import json
import tomllib
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

ROOT = Path(__file__).parent
DATA = ROOT / "data"
ARTICLES_CSV = ROOT / "articles.csv"

# All copy lives in copy.toml; this script holds structure and layout only.
COPY = tomllib.loads((ROOT / "copy.toml").read_text(encoding="utf-8"))
SHARED = COPY["shared"]

SITE_URL = "https://raphaelhernandes.com"
SITE_NAME = "Raphael Hernandes"
CONTACT_EMAIL = "hello@raphaelhernandes.com"
ENQUIRY_MAILTO = (
    f"mailto:{CONTACT_EMAIL}?subject={quote(SHARED['enquiries']['mail_subject'], safe='')}"
)
PORTRAIT_DISPLAY = "static/img/rh-640.jpg"
PORTRAIT_FULL = "static/img/rh.jpg"
SPEAKING_PHOTO = "static/img/rh-speaking.jpg"

SOCIAL_LINKS = [
    ("LinkedIn", "https://www.linkedin.com/in/raphaelhernandes/",
     "fa-brands fa-linkedin-in"),
    ("Bluesky", "https://bsky.app/profile/hernandesraph.bsky.social",
     "fa-brands fa-bluesky"),
    ("GitHub", "https://github.com/rhhernandes", "fa-brands fa-github"),
    ("Instagram", "https://www.instagram.com/hernandesraph/", "fa-brands fa-instagram"),
    ("Google Scholar", "https://scholar.google.com/citations?user=arCHs-gAAAAJ&hl=en",
     "fa-solid fa-graduation-cap"),
    ("Cambridge Digital Humanities", "https://www.cdh.cam.ac.uk/about/people/raphael-hernandes/",
     "fa-solid fa-building-columns"),
]

GOOGLE_SCHOLAR_URL = "https://scholar.google.com/citations?user=arCHs-gAAAAJ&hl=en"

# Profiles that belong in the Person schema's sameAs (they help search engines
# tie these identities to one person) but are NOT footer icons.
PROFILE_URLS = [
    "https://orcid.org/0009-0005-0323-8326",
    "https://www.theguardian.com/profile/raphael-hernandes",
    "https://www1.folha.uol.com.br/autores/raphael-hernandes.shtml",
    "https://www.lcfi.ac.uk/people/raphael-hernandes-2",
    "https://www.hardingscholars.fund.cam.ac.uk/raphael-hernandes-2025-cohort",
]

SCROLL_REVEAL_SCRIPT = """
    <script>
    (function() {
        var elements = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
        if (!elements.length) { return; }

        function revealAll() {
            elements.forEach(function(el) { el.classList.add('is-visible'); });
        }

        var reduceMotionQuery = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;

        if (!('IntersectionObserver' in window)) {
            revealAll();
            return;
        }

        if (reduceMotionQuery && reduceMotionQuery.matches) {
            revealAll();
            return;
        }

        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting || entry.intersectionRatio > 0) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.2,
            rootMargin: '0px 0px -10% 0px'
        });

        elements.forEach(function(el) { observer.observe(el); });

        if (reduceMotionQuery) {
            reduceMotionQuery.addEventListener('change', function(event) {
                if (event.matches) {
                    observer.disconnect();
                    revealAll();
                }
            });
        }
    })();
    </script>
"""


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def sanitize(value: str) -> str:
    cleaned = value.strip()
    replacements = {
        "”": '"',
        "“": '"',
        "’": "'",
    }
    for source, target in replacements.items():
        cleaned = cleaned.replace(source, target)
    cleaned = cleaned.replace('target="_blank>', 'target="_blank">')
    return cleaned


def load_articles() -> list[dict[str, object]]:
    articles: list[dict[str, object]] = []
    with ARTICLES_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                when = datetime.strptime(row["Date"], "%Y-%m-%d %H:%M:%S")
            except ValueError as exc:  # rare legacy rows
                raise ValueError(
                    f"Invalid date format for '{row['Article title in English']}': {row['Date']}") from exc
            articles.append(
                {
                    "title": sanitize(row["Article title in English"]),
                    "publication": sanitize(row["Where it was published"]),
                    "description": sanitize(row["Article Description in English"]),
                    "photo": sanitize(row["Photo"]),
                    "url": sanitize(row["Article URL"]),
                    "date": when,
                    "highlight": str(row["Highlight"]).strip().lower() == "true",
                    "category": sanitize(row["Category"]).lower(),
                    "show": str(row.get("Show", "true")).strip().lower() == "true",
                }
            )
    return articles


def load_json(filename: str, default: object) -> object:
    path = DATA / filename
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def format_date(value: datetime) -> str:
    return value.strftime("%b %d, %Y")


# ---------------------------------------------------------------------------
# Navigation / layout
# ---------------------------------------------------------------------------

def nav_items() -> list[tuple[str, str]]:
    items = [(item["label"], item["href"]) for item in SHARED["header"]["nav"]]
    teaching = load_json("teaching.json", {"show_in_nav": False, "entries": []})
    if teaching.get("show_in_nav") or teaching.get("entries"):
        extra = SHARED["header"]["teaching_nav"]
        items.append((extra["label"], extra["href"]))
    return items


def render_nav(current: str) -> str:
    links = []
    for label, href in nav_items():
        state = " aria-current=\"page\"" if href == current else ""
        links.append(f'<a href="{href}"{state}>{label}</a>')
    links.append(f'<a class="nav-cta" href="#enquiries">{SHARED["header"]["nav_cta"]}</a>')
    return "".join(links)


def enquiries_band() -> str:
    """Shared enquiries CTA; copy in copy.toml under [shared.enquiries]."""
    c = SHARED["enquiries"]
    return f"""<section class="cta-band" id="enquiries">
    <div class="container narrow">
        <p class="kicker kicker--light">{c["kicker"]}</p>
        <h2>{c["heading"]}</h2>
        <p>{c["body"]}</p>
        <p class="cta-actions"><a class="button button--light" href="{ENQUIRY_MAILTO}">{c["button"].format(email=CONTACT_EMAIL)}</a></p>
        <p class="cta-alt">{c["alt_html"]}</p>
    </div>
</section>
"""


def malton_band() -> str:
    """Decorative line drawing that sits above the enquiries band on the home page.

    Traced from Thomas Malton's 1799 aquatint of King's College, the Chapel and
    Clare Hall (Yale Center for British Art, public domain). Purely decorative,
    so it carries an empty alt and is hidden from assistive technology; the
    styling, including how far it rises behind the index list, lives in
    style.css under "Malton band".
    """
    return """<div class="malton-foot" aria-hidden="true">
            <div class="malton-foot-art">
                <img src="static/img/kings-college-line.svg" alt="" width="1200" height="446"
                     loading="lazy" decoding="async" />
            </div>
        </div>
        """


def render_social_links(extra_class: str = "") -> str:
    classes = " ".join([cls for cls in ("social-links", extra_class) if cls])
    items = []
    for label, url, icon_class in SOCIAL_LINKS:
        items.append(
            """
            <li>
                <a class="social-link" href="{url}" target="_blank" rel="noopener" aria-label="{label}">
                    <i class="{icon_class}" aria-hidden="true"></i>
                    <span class="sr-only">{label}</span>
                </a>
            </li>
            """.format(label=label, url=url, icon_class=icon_class)
        )
    return f'<ul class="{classes}">{"".join(items)}</ul>'


def person_schema_html(extra_nodes: list[dict] | None = None) -> str:
    """Person structured data, stamped into every page.

    The stable @id lets crawlers merge the copies into a single entity instead
    of reading them as several different people.
    """
    schema_copy = COPY["index"]["schema"]
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": f"{SITE_URL}/#person",
        "name": SITE_NAME,
        "url": f"{SITE_URL}/",
        "image": f"{SITE_URL}/{PORTRAIT_FULL}",
        "description": schema_copy["description"],
        "jobTitle": schema_copy["job_titles"],
        "knowsAbout": [
            {"@type": "Thing", "name": topic["name"], "sameAs": topic["wikipedia"]}
            if topic.get("wikipedia") else topic["name"]
            for topic in schema_copy["knows_about"]
        ],
        "worksFor": {"@type": "CollegeOrUniversity", "name": schema_copy["works_for"]},
        "affiliation": {
            "@type": "CollegeOrUniversity",
            "name": schema_copy["affiliation"],
            "department": schema_copy["affiliation_department"],
        },
        "alumniOf": {"@type": "CollegeOrUniversity", "name": schema_copy["alumni_of"]},
        "award": schema_copy["awards"],
        "email": f"mailto:{CONTACT_EMAIL}",
        "sameAs": [url for _, url, _ in SOCIAL_LINKS] + PROFILE_URLS,
    }
    nodes = [person] + (extra_nodes or [])
    return "".join(
        '<script type="application/ld+json">' + json.dumps(node, ensure_ascii=False) + "</script>"
        for node in nodes
    )


def render_layout(
    *,
    page_title: str,
    description: str,
    canonical_path: str,
    current: str,
    main: str,
    body_class: str = "",
    pre_enquiries: str = "",
    extra_head: str = "",
    noindex: bool = False,
    schema: bool = True,
    schema_nodes: list[dict] | None = None,
) -> str:
    body_attr = f' class="{body_class.strip()}"' if body_class.strip() else ""
    canonical = f"{SITE_URL}/{canonical_path}" if canonical_path else f"{SITE_URL}/"
    footer_copy = SHARED["footer"]["copyright"].format(year=f"{datetime.now():%Y}")
    robots_meta = '\n    <meta name="robots" content="noindex, follow" />' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="{description}" />{robots_meta}
    <title>{page_title}</title>
    <link rel="canonical" href="{canonical}" />
    <link rel="icon" href="favicon.ico" sizes="any" />
    <meta property="og:site_name" content="{SITE_NAME}" />
    <meta property="og:title" content="{page_title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{SITE_URL}/{PORTRAIT_FULL}" />
    <meta name="twitter:card" content="summary" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="assets/css/style.css" />
    <script src="https://kit.fontawesome.com/c796ba7827.js" crossorigin="anonymous"></script>
    {person_schema_html(schema_nodes) if schema else ""}{extra_head}
</head>
<body{body_attr}>
    <a class="skip-link" href="#main">{SHARED["header"]["skip_link"]}</a>
    <header class="site-header">
        <div class="container header-inner">
            <a class="brand" href="index.html">{SHARED["header"]["brand"]}</a>
            <nav class="site-nav" aria-label="Primary">{render_nav(current)}</nav>
        </div>
    </header>
    <main id="main">
        {main}
        {pre_enquiries}{enquiries_band()}
    </main>
    <footer class="site-footer">
        <div class="container">
            {render_social_links('social-links-footer')}
            <p class="footer-copy">{footer_copy}</p>
        </div>
    </footer>
    {SCROLL_REVEAL_SCRIPT}
</body>
</html>"""


# ---------------------------------------------------------------------------
# Shared components
# ---------------------------------------------------------------------------

def page_header(kicker: str, title: str, intro_paragraphs: list[str] | None = None) -> str:
    intro = ""
    if intro_paragraphs:
        intro_html = "\n    " + "\n    ".join(f"<p>{p}</p>" for p in intro_paragraphs) + "\n    "
        intro = f'<div class="page-intro">{intro_html}</div>'
    return f"""
    <section class="section page-title">
        <div class="container narrow">
            <p class="kicker">{kicker}</p>
            <h1>{title}</h1>
            {intro}
        </div>
    </section>
    """


def render_feature_cards(items: Iterable[dict[str, object]]) -> str:
    cards: list[str] = []
    labels = SHARED["cards"]
    for article in items:
        cards.append(
            """
            <article class="feature-card" data-reveal>
                <div class="feature-media">
                    <img src="{photo}" alt="{alt}" loading="lazy" />
                </div>
                <div class="feature-content">
                    <p class="feature-meta">{date} · {publication}</p>
                    <h3><a href="{url}" target="_blank" rel="noopener">{title}</a></h3>
                    <p>{description}</p>
                    <a class="feature-link" href="{url}" target="_blank" rel="noopener">{read_more}<span aria-hidden="true"> →</span></a>
                </div>
            </article>
            """.format(
                photo=article["photo"],
                alt=labels["illustration_alt"].format(title=article["title"]),
                title=article["title"],
                publication=article["publication"],
                description=article["description"],
                url=article["url"],
                date=format_date(article["date"]),
                read_more=labels["read_more"],
            )
        )
    return "".join(cards)


def render_article_list(items: Iterable[dict[str, object]]) -> str:
    entries: list[str] = []
    for article in items:
        entries.append(
            """
            <li class="article-item" data-reveal>
                <div class="article-meta">
                    <span>{date}</span>
                    <span>{publication}</span>
                </div>
                <a class="article-title" href="{url}" target="_blank" rel="noopener">{title}</a>
                <p>{description}</p>
            </li>
            """.format(
                date=format_date(article["date"]),
                publication=article["publication"],
                url=article["url"],
                title=article["title"],
                description=article["description"],
            )
        )
    return "".join(entries)


def render_entry(*, title: str, url: str = "", meta: str = "", desc: str = "") -> str:
    if url:
        heading = f'<a class="entry-title" href="{url}" target="_blank" rel="noopener">{title}</a>'
    else:
        heading = f'<span class="entry-title">{title}</span>'
    meta_html = f'<p class="entry-meta">{meta}</p>' if meta else ""
    desc_html = f'<p class="entry-desc">{desc}</p>' if desc else ""
    return f'<li class="entry" data-reveal>{meta_html}{heading}{desc_html}</li>'


def render_topics(topics: list[dict[str, str]]) -> str:
    return "".join(
        f"""
                <div class="topic" data-reveal>
                    <h3>{t["title"]}</h3>
                    <p>{t["desc"]}</p>
                </div>"""
        for t in topics
    )


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def build_home() -> None:
    c = COPY["index"]
    hero_copy = c["hero"]
    hero = f"""
    <section class="hero">
        <div class="container hero-grid">
            <div class="hero-copy">
                <p class="kicker">{hero_copy["kicker"]}</p>
                <h1>{hero_copy["heading"]}</h1>
                <p class="lede">{hero_copy["lede"]}</p>
                <p class="hero-summary">{hero_copy["summary"]}</p>
                <div class="hero-actions">
                    <a class="button" href="#enquiries">{hero_copy["button"]}</a>
                    <a class="text-link" href="about.html">{hero_copy["text_link"]}<span aria-hidden="true"> →</span></a>
                </div>
            </div>
            <div class="hero-media">
                <img src="{PORTRAIT_FULL}" alt="{SHARED["cards"]["portrait_alt"]}" width="640" height="640" fetchpriority="high" />
            </div>
        </div>
    </section>
    """

    cred_items = "".join(
        f"""
                <li>
                    <p class="cred-label">{item["label"]}</p>
                    <p class="cred-detail">{item["detail"]}</p>
                </li>"""
        for item in c["credentials"]["items"]
    )
    credentials = f"""
    <section class="cred-section" aria-label="{c["credentials"]["aria_label"]}">
        <div class="container">
            <ul class="cred-strip">{cred_items}
            </ul>
        </div>
    </section>
    """

    index_html = "".join(
        f"""
        <li data-reveal>
            <a class="index-row" href="{row["href"]}">
                <span class="index-title">{row["title"]}<span class="index-arrow" aria-hidden="true"> →</span></span>
                <span class="index-desc">{row["desc"]}</span>
            </a>
        </li>
        """
        for row in c["explore"]["rows"]
    )
    section_index = f"""
    <section class="section">
        <div class="container">
            <h2 class="sr-only">{c["explore"]["heading_sr"]}</h2>
            <ul class="index-list">{index_html}</ul>
        </div>
    </section>
    """

    html = render_layout(
        page_title=c["meta"]["title"],
        description=c["meta"]["description"],
        canonical_path="",
        current="index.html",
        main=hero + credentials + section_index,
        body_class="page-home",
        pre_enquiries=malton_band(),
    )
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def build_about() -> None:
    c = COPY["about"]
    paragraphs = c["body"]["paragraphs"]
    # Portrait sits between the first and second paragraphs; on wide screens
    # it floats right and the following text wraps around it (see .about-media).
    first = f"<p data-reveal>{paragraphs[0]}</p>"
    rest = "".join(f"<p data-reveal>{p}</p>" for p in paragraphs[1:])
    figure = f"""<figure class="about-media" data-reveal>
                    <img src="{PORTRAIT_DISPLAY}" alt="{SHARED["cards"]["portrait_alt"]}" loading="lazy" />
                    <figcaption class="img-credit">{c["body"]["photo_credit"]}</figcaption>
                </figure>"""
    # Optional: set pull_quote in copy.toml to show a pull quote after the body.
    # Omit the key (or leave it empty) and nothing is rendered.
    quote = c["body"].get("pull_quote", "").strip()
    quote_html = (
        f'\n                <blockquote class="pull-quote" data-reveal>{quote}</blockquote>'
        if quote
        else ""
    )
    content = page_header(c["header"]["kicker"], c["header"]["title"]) + f"""
    <section class="section about-section">
        <div class="container narrow">
            <div class="about-body">
                {first}
                {figure}
                {rest}{quote_html}
            </div>
        </div>
    </section>
    """

    html = render_layout(
        page_title=c["meta"]["title"],
        description=c["meta"]["description"],
        canonical_path="about.html",
        current="about.html",
        main=content,
        # About is the canonical profile page for the Person node.
        schema_nodes=[{
            "@context": "https://schema.org",
            "@type": "ProfilePage",
            "@id": f"{SITE_URL}/about.html#profilepage",
            "url": f"{SITE_URL}/about.html",
            "mainEntity": {"@id": f"{SITE_URL}/#person"},
        }],
    )
    (ROOT / "about.html").write_text(html, encoding="utf-8")


def build_research() -> None:
    c = COPY["research"]
    articles = [a for a in load_articles() if a["category"] == "academic" and a["show"]]
    articles.sort(key=lambda item: item["date"], reverse=True)
    publications = "".join(
        render_entry(
            title=str(a["title"]),
            url=str(a["url"]),
            meta=f"{a['date']:%b %Y} · {a['publication']}",
            desc=str(a["description"]),
        )
        for a in articles
    )

    themes = f"""
    <section class="section">
        <div class="container">
            <p class="kicker">{c["themes"]["kicker"]}</p>
            <h2>{c["themes"]["heading"]}</h2>
            <div class="topic-grid">{render_topics(c["themes"]["topics"])}
            </div>
        </div>
    </section>
    """

    pubs_section = f"""
    <section class="section">
        <div class="container">
            <p class="kicker">{c["publications"]["kicker"]}</p>
            <h2>{c["publications"]["heading"]}</h2>
            <ul class="entry-list">{publications}</ul>
            <p class="section-footnote"><a class="text-link" href="{GOOGLE_SCHOLAR_URL}" target="_blank" rel="noopener">{c["publications"]["scholar_link"]}<span aria-hidden="true"> →</span></a></p>
        </div>
    </section>
    """

    content = page_header(c["header"]["kicker"], c["header"]["title"], c["header"]["intro"]) + themes + pubs_section
    html = render_layout(
        page_title=c["meta"]["title"],
        description=c["meta"]["description"],
        canonical_path="research.html",
        current="research.html",
        main=content,
    )
    (ROOT / "research.html").write_text(html, encoding="utf-8")


def build_journalism() -> None:
    c = COPY["journalism"]
    articles = [a for a in load_articles() if a["category"] == "journalism" and a["show"]]
    articles.sort(key=lambda item: item["date"], reverse=True)
    highlights = [a for a in articles if a["highlight"]]
    others = [a for a in articles if not a["highlight"]]

    highlight_section = f"""
    <section class="section">
        <div class="container">
            <p class="kicker">{c["highlights"]["kicker"]}</p>
            <h2 class="sr-only">{c["highlights"]["heading_sr"]}</h2>
            <div class="feature-grid">{render_feature_cards(highlights)}</div>
        </div>
    </section>
    """ if highlights else ""

    list_section = f"""
    <section class="section">
        <div class="container">
            <h2>{c["more"]["heading"]}</h2>
            <ul class="article-list">{render_article_list(others)}</ul>
        </div>
    </section>
    """ if others else ""

    content = page_header(c["header"]["kicker"], c["header"]["title"], c["header"]["intro"]) + highlight_section + list_section
    html = render_layout(
        page_title=c["meta"]["title"],
        description=c["meta"]["description"],
        canonical_path="journalism.html",
        current="journalism.html",
        main=content,
    )
    (ROOT / "journalism.html").write_text(html, encoding="utf-8")


def build_speaking() -> None:
    c = COPY["speaking"]
    talks = load_json("talks.json", [])
    testimonials = load_json("testimonials.json", [])

    # Optional: the section only renders once [[speaking.topics.items]] has
    # entries in copy.toml. Empty list (or no items) and nothing is output.
    topic_items = c["topics"].get("items") or []
    topics = f"""
    <section class="section">
        <div class="container">
            <p class="kicker">{c["topics"]["kicker"]}</p>
            <h2>{c["topics"]["heading"]}</h2>
            <div class="topic-grid">{render_topics(topic_items)}
            </div>
        </div>
    </section>
    """ if topic_items else ""

    format_items = "".join(
        f"""
                <li data-reveal>
                    <p class="cred-label">{item["label"]}</p>
                    <p class="cred-detail">{item["detail"]}</p>
                </li>"""
        for item in c["formats"]["items"]
    )
    formats = f"""
    <section class="section">
        <div class="container">
            <p class="kicker">{c["formats"]["kicker"]}</p>
            <h2>{c["formats"]["heading"]}</h2>
            <ul class="format-grid">{format_items}
            </ul>
        </div>
    </section>
    """

    talk_entries = []
    for talk in talks:
        title = talk.get("title") or talk.get("event") or talk.get("venue", "")
        meta_parts = [talk.get("date", "")]
        if talk.get("title") or talk.get("event"):
            meta_parts.append(talk.get("venue", ""))
        meta_parts.append(talk.get("location", ""))
        talk_entries.append(
            render_entry(
                title=title,
                url=talk.get("url", ""),
                meta=" · ".join(p for p in meta_parts if p),
                desc=talk.get("notes", ""),
            )
        )
    talks_caption = c["talks"].get("image_caption", "")
    talks_figcaption = (
        f'\n                <figcaption class="img-credit">{talks_caption}</figcaption>'
        if talks_caption
        else ""
    )
    # Portrait floated to the right of the entry list: the entries wrap around it
    # and return to full width once the photo ends (see .talks-media in the CSS).
    talks_figure = f"""
            <figure class="talks-media" data-reveal>
                <img src="{SPEAKING_PHOTO}" alt="{c["talks"].get("image_alt", "")}" width="1280" height="1920" loading="lazy" />{talks_figcaption}
            </figure>"""
    talks_section = f"""
    <section class="section">
        <div class="container talks-body">
            <p class="kicker">{c["talks"]["kicker"]}</p>
            <h2>{c["talks"]["heading"]}</h2>{talks_figure}
            <ul class="entry-list entry-list--float">{''.join(talk_entries)}</ul>
        </div>
    </section>
    """ if talk_entries else ""

    testimonial_entries = "".join(
        f"""
        <blockquote class="testimonial" data-reveal>
            <p>{t.get('quote', '')}</p>
            <footer>{t.get('name', '')}{' · ' + t.get('role', '') if t.get('role') else ''}</footer>
        </blockquote>
        """
        for t in testimonials
    )
    # Testimonials render automatically once data/testimonials.json has entries.
    testimonials_section = f"""
    <section class="section">
        <div class="container narrow">
            <p class="kicker">{c["testimonials"]["kicker"]}</p>
            <h2>{c["testimonials"]["heading"]}</h2>
            {testimonial_entries}
        </div>
    </section>
    """ if testimonials else ""

    content = page_header(c["header"]["kicker"], c["header"]["title"], c["header"]["intro"]) + topics + formats + talks_section + testimonials_section
    html = render_layout(
        page_title=c["meta"]["title"],
        description=c["meta"]["description"],
        canonical_path="speaking.html",
        current="speaking.html",
        main=content,
    )
    (ROOT / "speaking.html").write_text(html, encoding="utf-8")


def build_recognition() -> None:
    c = COPY["recognition"]
    awards = load_json("awards.json", [])
    press = load_json("press.json", [])

    press_entries = "".join(
        render_entry(
            title=p.get("title", ""),
            url=p.get("url", ""),
            meta=" · ".join(x for x in [p.get("date", ""), p.get("outlet", "")] if x),
            desc=p.get("note", ""),
        )
        for p in press
    )
    if press_entries:
        press_listing = f'<ul class="entry-list">{press_entries}</ul>'
    else:
        press_listing = f'<div class="empty-state">{c["press"]["empty"]}</div>'
    press_section = f"""
    <section class="section">
        <div class="container">
            <h2>{c["press"]["heading"]}</h2>
            {press_listing}
        </div>
    </section>
    """

    award_entries = "".join(
        render_entry(
            title=a.get("title", ""),
            url=a.get("url", ""),
            meta=" · ".join(p for p in [a.get("year", ""), a.get("org", "")] if p),
            desc=a.get("detail", ""),
        )
        for a in awards
    )
    awards_section = f"""
    <section class="section">
        <div class="container">
            <h2>{c["awards"]["heading"]}</h2>
            <ul class="entry-list">{award_entries}</ul>
        </div>
    </section>
    """ if awards else ""

    content = page_header(c["header"]["kicker"], c["header"]["title"], c["header"]["intro"]) + press_section + awards_section
    html = render_layout(
        page_title=c["meta"]["title"],
        description=c["meta"]["description"],
        canonical_path="recognition.html",
        current="recognition.html",
        main=content,
    )
    (ROOT / "recognition.html").write_text(html, encoding="utf-8")


def build_teaching() -> None:
    c = COPY["teaching"]
    teaching = load_json("teaching.json", {"show_in_nav": False, "entries": []})
    entries = teaching.get("entries", [])

    entry_html = "".join(
        render_entry(
            title=e.get("course", ""),
            url=e.get("url", ""),
            meta=" · ".join(p for p in [e.get("term", ""), e.get("role", ""), e.get("institution", "")] if p),
            desc=e.get("description", ""),
        )
        for e in entries
    )
    if entry_html:
        listing = f'<ul class="entry-list">{entry_html}</ul>'
    else:
        listing = f'<div class="empty-state">{c["list"]["empty"]}</div>'

    content = page_header(c["header"]["kicker"], c["header"]["title"], c["header"]["intro"]) + f"""
    <section class="section">
        <div class="container">
            {listing}
        </div>
    </section>
    """
    html = render_layout(
        page_title=c["meta"]["title"],
        description=c["meta"]["description"],
        canonical_path="teaching.html",
        current="teaching.html",
        main=content,
        # Placeholder until data/teaching.json has entries: keep it out of search
        # results, but let crawlers follow its links.
        noindex=not entries,
    )
    (ROOT / "teaching.html").write_text(html, encoding="utf-8")


def build_academic_redirect() -> None:
    """academic.html moved to research.html; keep the old URL working."""
    c = COPY["academic"]
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>{c["page_title"]}</title>
    <meta http-equiv="refresh" content="0; url=research.html" />
    <link rel="canonical" href="{SITE_URL}/research.html" />
    <meta name="robots" content="noindex" />
</head>
<body>
    <p>{c["moved_html"]}</p>
</body>
</html>"""
    (ROOT / "academic.html").write_text(html, encoding="utf-8")


def build_sitemap_and_robots() -> None:
    """Sitemap of indexable pages, plus a robots.txt pointing at it.

    teaching.html is left out while it is a noindex placeholder, and
    academic.html is a redirect, so neither belongs in the sitemap.
    """
    teaching = load_json("teaching.json", {"show_in_nav": False, "entries": []})
    pages = ["", "about.html", "research.html", "journalism.html",
             "speaking.html", "recognition.html"]
    if teaching.get("entries"):
        pages.append("teaching.html")

    today = f"{datetime.now():%Y-%m-%d}"
    urls = "".join(
        f"""
    <url>
        <loc>{SITE_URL}/{page}</loc>
        <lastmod>{today}</lastmod>
    </url>"""
        for page in pages
    )
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")


def main() -> None:
    build_home()
    build_about()
    build_research()
    build_journalism()
    build_speaking()
    build_recognition()
    build_teaching()
    build_academic_redirect()
    build_sitemap_and_robots()


if __name__ == "__main__":
    main()
