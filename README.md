# PrivSearch

A small web app for searching and saving bookmarks, built with Flask and SQLite.

PrivSearch is a learning project exploring what a **privacy-focused search front-end**
would look like: no ads, no tracking scripts, no query logging of my own.

**Status:** v1.0 — working locally. Not yet deployed.

## Features

- **Search** — queries the Wikipedia public API server-side and renders the results
- **Save bookmarks** — stores a result (title, URL, engine) in SQLite
- **View saved** — a page listing every saved bookmark
- **Delete** — remove a bookmark
- **Duplicate protection** — saving the same URL twice is blocked by a database constraint
- **Flash messages** — success / info / error feedback, stored in the signed session cookie

## Tech stack

| Layer | Choice |
|---|---|
| Language | Python 3.14 |
| Web framework | Flask 3.1 |
| Templating | Jinja2 (server-rendered) |
| Database | SQLite |
| Search source | Wikipedia public API (no API key) |
| HTTP client | `urllib` (Python standard library) |

## Run it locally

```bash
git clone https://github.com/aaniesfaizie-ship-it/privsearch.git
cd privsearch
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py

```

Then open http://127.0.0.1:5000 in your browser.

## Project structure

```
privsearch/
├── app.py              # Flask app: routes and request handling
├── db.py               # SQLite helpers (init, add, list, delete)
├── search.py           # Fetches results from the Wikipedia API
├── templates/
│   ├── index.html      # search + results
│   └── saved.html      # saved bookmarks
├── requirements.txt
└── .gitignore
```

## How it works

1. A request to `/search?q=...` reaches `app.py`.
2. `app.py` calls `search_web()` in `search.py`.
3. `search.py` calls Wikipedia's API with a 5-second timeout, parses the JSON,
   and returns a list of `{title, url, engine}` dicts.
4. `app.py` renders `index.html` with those results.
5. Saving a result POSTs to `/save`, which writes a row through `db.py`.

## What I'd add next

- [ ] User accounts, so each person sees only their own bookmarks
- [ ] Swap SQLite for PostgreSQL
- [ ] Automated tests (pytest) + GitHub Actions CI
- [ ] Docker + `docker-compose`
- [ ] Self-hosted SearXNG for real multi-engine, privacy-respecting search

## Limitations (being honest)

- Results come from the **Wikipedia API**, so queries do leave the server. This is a
  search *front-end* prototype, not a fully private search engine.
- Single-user: there is no login yet, so all bookmarks share one list.
- Not deployed — it runs locally only.

## Notes

Built as part of a 30-day learning project to practise Linux, Python, Flask, SQLite and Git.
