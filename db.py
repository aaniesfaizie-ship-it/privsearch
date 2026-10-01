from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Bookmark(db.Model):
    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False, unique=True)
    engine = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
    )
