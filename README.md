# chrominsky.dev

Personal site of Bartosz Chrominski: C# / .NET backend work on AWS and native Apple apps (DevPulse, Mighty Markdown, CloudLatch, TapVault).

Live at https://chrominsky.dev (English) and https://chrominsky.dev/pl/ (Polish).

## Layout

| Path | Purpose |
| --- | --- |
| `index.html` | English page, the source of truth |
| `pl/index.html` | Polish page, generated from `index.html` |
| `scripts/build_pl.py` | Translation pairs and the generator for `pl/index.html` |
| `404.html` | Not-found page served by GitHub Pages |
| `assets/fonts/` | Self-hosted Fraunces and IBM Plex Mono (OFL 1.1) |
| `assets/shots/`, `assets/icons/` | App visuals from the public product site repositories |
| `assets/og-image.png` | Social preview image (1200×630) |
| `robots.txt`, `sitemap.xml` | Crawler metadata |
| `CNAME` | Custom domain for GitHub Pages |

No build step, no third-party requests, no tracking.

## Editing

1. Edit `index.html`.
2. Regenerate the Polish page. The script fails if an English string it translates has changed, so update the matching pair in `scripts/build_pl.py` first:

   ```sh
   python3 scripts/build_pl.py
   ```

3. Preview locally:

   ```sh
   python3 -m http.server 8765
   ```

## Hosting

GitHub Pages builds from `main` (root). DNS is on Cloudflare: A/AAAA records for GitHub Pages and the `www` CNAME are set to DNS only, so GitHub issues the HTTPS certificate. Mail for `contact@chrominsky.dev` is handled separately from the site.
