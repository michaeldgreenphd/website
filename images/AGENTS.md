# images/ — photos and headshot assets

Read together with the root `AGENTS.md`.

- Headshot assets derive from `Fall 2025 Headshot.JPG`: `headshot-408.jpg`
  (page, 408×570), `headshot-icon.png` (256px square, link previews),
  `favicon-64.png`, `apple-touch-icon.png` (180px). When the photo changes,
  regenerate all four (Pillow; square crop biased toward the face) and
  update the JSON-LD `image` in `index.html`.
- The For Fun photos are JPEGs (quality 82, progressive, no EXIF):
  `film-1`, `film-3` and `chargers-sofi` at 640px from the larger originals
  in git history at commit `60bd128`; `film-2`, `running`, `city-1` and
  `city-2` at their old size, because no larger original exists (the
  `film 2.jpg` at `60bd128` is a different photo). A replacement photo
  should be about twice its displayed width (640px covers every slot).
- New files use lowercase-hyphenated names. Existing names with spaces stay
  as they are and are referenced with `%20`.
