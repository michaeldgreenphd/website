# michaeldgreen.phd

Personal website of Michael D. Green, PhD — a flat single page, hosted on
GitHub Pages at [www.michaeldgreen.phd](https://www.michaeldgreen.phd/)
(the custom domain is set in `CNAME`). Edit `index.html`, push to `main`,
and the live site updates within a couple of minutes.

## How to edit the page

Everything is in `index.html`; each section is marked with a comment banner.

| Section (anchor)      | What to change there                                       |
|-----------------------|------------------------------------------------------------|
| `#about`              | the three bio paragraphs                                    |
| `#research`           | research areas, their blurbs, and project links             |
| `#fun`                | photos, playlist, podcasts                                   |
| `#cv`                 | position, education, expertise, select service and awards   |
| `#media`              | Substack blurb, select media appearances                    |
| `#contact`            | email, Signal, social links, collaboration interests        |
| `#publications`       | intro sentence only — the list itself is generated         |
| masthead              | name, role line, intro sentence, header link row            |

**Do not hand-edit the blocks between `<!-- data:… -->` and `<!-- /data:… -->`
markers** (citation metrics, the citations chart, recent posts, the
publication list, the ORCID "updated" date). `scripts/render_snapshot.py`
regenerates them from the JSON data files and would overwrite any manual
change. To change how they look, edit that script.

When your role changes, update the masthead role line **and** the
`jobTitle`/`affiliation` values in the JSON-LD block in `<head>`.

## Automatic data

Three scripts run twice a day via GitHub Actions
(`.github/workflows/update-scholar.yml`) and write `scholar_stats.json`,
`citations_over_time.png`, `citations_over_time_dark.png`,
`substack_posts.json`, and `orcid_works.json`; a fourth,
`scripts/render_snapshot.py`, renders those into `index.html`. The bot then
commits whatever changed, so pull before editing a local clone (editing in
the GitHub web editor is unaffected).

A red run means a script crashed and should be looked at; a Google Scholar
block only produces a warning and the previous numbers stay in place.
Details, including the optional ScraperAPI key, are in
`docs/SCHOLAR_PIPELINE.md`. To change the ORCID iD or the Substack feed,
edit the constants at the top of `scripts/fetch_orcid.py` and
`scripts/fetch_substack.py`.

## Adding files

See `docs/UPLOADING_FILES_GUIDE.md`. In short: manuscripts go in
`manuscripts/`, CVs in `cv/`, photos in `images/`, and the CV is linked from
two places in `index.html` (the header link row and the top of the CV
section) that both need updating when a new dated CV is uploaded.

## Repository layout

```
website/
├── index.html                  # The site (single page)
├── 404.html                    # Not-found page; forwards old root-level PDF links
├── published-manuscripts.html  # Manuscript PDFs, by year
├── faq.html                    # Contact FAQ
├── theme.css                   # Tokens for the two secondary pages above
├── fonts/                      # Self-hosted Fraunces, DM Sans, IBM Plex Mono
├── images/, cv/, manuscripts/  # Assets (see docs/UPLOADING_FILES_GUIDE.md)
├── scripts/                    # Data pipeline (fetch_*.py, render_snapshot.py)
├── .github/workflows/          # Twice-daily data refresh
├── scholar_stats.json, substack_posts.json, orcid_works.json,
│   citations_over_time*.png    # Generated — do not edit by hand
└── docs/                       # Pipeline and upload guides
```

The previous tabbed version of the site is preserved in git history at
commit `60bd128` — view it at
<https://github.com/michaeldgreenphd/website/blob/60bd128/tabbed-site.html>
or restore it with `git show 60bd128:tabbed-site.html > tabbed-site.html`.
