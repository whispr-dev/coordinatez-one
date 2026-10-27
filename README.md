# Coordinates 1.0.0

A complete static website by whispr.dev: WGS 84 GPS coordinate conversion, a draggable orthographic globe, day/night shading and world civil clocks.

## Run on Windows

No installation, npm build, API key or remote font/CDN is needed. Double-click `dist/index.html` to open the tool directly. All runtime assets are included. Clipboard and device location require HTTPS or localhost in browsers that restrict those features; coordinates, globe and clocks work directly from a file.

For a local HTTP preview, with Python 3 installed:

```powershell
Set-Location .\coordinates
python -m http.server 8000 --directory dist
```

Open http://localhost:8000/ . On Linux use `python3` instead of `python`.

## Use

Paste latitude first, longitude second. Examples:

- `35.6762, 139.6503`
- `35° 40′ 34.32″ N, 139° 39′ 1.08″ E`
- `33 52 7.68 S, 151 12 33.48 E`

Choose Decimal or Deg · min · sec; the fields, globe labels and equivalent reading change together. Invalid coordinates are rejected and keep the current selection. Copy copies the equivalent format. Click a city/zone to centre it. Click empty globe to select a point. Drag to turn. When the globe has keyboard focus, arrows turn it and Enter selects its centre. Reset returns to Greenwich. Recenter returns to the selected point after dragging.

Major cities covers 41 locations. All time zones includes 418 distinct civil zones, represented by 419 locations (London and Greenwich share one zone). Search matches names and IANA identifiers; Show more progressively renders the catalogue. All zone dots are on the globe even when the list is filtered. Some dots overlap at this world scale.

## Upload to an existing server

Copy **the contents of `dist/`** into the active site document root. It contains all public files including robots.txt, sitemap.xml, llms.txt, cookies.txt and README.md. Do not configure a catch-all HTML response for missing text/XML files. Serve unknown paths as 404.

For an existing writable web root and configured SSH alias, PowerShell 7.2+ and Node 22+:

```powershell
.\Deploy.ps1 -HostAlias lon1 -WebRoot /srv/coordinates/site -Origin https://your-domain.example
```

Replace the example web root and domain with the actual active ones. The script updates SEO URLs, verifies the files, uploads via OpenSSH, and compares public text-file responses against the real local files. It does not modify server/proxy configuration or delete existing files. Back up an existing site before uploading replacements. A Cloudflare cache can require a purge if public verification sees old content.

For manual upload, first run:

```powershell
node scripts/configure-origin.mjs https://your-domain.example
node scripts/brand-check.mjs
```

Recommended Caddy block for a standalone static document root:

```caddyfile
your-domain.example {
    root * /srv/coordinates/site
    encode zstd gzip
    file_server
}
```

Recommended Nginx location inside the existing correct server block:

```nginx
root /srv/coordinates/site;
index index.html;
location / { try_files $uri $uri/ =404; }
```

Replace the example origin/root with the actual values. Do not paste a second server block into an unknown configuration. When a site's existing reverse proxy serves other routes, its static public-file routing must be integrated into that configuration.

## Verify

Node 22 or newer, no packages to install:

```powershell
node --test tests/core.test.cjs
node scripts/brand-check.mjs
```

Tests cover known city coordinates, DMS rounding carry, 3,602 round trips including poles/antimeridian, malformed inputs, civil DST/date rollover, half/quarter hour offsets, geographic lookup and seasonal solar position. Browser QA covered Tokyo selection, format switching, invalid paste, keyboard selection, clipboard, globe clicks and 390px mobile layout.

## Source and data

- `dist/index.html`, `style.css`, `app.js`: complete user interface.
- `dist/core.js`: pure shared conversion, clock and solar functions, usable with `require()` for tests.
- `dist/data.js`: bundled Natural Earth land geometry and zone reference points.
- `dist/vendor/d3.min.js`: D3 7.9.0, ISC; license included.
- `dist/vendor/tz.js`: @photostructure/tz-lookup 11.7.0, CC0; license included. Approximate offline lookup, not exact legal boundaries.
- `zone.tab`: IANA TZ source reference positions, retrieved 26 October 2026 from https://github.com/eggert/tz/blob/main/zone.tab . Public domain.
- `land.geojson`: Natural Earth 1:110m land, retrieved 26 October 2026 from https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_land.geojson . Public domain; includes small-scale simplification.
- `scripts/make-data.py` regenerates data.js from the included data, using Python 3 with the standard library only.
- `scripts/brand-assets.cjs` regenerates JPEG share cards using the bundled D3 and optional `sharp` 0.35.5. Prebuilt cards are included; the website has no Node dependency.
- `dist/site.json`: website metadata. The tool is correctly classified as a website, not a game.
- `dist/og.jpg`: 1200×630. `dist/x-banner.jpg`: 1200×264. Favicon is an original SVG instrument globe.

Runtime assets are vendored; see SHA256SUMS.txt for exact bytes. Application code and original brand assets © 2026 whispr.dev. Third-party data/code retain their stated licenses. No third-party runtime requests, tracking or cookies are added by this tool.

## Accuracy and limits

The main risk is timezone lookup close to a border. The lookup data are compressed and approximate, and civil rules can change; select a named city/zone for its known civil clock. The application uses your device's time and the browser's IANA timezone data, so keep both up to date. New zones unsupported by an old browser show an explicit unavailable reading. The geometric night line ignores atmospheric refraction, elevation and terrain. The graticule shows geography; it does not claim to draw political timezone boundaries. Decimal output is displayed to six places, DMS seconds to three; display precision does not establish survey accuracy. No datum transformation, address geocoding or navigation-grade position accuracy is claimed.
