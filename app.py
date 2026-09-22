from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.error

import db
from search import search_web

app = Flask(__name__)

# Flask needs this to sign the session cookie (where flash messages live).
# In production this must be a long random value that is NEVER committed to Git.
app.secret_key = "dev-only-change-me-later"

db.init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q", "")
    results = []
    if query:
        try:
            results = search_web(query)
        except (urllib.error.URLError, TimeoutError):
            flash("Search is temporarily unavailable — please try again.", "error")
    return render_template("index.html", query=query, results=results)


@app.route("/save", methods=["POST"])
def save():
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    engine = request.form.get("engine", "unknown").strip()

    if not title or not url:
        flash("Title and URL are required.", "error")
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
    app.run(debug=True)
