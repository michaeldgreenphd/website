# images/ — photos and headshot assets

Read together with the root `AGENTS.md`.

- Headshot assets derive from `Fall 2025 Headshot.JPG`: `headshot-408.jpg`
  (page, 408×570), `headshot-icon.png` (256px square, link previews),
  `favicon-64.png`, `apple-touch-icon.png` (180px). When the photo changes,
  regenerate all four (Pillow; square crop biased toward the face) and
  update the JSON-LD `image` in `index.html`.
- The For Fun photos are 320px PNGs; sharper JPEG replacements, and the
  source-file caveats for each, are in `docs/BACKLOG.md`.
- New files use lowercase-hyphenated names. Existing names with spaces stay
  as they are and are referenced with `%20`.
