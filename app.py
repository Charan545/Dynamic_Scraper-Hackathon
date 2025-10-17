from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from scraper import scrape_bbc_articles
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///news.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Model
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255))
    source = db.Column(db.String(50))
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)

# Scraper function
def scrape_and_store():
    articles = scrape_bbc_articles(limit=10)
    new_count = 0
    with app.app_context():
        for a in articles:
            if not News.query.filter_by(title=a["title"]).first():
                db.session.add(News(
                    title=a["title"],
                    url=a["url"],
                    source=a["source"],
                    fetched_at=a["fetched_at"],
                    content=a["content"]
                ))
                new_count += 1
        db.session.commit()
    print(f"[{datetime.utcnow()}] Scraping done. {new_count} new articles added.")

# Homepage
@app.route("/")
def home():
    headlines = News.query.order_by(News.fetched_at.desc()).all()
    return render_template("index.html", headlines=headlines)

# Manual scrape endpoint
@app.route("/scrape")
def scrape():
    scrape_and_store()
    return {"message": "Scrape successful!"}

@app.route("/article/<int:article_id>")
def article(article_id):
    article = News.query.get_or_404(article_id)
    return render_template("article.html", article=article)

# API endpoint
@app.route("/api")
def api():
    articles = News.query.order_by(News.fetched_at.desc()).all()
    return jsonify([{
        "title": a.title,
        "url": a.url,
        "source": a.source,
        "fetched_at": a.fetched_at.strftime("%Y-%m-%d %H:%M:%S"),
        "content": a.content
    } for a in articles])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Start scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=scrape_and_store, trigger="interval", minutes=30)
    scheduler.start()
    print("Scheduler started: Scraping will run every 30 minutes.")
    app.run(debug=True)
