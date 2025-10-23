# Raphael Hernandes Portfolio

Static site for [raphaelhernandes.com](https://raphaelhernandes.com) built with a custom, mobile-first theme.

## Overview

- `build_site.py` generates the three English pages (`index.html`, `academic.html`, `journalism.html`) using the data in `articles.csv`.
- `articles.csv` now includes a `Category` column (`academic` or `journalism`) alongside the existing `Highlight` field to drive featured items.
- Styles live in `assets/css/style.css`; the build also loads Font Awesome via kit for iconography.

## Update Workflow

1. Edit `articles.csv` with new work, setting `Highlight` for feature cards as needed.
2. Run `python build_site.py` to regenerate the static pages.
3. Commit the updated files and publish via GitHub Pages.

## Attribution

- Icons provided by [Font Awesome](https://fontawesome.com/).
- Website refreshed in October 2025 with the assistance of Generative AI (GPT-5-Codex).
