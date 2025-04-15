from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models import JournalEntry
from app import db
from app.sentiment import analyze_sentiment

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.journal'))

@main_bp.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        text = request.form.get('entry')
        if text:
            # Perform sentiment analysis
            sentiment_result = analyze_sentiment(text)
            
            # Create journal entry with sentiment
            entry = JournalEntry(
                text=text,
                sentiment_label=sentiment_result['label'],
                sentiment_score=sentiment_result['score']
            )
            db.session.add(entry)
            db.session.commit()
            
        return redirect(url_for('main.journal'))

    # Get all entries for display
    entries = JournalEntry.query.order_by(JournalEntry.timestamp.desc()).all()
    return render_template('index.html', entries=entries)

# API endpoints for JSON data
@main_bp.route('/api/journal', methods=['GET'])
def get_entries_api():
    entries = JournalEntry.query.order_by(JournalEntry.timestamp.desc()).all()
    return jsonify([entry.to_dict() for entry in entries])

@main_bp.route('/api/journal', methods=['POST'])
def create_entry_api():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Text is required'}), 400
    
    # Perform sentiment analysis
    sentiment_result = analyze_sentiment(data['text'])
    
    # Create journal entry with sentiment
    entry = JournalEntry(
        text=data['text'],
        sentiment_label=sentiment_result['label'],
        sentiment_score=sentiment_result['score']
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201
