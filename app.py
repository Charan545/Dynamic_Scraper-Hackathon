import os
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Headline
from scraper import scrape_bbc_headlines
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///data.db")

# If using sqlite, allow check_same_thread false for SQLAlchemy
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)

# Create DB tables if not present
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.route("/")
def index():
    db = SessionLocal()
    headlines = db.query(Headline).order_by(Headline.fetched_at.desc()).limit(100).all()
    db.close()
    return render_template("index.html", headlines=headlines)

@app.route("/api/headlines")
def api_headlines():
    db = SessionLocal()
    items = db.query(Headline).order_by(Headline.fetched_at.desc()).limit(100).all()
    db.close()
    return jsonify([h.to_dict() for h in items])

@app.route("/scrape", methods=["GET", "POST"])
def scrape_trigger():
    # optional token protection
    token = os.environ.get("SCRAPE_TOKEN")
    if token:
        provided = request.args.get("token") or request.headers.get("X-SCRAPE-TOKEN")
        if provided != token:
            return "Unauthorized", 401

    try:
        items = scrape_bbc_headlines(limit=25)
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

    db = SessionLocal()
    added = 0
    for it in items:
        # naive duplicate avoidance: title match
        exists = db.query(Headline).filter(Headline.title == it["title"]).first()
        if exists:
            continue
        h = Headline(
            title=it["title"][:512],
            url=it.get("url"),
            source=it.get("source"),
            fetched_at=it.get("fetched_at", datetime.utcnow())
        )
        db.add(h)
        added += 1
    db.commit()
    db.close()
    return {"status": "ok", "added": added}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
