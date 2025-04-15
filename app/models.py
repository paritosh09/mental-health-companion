from app import db
from datetime import datetime

class JournalEntry(db.Model):
    __tablename__ = 'journal_entry'

    id = db.Column(db.Integer, primary_key=True)  # Changed to Integer for better SQLite compatibility
    text = db.Column(db.String(500), nullable=False)  # Text should not be nullable
    sentiment_label = db.Column(db.String(20), nullable=True)
    sentiment_score = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<JournalEntry {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'sentiment_label': self.sentiment_label,
            'sentiment_score': self.sentiment_score,
            'timestamp': self.timestamp.isoformat()
        }
