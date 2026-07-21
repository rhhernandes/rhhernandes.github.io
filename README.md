# Raphael Hernandes — Personal Site

Static site for [raphaelhernandes.com](https://raphaelhernandes.com), built with a single Python script (stdlib only) and deployed via GitHub Pages.

## How it works

`build_site.py` generates every page from the content files. Layout lives in the script; **all page copy lives in `copy.toml`**; all list-based content lives in `articles.csv` and `data/*.json`. Text and entries can be changed without touching layout code.

```bash
python3 build_site.py
```

Pages generated: `index.html`, `about.html`, `research.html`, `journalism.html`, `speaking.html`, `recognition.html`, `teaching.html`, and `academic.html` (a redirect to `research.html`, preserving the old URL).

## Updating content

### All page copy — `copy.toml`

Every piece of text on the site — headings, intros, the About narrative, topic cards, meta titles/descriptions, the enquiries band, footer, nav labels, image alt text — lives in `copy.toml`, organised page by page with the shared sections (header/nav, enquiries band, footer) at the end. Edit the text there and rebuild. Text is inserted into the HTML as-is: write `&` as `&amp;` and use plain `<a href="...">` tags for links.

### Journalism pieces & research publications — `articles.csv`

Same format as before. `Category` is `Journalism` or `Academic` (Academic entries populate the Research page's publications list), `Highlight` puts a piece in the Journalism highlights grid, `Show` toggles visibility.

### Talks & engagements — `data/talks.json`

```json
{
  "title": "Talk title (optional)",
  "event": "Event or programme name (optional)",
  "venue": "Alan Turing Institute",
  "location": "London",
  "date": "May 2026",
  "url": "https://... (optional)",
  "notes": "One-line description (optional)"
}
```

Only `venue` is required — entries with just a venue render as a clean venue list. `date` is free text, displayed as written.

### Awards & honours — `data/awards.json`

```json
{
  "title": "Award name",
  "org": "Awarding body",
  "year": "2026",
  "detail": "One-line description.",
  "url": "https://... (optional)"
}
```

### Press about me — `data/press.json`

```json
{
  "outlet": "Outlet name",
  "title": "Headline",
  "date": "Jun 2026",
  "url": "https://...",
  "note": "Optional context line"
}
```

The "In the media" section on the Recognition page shows a placeholder until this file has at least one entry.

### Testimonials — `data/testimonials.json`

```json
{
  "quote": "What they said.",
  "name": "Person Name",
  "role": "Title, Organisation"
}
```

The testimonials section on the Speaking page appears automatically once this file has at least one entry.

### Teaching — `data/teaching.json`

```json
{
  "show_in_nav": false,
  "entries": [
    {
      "course": "Course name",
      "role": "Supervisor / Lecturer / …",
      "institution": "University of Cambridge",
      "term": "Michaelmas 2026",
      "description": "One-line description.",
      "url": "https://... (optional)"
    }
  ]
}
```

`teaching.html` always builds, but only joins the navigation when `show_in_nav` is `true` **or** `entries` is non-empty.

### Enquiries banner

The black "Speaking & advisory enquiries" band that closes every page is edited in `copy.toml` under `[shared.enquiries]` — it updates site-wide on rebuild. `{email}` in the button text is replaced at build time with the contact address.

### Malton band (home page only)

The faint line drawing above the enquiries band on the home page is
`static/img/kings-college-line.svg` — King's College, the Chapel and Clare Hall,
traced from Thomas Malton's 1799 aquatint (Yale Center for British Art, public
domain). It is emitted by `malton_band()` in `build_site.py` and passed to
`render_layout(pre_enquiries=…)` from `build_home()` only, so it appears on no
other page. It is decorative: `aria-hidden`, empty `alt`, lazily loaded.

Everything visual is tuned in `style.css` under **Malton band**:

| What | Knob |
| --- | --- |
| Zoom — how much of the drawing is in frame | `--malton-size` |
| Where the enquiries box sits | `--malton-band` (lower = it climbs) |
| Hiding the empty lawn behind the enquiries box | `--malton-sink` (the lawn is the bottom 29% of the drawing, so `size × 0.29` buries it exactly) |
| Which slice shows when cropped left/right | `--malton-x` (0% = trees and Clare Hall, 100% = Gibbs building) |
| Which slice shows when cropped top/bottom | `--malton-y` (0% = rooflines, 100% = lawn) |
| Top / bottom dissolve | gradient stops in `.malton-foot-art::before` |
| Left / right dissolve | `.malton-foot-art::after` |
| Line colour | the `fill` attribute in the SVG, currently `#e3dfd7` (`--divider`) |

How far the drawing climbs behind the index rows is the leftover,
`size − band − sink`, so there's nothing to set for it.

Two things that catch people out:

- **Only one of `x`/`y` does anything at a given width.** The artwork is
  1200×446 (ratio 2.69), so it crops left/right while the viewport is narrower
  than `size × 2.69`, and top/bottom once it is wider.
- **On phones a *bigger* `--malton-size` gives a tighter crop**, not a shrunken
  whole view, because `object-fit: cover` is cropping horizontally there.

### Contact email & socials

`CONTACT_EMAIL` and `SOCIAL_LINKS` are constants at the top of `build_site.py`.

### Images

`static/img/rh.jpg` is the full-resolution portrait (used for social-share previews); `rh-640.jpg` is the optimised display version. If the portrait changes, regenerate with:

```bash
sips -Z 640 -s format jpeg -s formatOptions 82 static/img/rh.jpg --out static/img/rh-640.jpg
```

## Publish

1. Edit content files.
2. `python3 build_site.py`
3. Commit and push — GitHub Pages serves the result.

## Attribution

- Icons by [Font Awesome](https://fontawesome.com/); type: Source Serif 4 & Source Sans 3.
- Website overhauled in July 2026 with the assistance of Claude Code.
