"""Point each Steam game card at the game's current Steam header image.

Steam gives every header image a new URL (a hash in the path) when the
developer uploads a new one, and browsers can't ask Steam for it directly.
This script asks Steam's store API for each app's current header URL and
rewrites the matching <img> in the listed pages. It also keeps a backup
copy of each header in img/steam/<app id>.jpg, which the page shows if
Steam's image fails to load. Run by the "Steam images" GitHub Action every
few hours; safe to run by hand.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html"]
BACKUP_DIR = ROOT / "img" / "steam"

# Any Steam header image URL for an app, old or new.
HEADER_RE = re.compile(
    r"https://shared\.akamai\.steamstatic\.com/store_item_assets/steam/apps/(\d+)/[^\"'\s]*?header\.jpg(?:\?[^\"'\s]*)?"
)


def current_header(app_id: str) -> str | None:
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&filters=basic"
    req = urllib.request.Request(url, headers={"User-Agent": "mojogamesstudio-site"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    entry = data.get(app_id) or {}
    if not entry.get("success"):
        return None
    header = entry["data"].get("header_image")
    # Drop Steam's cache-buster; the hash in the path already changes per upload.
    return header.split("?")[0] if header else None


def save_backup(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "mojogamesstudio-site"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists() or dest.read_bytes() != data:
        dest.write_bytes(data)
        print(f"backup saved: {dest.relative_to(ROOT)} ({len(data)} bytes)")


def main() -> int:
    changed = False
    cache: dict[str, str | None] = {}
    for name in PAGES:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")

        def swap(m: re.Match) -> str:
            app_id = m.group(1)
            if app_id not in cache:
                cache[app_id] = current_header(app_id)
            new = cache[app_id]
            if not new:
                print(f"{name}: app {app_id}: no header from Steam, left as is")
                return m.group(0)
            backup = BACKUP_DIR / f"{app_id}.jpg"
            if new != m.group(0).split("?")[0] or not backup.exists():
                save_backup(new, backup)
            return new

        updated = HEADER_RE.sub(swap, text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"{name}: updated")
            changed = True
    if not changed:
        print("No changes: every card already shows the current Steam header.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
