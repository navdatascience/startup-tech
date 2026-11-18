# Startup Tech podcast

Startup ideas, new AI tools, and founder stories with Mimi and Alex — a daily
distillation of three YouTube channels so you don't have to watch hours of video:

- [Starter Story](https://youtube.com/@starterstory) — founder case studies and revenue playbooks
- [Greg Isenberg](https://youtube.com/@gregisenberg) — startup ideas and AI-native businesses
- [The Next New Thing AI](https://youtube.com/@thenextnewthingai) — new AI tools and profitable AI startups

## What's here

- **`feed.xml`** — RSS 2.0 feed of every episode, regenerated daily. Subscribe
  to it in any podcast app via the raw file URL:
  `https://raw.githubusercontent.com/navdatascience/startup-tech/main/feed.xml`
- **`notes.md`** — Date-wise episode notes, newest first. Each entry has the
  episode summary, the stories covered, and a listen link.
- **`transcripts/`** — Full transcript (the spoken script) for each episode,
  one file per day: `transcripts/YYYY-MM-DD.md`.
- **`scripts/update.py`** — The generator. It reads the local podcast catalog
  and rebuilds `feed.xml` and `notes.md` (Startup Tech episodes only).

## How it stays current

After each morning's episode is generated and published, the daily job
regenerates this repo's feed and notes, adds that day's transcript, and pushes
the update — no manual step.

Audio itself is hosted on the podcast feed; this repo holds the feed, the
notes, and the transcripts, not the MP3s.
