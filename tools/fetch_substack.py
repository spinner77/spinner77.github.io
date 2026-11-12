"""Fetch the Tangled Roots Substack feed into _data/substack.json.

Run by .github/workflows/pages.yml before each build. If substack_url is
empty in _config.yml, or the feed can't be reached, the existing file is
kept so the site still builds.
"""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_data" / "substack.json"


def substack_url():
    text = (ROOT / "_config.yml").read_text(encoding="utf-8")
    m = re.search(r'^substack_url:\s*"([^"]*)"', text, re.M)
    return m.group(1).strip().rstrip("/") if m else ""


def clean(text):
    text = unescape(re.sub(r"<[^>]+>", " ", text or ""))
    return re.sub(r"\s+", " ", text).strip()


def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    posts = []
    for item in root.iter("item"):
        title = clean(item.findtext("title"))
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        date = item.findtext("pubDate")
        iso = parsedate_to_datetime(date).isoformat() if date else ""
        summary = clean(item.findtext("description"))
        if len(summary) > 200:
            summary = summary[:197].rsplit(" ", 1)[0] + "…"
        posts.append({"title": title, "url": link, "date": iso, "summary": summary})
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, application/json, text/html;q=0.9, */*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def from_archive(url):
    """Backup: Substack's public archive list, used by its own website."""
    data = json.loads(get(url + "/api/v1/archive?sort=new&limit=50"))
    posts = []
    for p in data:
        if p.get("audience") not in (None, "everyone", "only_free"):
            continue
        posts.append({
            "title": clean(p.get("title")),
            "url": p.get("canonical_url") or f"{url}/p/{p.get('slug')}",
            "date": p.get("post_date") or "",
            "summary": clean(p.get("subtitle") or p.get("description")),
        })
    return posts


def main():
    url = substack_url()
    if not url:
        print("substack_url is empty; keeping", OUT.name)
        return
    posts = None
    for name, fetch in (("feed", lambda: parse(get(url + "/feed"))), ("archive", lambda: from_archive(url))):
        try:
            posts = fetch()
            print(f"Read {len(posts)} posts from the {name}")
            break
        except Exception as e:
            print(f"Could not read the {name}:", e)
    if posts is None:
        print("Keeping the existing list")
        return
    OUT.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
