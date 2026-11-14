# Clinical Safety Toolkit

A plain-English clinical safety toolkit for practice managers and partners in general practice, from Staffordshire Training Hub.

## How it's published

The site is built with Astro and published to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`. Publishing only runs while the repository is public.

## Changing the words

Page text lives in `src/pages` (`.mdx` files, one per page). Templates live in `src/data/templates.json`; after changing them, run `python3 scripts/make_downloads.py` to rebuild the Word and Excel downloads in `public/downloads`.

The top of each page file holds its title, intro line (`lede`) and the date its sources were last checked (`checked`).
