# mojogamesstudio.com

The Mojogames Studio website. **The full site is being built in its own Claude chat
(user, 2026-10-28); the Atlas of Wanderworlds chat only supplies the game build.**

## State when handed off (2026-10-28)

A starter site, LIVE since 2026-10-28 at https://mojogamesstudio.com (GitHub Pages, HTTPS enforced, DNS at Porkbun: four A records plus www CNAME; email MX and TXT untouched). Pull before editing: GitHub may add commits (e.g. when the custom domain is re-saved).
- `index.html`: minimal home page (logo, an Atlas of Wanderworlds card with a Play
  button linking to `atlas/`), dark pixel-star background, Silkscreen font. Checked at
  desktop and narrow widths. Replace or restyle freely.
- `img/`: `mojogames-logo.png` (900 px, from `Projects/mojogames/Mojogames Logo v2.png`),
  `atlas-icon.png` and `favicon.png` (the Atlas app icon).
- `atlas/`: the Atlas web build. Don't edit by hand (see below).
- `CNAME` (mojogamesstudio.com) and `.nojekyll`, for GitHub Pages.

## Decisions already made by the user (2026-10-28)

- Atlas of Wanderworlds is hosted on this site, at `https://mojogamesstudio.com/atlas/`.
- Hosting: **GitHub Pages**, a **public** repo (planned name `zagmojo/mojogamesstudio.com`)
  holding only the site files. Cloudflare Pages was ruled out: it caps files at 25 MB
  and the game's `atlas/index.wasm` is about 38 MB (GitHub's limit is 100 MB per file).
- Scope: minimal first (home + Atlas), the other planned pages later
  (`business-docs/checklist.md`, website item).

## Still to do

1. ~~`git init`, create the public repo with `gh`, push, turn on Pages (main branch, root).~~
   Done 2026-10-28: https://github.com/zagmojo/mojogamesstudio.com, Pages on (main, /),
   custom domain mojogamesstudio.com from `CNAME`.
2. (Done 2026-10-28.) DNS at Porkbun (the user enters these; leave the email-forwarding MX records alone):
   A records for `mojogamesstudio.com` to 185.199.108.153, 185.199.109.153,
   185.199.110.153, 185.199.111.153; CNAME `www` to `zagmojo.github.io`. Remove
   Porkbun's default parking records for the root and `www` if present.
3. (Done 2026-10-28.) Once GitHub shows the certificate, turn on "Enforce HTTPS".
4. Next: the rest of the site (Knaights, HAMB, Protorogo, press kit, contact), built in the business chat.

## The Atlas build (contract with the Atlas chat)

- The game lives in `atlas/` and must be served as-is (no build step, no renaming).
  It needs HTTPS (Godot's web engine refuses plain http), which Pages provides.
- Updated by `C:\Users\zagmo\Projects\AtlasOfWanderworlds\prototype\tools\publish_web.ps1`:
  it rebuilds the game, replaces `atlas/`, and with `-Push` commits and pushes this repo.
- It is an installable web app (manifest + service worker in `atlas/`), so keep the
  files together under `atlas/`.
