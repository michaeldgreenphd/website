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

Files that stay in the repository **root** and should not be moved:
`index.html`, `404.html`, `published-manuscripts.html`, `faq.html`,
`theme.css`, `CNAME`, and the auto-generated data files
(`scholar_stats.json`, `substack_posts.json`, `orcid_works.json`,
`citations_over_time.png`, `citations_over_time_dark.png`) which the
twice-daily GitHub Action refreshes and renders into `index.html`.

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
   record — they're small, and links already shared keep working).
2. In `index.html`, the CV is linked in **two** places. Search for
   `cv/Michael%20Green` and update both:

   ```html
   <a href="cv/Michael%20Green%20June%202026%20CV.pdf" target="_blank" rel="noopener noreferrer">CV</a>
   …
   … is in the <a href="cv/Michael%20Green%20June%202026%20CV.pdf" target="_blank" rel="noopener noreferrer">full CV (PDF)</a>.
   ```

   Spaces in the filename are written as `%20` in the link.

## Adding images

1. Upload into `images/`.
2. Reference as `images/your%20file.png` in `src` attributes (spaces as
   `%20`), and add the image's pixel `width` and `height` attributes so the
   page does not shift while it loads. Below-the-fold images should include
   `loading="lazy" decoding="async"`.
3. Keep web-size images around or under ~200 KB where possible — large
   uploads slow the page down (photos display at modest sizes; ~600–900px on
   the long edge is plenty).

## Things to know

- **Spaces in filenames are fine** but write them as `%20` in links, and
  match the filename exactly, including capitalization. New files are easier
  to link with lowercase, hyphenated names (`new-headshot.jpg`).
- **Old root-level links:** files used to live at the repository root (e.g.
  `/Michael Green June 2026 CV.pdf`). `404.html` forwards those old links to
  `/cv/...` or `/manuscripts/...` automatically, as long as the dated file
  is still there.
- The citation metrics, chart, recent posts, and publication list update
  automatically — no file uploads needed for those.
