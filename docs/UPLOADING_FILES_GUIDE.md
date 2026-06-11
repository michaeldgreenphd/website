# Uploading Files Guide

How to add new files to the website now that assets live in dedicated
folders. All uploads can be done from the GitHub web interface ("Add file →
Upload files" inside the target folder) or locally with git.

## Folder layout

| Folder         | What goes here                              | Example |
|----------------|---------------------------------------------|---------|
| `manuscripts/` | Publication PDFs                            | `manuscripts/Green et al 2027.pdf` |
| `cv/`          | CV PDFs                                     | `cv/Michael Green September 2026 CV.pdf` |
| `images/`      | Photos, logos, and other image assets       | `images/new headshot.jpg` |
| `docs/`        | Repository documentation (like this guide)  | — |

Files that stay in the repository **root** and should not be moved or edited
by hand: `index.html`, `published-manuscripts.html`, `faq.html`, `theme.css`,
`CNAME`, and the auto-generated data files (`scholar_stats.json`,
`substack_posts.json`, `citations_over_time.png`,
`citations_over_time_dark.png`) which the daily GitHub Action refreshes.

## Adding a new manuscript

1. Upload the PDF into the `manuscripts/` folder.
2. In `published-manuscripts.html`, copy an existing `manuscript-item` block,
   bump the number, and point its link at the new file:

   ```html
   <h3><a href="manuscripts/Your File 2027.pdf" target="_blank">Title</a></h3>
   ```

3. New entries go at the top of their year section (newest first). Bold your
   name in the co-author list with `<strong>Michael D. Green</strong>`.

## Updating the CV

1. Upload the new PDF into the `cv/` folder (keep the old ones for the
   record — they're small).
2. In `index.html`, find the CV section's download button and update it:

   ```html
   <a href="cv/Michael Green June 2026 CV.pdf" class="btn" target="_blank">Download Full CV (PDF)</a>
   ```

## Adding images

1. Upload into `images/`.
2. Reference as `images/your file.png` in `src` attributes. Below-the-fold
   images should include `loading="lazy" decoding="async"`.
3. Keep web-size images around or under ~200 KB where possible — large
   uploads slow the page down (photos display at modest sizes; ~600–900px on
   the long edge is plenty).

## Things to know

- **Spaces in filenames are fine** — browsers handle them — but the link in
  the HTML must match the filename exactly, including capitalization.
- **Old root-level links:** files used to live at the repository root (e.g.
  `/Michael Green June 2026 CV.pdf`). Any such links shared externally
  before the reorganization will 404; the current locations are
  `/cv/...` and `/manuscripts/...`.
- The Media, Research, and Scholar-dashboard data on the site updates
  automatically — no file uploads needed for those.
