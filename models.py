from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Headline(Base):
    __tablename__ = "headlines"
    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    url = Column(String(1024))
    source = Column(String(128))
    fetched_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "fetched_at": self.fetched_at.isoformat(),
            "summary": self.summary,
        }
