# Backlog

Work that was proposed, weighed, and parked — with the reasoning intact so a
future session can pick it up without re-deriving it. Settled "do not
re-propose" decisions are in `AGENTS.md`, not here. Items marked **owner**
need the owner's own accounts and can't be done from the repo.

Source: the 2026-09 seven-lens audit of the live homepage (performance,
resilience, security, accessibility, design, features, code quality) with
two-skeptic verification, plus follow-up discussion.

## Site polish (audit items not yet done)

- **Sharper For Fun photos (audit P1).** The seven photos are 320px PNGs —
  soft on a phone and ~880 KB together. Re-save as JPEG (quality ~80):
  `film 1`, `film 3` and `chargers sofi` have larger originals in git history
  at commit `60bd128` (`images/film 1.jpg`, `film 3.jpg`,
  `chargers sofi.jpg`); **`film 2.jpg` there is a different photo — re-save
  the pixels of `film 2.png` instead**; `running`, `city 1`, `city 2` have
  no larger originals. Update `width`/`height` attributes to match. Expected
  ~240 KB total.
- **Descriptive link text (A4).** In `index.html`: the Guardian item's
  "Full speech link *here*" → "watch the full speech on YouTube" (also
  fixes the missing "a" in that sentence); the publications intro's
  "collected *on this page*" → "PDFs of all published manuscripts are
  collected on a separate page" with the link on the noun phrase.
- **Year labels as headings (A5).** Emit `<h3 class="year-label">` instead of
  `<div>` in `scripts/render_snapshot.py` (the CSS class rule already
  overrides the bare `h3` rule) so screen-reader users can jump by year.
- **Print stylesheet (F2).** ~20 lines of `@media print`: hide the sticky
  bar, theme switch, skip link and iframes; force the light palette; open
  the publications fold (`details.pubs-fold::details-content` /
  `content-visibility`); avoid breaks inside entries; print pub URLs after
  titles. Test via iPhone Share → Print (Share → PDF does not apply print
  styles).
- **Page title with discipline.** `<title>` is just the name; "Michael D.
  Green, PhD · Population Health Researcher, Johns Hopkins" matches how
  people search and disambiguates a common name. Keep the JSON-LD `name`
  as is.
- **Share card (1200×630).** A designed Open Graph image — name and role in
  Fraunces on the green with the headshot — for LinkedIn/Bluesky/iMessage
  previews; keep the 256px square as a fallback `og:image` or switch
  `twitter:card` to `summary_large_image`.
- **Reading measure.** Paragraphs run ~90 characters per line on desktop
  (`p { max-width: 42rem }`); 65–75 is the comfortable range — try `~38rem`
  or `70ch`.
- **Typographic quotes.** Straight `"` and `'` in the prose → curly
  (“ ” ’), including `O'Brien`; prose only, never inside code or
  attributes.
- **`text-wrap: pretty`** on paragraphs (Safari/Chrome); older browsers
  ignore it.
- **Self-host the fonts on `faq.html` and `published-manuscripts.html`** so
  the "no web-font CDN" rule holds site-wide: reuse the `fonts/` files and
  add the weights those pages use, or reduce their weights to the
  homepage's set.
- **`docs/SCHOLAR_PIPELINE.md` is stale** (it still describes a "dashboard
  on the Research tab"). Fold what is still true into `scripts/AGENTS.md`
  and `.github/workflows/AGENTS.md`, delete it, and update the pointers in
  `README.md` and `scripts/fetch_scholar.py`.

## Email friction (parked by the owner)

- **Subject-line token.** Add to the FAQ's "Getting in touch" block: "put
  the word *heron* in your subject line so I know you've been here", plus a
  Gmail filter (subject doesn't contain the word → skip inbox, label
  "unread cold"). Costs a real reader four seconds; invisible to scrapers
  and templated outreach. **Owner** sets the filter.
- **Dedicated alias.** With Cloudflare Email Routing (free once DNS moves),
  publish `hello@michaeldgreen.phd` forwarding to Gmail; rotate it if it
  attracts junk. Different aliases per surface (site / CV / ORCID) show
  where lazy mail originates. **Owner.**

## Discoverability (**owner**, outside the repo)

- Link the domain from every profile: ORCID "Websites & social links",
  Google Scholar *Homepage*, LinkedIn website, and the Bluesky, Substack,
  Instagram and Threads bios — the reciprocal half of the JSON-LD `sameAs`
  claim.
- Ask the JHU department page (and Duke, if it lists him) to link to the
  site — the strongest identity signal available.
- Google Search Console and Bing Webmaster Tools (Bing's index feeds ChatGPT
  search and Copilot). A three-URL `sitemap.xml` is worth adding once
  Search Console exists.
- A Wikidata item (ORCID iD, Scholar ID, official website, employer);
  self-created researcher items are permitted there, unlike Wikipedia.
- One name form everywhere: "Michael D. Green".

## Infrastructure (**owner**, DNS)

- **Cloudflare in front of GitHub Pages**: move nameservers from Squarespace,
  A records to GitHub Pages plus `CNAME www → michaeldgreenphd.github.io`,
  SSL/TLS "Full", keep GitHub's Enforce HTTPS. Then: turn on *Block AI
  crawlers* (training bots only; leave search/answer crawlers allowed to
  match `robots.txt`) and *AI Labyrinth*; leave *Bot Fight Mode* off (it
  challenges RSS readers and link-preview fetchers). Pay-per-crawl was a
  limited beta, not a personal-site option.
- `Google-Extended` stays allowed in `robots.txt` (Gemini training and
  grounding; unrelated to Search/AI Overviews). Uncomment the block in
  `robots.txt` to opt out.

## Housekeeping

- An archive tag `tabbed-site-final` at commit `60bd128` could be created
  from the GitHub UI (Releases → new tag); the cloud session's git proxy
  refuses tag pushes.
- `docs/GITHUB_PAGES_SETUP.md` still describes the Squarespace DNS setup;
  update it if DNS moves to Cloudflare.
