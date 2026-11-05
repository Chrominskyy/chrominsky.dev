# Chrominsky

Personal showcase page: C# / .NET backend work and native Apple apps (DevPulse, Mighty Markdown, CloudLatch, TapVault).

Single static `index.html`, no build step, no tracking. Fonts: Fraunces and IBM Plex Mono from Google Fonts. App icons in `assets/icons/` come from the respective public product site repositories.

Preview locally:

```sh
python3 -m http.server 8765
```

Live at https://chrominsky.dev, served by GitHub Pages from `main` (root). DNS is on Cloudflare, with A/AAAA records for GitHub Pages set to DNS only; the `CNAME` file holds the custom domain.
