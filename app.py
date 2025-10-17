from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from scraper import scrape_bbc_headlines  # ✅ import the working scraper

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///news.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Model
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255))
    source = db.Column(db.String(50))
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)
    summary = db.Column(db.Text)

# Routes
@app.route("/")
def home():
    headlines = News.query.order_by(News.fetched_at.desc()).all()
    return render_template("index.html", headlines=headlines)

@app.route("/scrape")
def scrape():
    headlines = scrape_bbc_headlines()
    for h in headlines:
        existing = News.query.filter_by(title=h["title"]).first()
        if not existing:
            db.session.add(News(
                title=h["title"],
                url=h["url"],
                source=h["source"],
                fetched_at=h["fetched_at"],
                summary=h["summary"]
            ))
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
