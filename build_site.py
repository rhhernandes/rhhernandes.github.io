from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).parent
ARTICLES_CSV = ROOT / "articles.csv"
OUTPUTS = {
    "home": ROOT / "index.html",
    "academic": ROOT / "academic.html",
    "journalism": ROOT / "journalism.html",
}

NAV_ITEMS = [
    ("Home", "index.html"),
    ("Academic Work", "academic.html"),
    ("Journalism Work", "journalism.html"),
]

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

BIO_TEXT = """I am an artificial intelligence (AI) ethics researcher and data journalist specializing in the intersections between AI, journalism, and society. My work combines in-depth reporting and quantitative analysis to explore the ethical implications and societal impacts of AI technologies.

I am currently pursuing a <a href="https://www.cdh.cam.ac.uk/about/people/raphael-hernandes/" target="_blank" rel="noopener">PhD at Cambridge Digital Humanities</a>, University of Cambridge, where my research examines how AI reshapes journalism, information environments, and epistemic security. My work is supported by a <a href="https://www.hardingscholars.fund.cam.ac.uk/raphael-hernandes-2025-cohort" target="_blank" rel="noopener">Harding Distinguished Postgraduate Scholarship</a>.

My journalism career includes roles as a Data Journalist at <a href="https://www.theguardian.com/profile/raphael-hernandes" target="_blank" rel="noopener">The Guardian</a> (UK) and as Editor-at-Large at <a href="https://www1.folha.uol.com.br/autores/raphael-hernandes.shtml" target="_blank" rel="noopener">Folha de S.Paulo</a> (Brazil), where I led innovative data- and AI-driven newsroom projects and reported on the intersections of technology, media, and society.

I hold an MPhil in Ethics of AI, Data, and Algorithms from Cambridge, graduating with distinction and receiving the <a href="https://www.lcfi.ac.uk/education/mphil/huw-price-prize" target="_blank" rel="noopener">Huw Price Prize</a> for best overall performance.

As a Research Assistant at the Leverhulme Centre for the Future of Intelligence (Cambridge), I analyzed media coverage of AI and examined the use of generative systems in political communication, co-creating a <a href="https://www.desirableai.com/journalism-toolkit" target="_blank" rel="noopener">toolkit to help journalists responsibly adopt AI</a> technologies in their work.

I regularly speak at technology and journalism conferences, engaging diverse audiences to foster a critical understanding of AI's role in society. I am committed to empowering the public through technology, data, and informed discourse on AI ethics and responsible innovation."""

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


def sanitize(value: str) -> str:
    cleaned = value.strip()
    replacements = {
        "”": '"',
        "“": '"',
        "’": "'",
        "–": "-",
        "—": "-",
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
                }
            )
    return articles


def format_date(value: datetime) -> str:
    return value.strftime("%b %d, %Y")


def render_nav(current: str) -> str:
    links = []
    for label, href in NAV_ITEMS:
        state = " aria-current=\"page\"" if href == current else ""
        links.append(f'<a href="{href}"{state}>{label}</a>')
    return "".join(links)


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


def render_feature_cards(items: Iterable[dict[str, object]]) -> str:
    cards: list[str] = []
    for article in items:
        cards.append(
            """
            <article class="feature-card" data-reveal>
                <div class="feature-media">
                    <img src="{photo}" alt="Illustration for {title}" loading="lazy" />
                </div>
                <div class="feature-content">
                    <p class="feature-meta">{date} · {publication}</p>
                    <h3><a href="{url}" target="_blank" rel="noopener">{title}</a></h3>
                    <p>{description}</p>
                    <a class="feature-link" href="{url}" target="_blank" rel="noopener">Read more<span aria-hidden="true"> →</span></a>
                </div>
            </article>
            """.format(
                photo=article["photo"],
                title=article["title"],
                publication=article["publication"],
                description=article["description"],
                url=article["url"],
                date=format_date(article["date"]),
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


def render_layout(
    *,
    page_title: str,
    current: str,
    main: str,
    meta_description: str | None = None,
    extra_body_end: str = "",
    defer_nav: bool = False,
) -> str:
    description = meta_description or "Portfolio of Raphael Hernandes, AI ethics researcher and journalist."
    header_classes = "site-header"
    if defer_nav:
        header_classes += " site-header--deferred"
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <meta name=\"description\" content=\"{description}\" />
    <title>{page_title}</title>
    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
        <link href=\"https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;500;600;700&display=swap\" rel=\"stylesheet\" />
            <link rel=\"stylesheet\" href=\"assets/css/style.css\" />
            <script src=\"https://kit.fontawesome.com/c796ba7827.js\" crossorigin=\"anonymous\"></script>
</head>
<body>
    <header class=\"{header_classes}\">
        <div class=\"container\">
            <a class=\"brand\" href=\"index.html\">Raphael Hernandes</a>
            <nav class=\"site-nav\">{render_nav(current)}</nav>
        </div>
    </header>
    <main>
        {main}
    </main>
    <footer class=\"site-footer\">
        <div class=\"container\">
                <p>© {datetime.now():%Y} Raphael Hernandes. All rights reserved.</p>
                {render_social_links('social-links-footer')}
        </div>
    </footer>
        {SCROLL_REVEAL_SCRIPT}
    {extra_body_end}
</body>
</html>"""


def build_home() -> None:
    hero = f"""
    <section class=\"hero\">
        <div class=\"container hero-grid\">
            <div class=\"hero-copy\">
                <h1>Raphael Hernandes</h1>
                <p class=\"hero-role\">AI ETHICS RESEARCHER · DATA, TECH JOURNALIST</p>
                {render_social_links('social-links-hero')}
                <div class=\"hero-links\">
                    <a href=\"academic.html\">Academic Work</a>
                    <span class="hero-links-separator" aria-hidden="true">·</span>
                    <a href=\"journalism.html\">Journalism Work</a>
                </div>
            </div>
            <div class=\"hero-media\">
                <img src=\"static/img/rh.jpg\" alt=\"Portrait of Raphael Hernandes\" loading=\"lazy\" />
            </div>
        </div>
    </section>
    """
    bio_paragraphs = [segment.strip()
                      for segment in BIO_TEXT.split("\n\n") if segment.strip()]
    bio = "".join(
        f"<p data-reveal>{paragraph}</p>" for paragraph in bio_paragraphs)
    bio_section = f"""
    <section class=\"section bio-section\">
        <div class=\"container narrow\">
            <h2>Bio</h2>
            {bio}
        </div>
    </section>
    """
    nav_script = """
    <script>
    (function() {
        var header = document.querySelector('.site-header');
        var heroImage = document.querySelector('.hero-media img');
        if (!header || !heroImage || !header.classList.contains('site-header--deferred')) { return; }

        function computeThreshold() {
            var rect = heroImage.getBoundingClientRect();
            var imageHeight = heroImage.offsetHeight || heroImage.naturalHeight || 0;
            return window.scrollY + rect.top + (imageHeight / 2);
        }

        var threshold = 0;

        function recalc() {
            threshold = computeThreshold();
            toggle();
        }

        function toggle() {
            if (threshold <= 0) {
                header.classList.remove('nav-visible');
                return;
            }

            if (window.scrollY >= threshold) {
                header.classList.add('nav-visible');
            } else {
                header.classList.remove('nav-visible');
            }
        }

        if (!heroImage.complete) {
            heroImage.addEventListener('load', recalc);
        }

        recalc();
        window.addEventListener('scroll', toggle, { passive: true });
        window.addEventListener('resize', recalc);
    })();
    </script>
    """
    content = hero + bio_section
    html = render_layout(
        page_title="Raphael Hernandes · AI Ethics Researcher & Journalist",
        current="index.html",
        main=content,
        meta_description="Portfolio and bio of Raphael Hernandes, AI ethics researcher and data journalist.",
        extra_body_end=nav_script,
        defer_nav=True,
    )
    OUTPUTS["home"].write_text(html, encoding="utf-8")


def build_category_page(category: str, *, title: str, filename: str) -> None:
    all_articles = load_articles()
    scoped = [item for item in all_articles if item["category"] == category]
    scoped.sort(key=lambda item: item["date"], reverse=True)
    highlights = [item for item in scoped if item["highlight"]]
    others = [item for item in scoped if not item["highlight"]]

    header_section = (
        """
        <section class=\"section section-title\">
            <div class=\"container\">
                <h1>{title}</h1>
            </div>
        </section>
        """.format(title=title)
    )

    if highlights:
        highlight_section = (
            """
            <section class=\"section\">
                <div class=\"container\">
                    <h2>Highlights</h2>
                    <div class=\"feature-grid\">{cards}</div>
                </div>
            </section>
            """.format(cards=render_feature_cards(highlights))
        )
    else:
        highlight_section = """
            <section class=\"section\">
                <div class=\"container\">
                    <div class=\"empty-state\">Highlights coming soon.</div>
                </div>
            </section>
        """

    list_section = ""
    if others:
        list_section = """
        <section class=\"section\">
            <div class=\"container\">
                <h2>More selected work</h2>
                <ul class=\"article-list\">{items}</ul>
            </div>
        </section>
        """.format(items=render_article_list(others))

    content = header_section + highlight_section + list_section
    html = render_layout(
        page_title=f"{title} · Raphael Hernandes",
        current=filename,
        main=content,
    )
    OUTPUTS_KEY = "academic" if category == "academic" else "journalism"
    OUTPUTS[OUTPUTS_KEY].write_text(html, encoding="utf-8")


def main() -> None:
    build_home()
    build_category_page("academic", title="Academic Work",
                        filename="academic.html")
    build_category_page("journalism", title="Journalism Work",
                        filename="journalism.html")


if __name__ == "__main__":
    main()
