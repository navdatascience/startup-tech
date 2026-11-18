#!/usr/bin/env python3
"""Regenerate feed.xml + notes.md for the Startup Tech podcast from the
local podcast-helper manifest, inside a checkout of navdatascience/startup-tech.

Only episodes published to the "Startup Tech podcast" feed are included
(the manifest also contains Personal Tech episodes — those are filtered out).

Usage:  podcast-helper manifest read > /tmp/startup-manifest.json
        python3 scripts/update.py /tmp/startup-manifest.json <repo-dir>

Transcripts: the daily job copies each episode's script to
transcripts/<YYYY-MM-DD>.md in the repo before committing; this script
links to it from notes.md when the file exists.
"""
import json
import os
import sys
from datetime import datetime, timezone
from email.utils import format_datetime

MANIFEST_PATH, REPO_DIR = sys.argv[1], sys.argv[2]
FEED_TITLE_WANT = "Startup Tech podcast"

with open(MANIFEST_PATH, encoding="utf-8") as f:
    data = json.load(f)

all_episodes = data.get("episodes", [])
# Keep only episodes that belong to a feed titled Startup Tech podcast.
# Episodes carry no per-episode feed title in the manifest, so we match by
# slug prefix "startup-tech-" (generate-slug from titles "Startup Tech — ...").
episodes = [e for e in all_episodes if e.get("slug", "").startswith("startup-tech-")]
episodes = sorted(episodes, key=lambda e: e["created_at"], reverse=True)

feeds = data.get("feeds", []) or []
feed = next((f for f in feeds if f.get("feed_title") == FEED_TITLE_WANT), {}) or {}
feed_title = feed.get("feed_title", FEED_TITLE_WANT)
feed_url = feed.get("feed_url", "")


def fmt_date(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).strftime("%B %d, %Y")


def date_slug(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d")


def rfc822(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return format_datetime(dt.astimezone(timezone.utc))


def topics_body(topics):
    if not topics:
        return ""
    lines = topics.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def esc(text):
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


items_xml = []
for ep in episodes:
    url = ep.get("episode_url", "")
    size = 0
    path = ep.get("path", "")
    if path and os.path.exists(path):
        size = os.path.getsize(path)
    items_xml.append(
        "    <item>\n"
        f"      <title>{esc(ep['title'])}</title>\n"
        f"      <description>{esc(ep.get('description', ''))}</description>\n"
        f"      <pubDate>{rfc822(ep['created_at'])}</pubDate>\n"
        f"      <guid isPermaLink=\"false\">{esc(ep['slug'])}</guid>\n"
        f"      <enclosure url=\"{esc(url)}\" length=\"{size}\" type=\"audio/mpeg\" />\n"
        "    </item>"
    )

feed_xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    "<rss version=\"2.0\">\n"
    "  <channel>\n"
    f"    <title>{esc(feed_title)}</title>\n"
    f"    <link>{esc(feed_url)}</link>\n"
    "    <description>Startup ideas, new AI tools, and founder stories from Starter Story, Greg Isenberg, and The Next New Thing AI — distilled daily.</description>\n"
    f"    <lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>\n"
    + "\n".join(items_xml)
    + "\n  </channel>\n</rss>\n"
)
with open(os.path.join(REPO_DIR, "feed.xml"), "w", encoding="utf-8") as f:
    f.write(feed_xml)

lines = [
    "# Startup Tech — Episode Notes",
    "",
    "Startup ideas, new AI tools, and founder stories with Mimi and Alex. Newest first. "
    "Sources: Starter Story, Greg Isenberg, and The Next New Thing AI on YouTube. "
    "Each entry links to the episode audio and its full transcript.",
    "",
]
for ep in episodes:
    mins = round(ep.get("duration_secs", 0) / 60)
    lines.append(f"## {fmt_date(ep['created_at'])} — {ep['title']}")
    lines.append("")
    listen = ep.get("episode_url", "")
    if listen:
        lines.append(f"- Listen: {listen}")
    lines.append(f"- Length: ~{mins} minutes")
    tpath = os.path.join(REPO_DIR, "transcripts", f"{date_slug(ep['created_at'])}.md")
    if os.path.exists(tpath):
        lines.append(f"- Transcript: [transcripts/{date_slug(ep['created_at'])}.md](transcripts/{date_slug(ep['created_at'])}.md)")
    desc = ep.get("description", "")
    if desc:
        lines.append(f"- Summary: {desc}")
    body = topics_body(ep.get("topics", ""))
    if body:
        lines.append("")
        lines.append(body)
    lines.append("")
    lines.append("---")
    lines.append("")

with open(os.path.join(REPO_DIR, "notes.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines).rstrip() + "\n")

print(f"episodes: {len(episodes)}")
print(f"feed.xml + notes.md written to {REPO_DIR}")
