import os
import urllib.error
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

import db
from search import search_web

# Read values from the local .env file into the environment.
load_dotenv()

# Fail loudly if the secret is missing, instead of running with a weak default.
secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    raise RuntimeError(
        "SECRET_KEY is missing. Create a .env file with SECRET_KEY=your-secret."
    )

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key

# Debug mode is configuration, not a hardcoded truth.
debug_enabled = os.environ.get("FLASK_DEBUG", "0") == "1"

db.init_db()


@app.route("/health")
def health():
    """Lightweight endpoint for Docker / monitoring to check the app is up."""
    return {"status": "ok"}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()[:200]
    results = []
    if query:
        try:
            results = search_web(query)
        except (urllib.error.URLError, TimeoutError, ValueError):
            flash("Search is temporarily unavailable. Please try again.", "error")
    return render_template("index.html", query=query, results=results)


@app.route("/save", methods=["POST"])
def save():
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    engine = request.form.get("engine", "unknown").strip()

    parsed = urlparse(url)
    valid_url = parsed.scheme.lower() in {"http", "https"} and bool(parsed.netloc)

    if not title or not url:
        flash("Title and URL are required.", "error")
    elif not valid_url:
        flash("Only valid HTTP or HTTPS URLs are allowed.", "error")
    elif db.add_bookmark(title, url, engine):
        flash("Bookmark saved.", "success")
    else:
        flash("This bookmark is already saved.", "info")

    return redirect(url_for("saved"))


@app.route("/saved")
def saved():
    bookmarks = db.get_bookmarks()
    return render_template("saved.html", bookmarks=bookmarks)


@app.route("/delete/<int:bookmark_id>", methods=["POST"])
def delete(bookmark_id):
    db.delete_bookmark(bookmark_id)
    flash("Bookmark deleted.", "success")
    return redirect(url_for("saved"))


if __name__ == "__main__":
    app.run(debug=debug_enabled)
