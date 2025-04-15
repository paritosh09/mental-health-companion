from transformers import pipeline

# Load the model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Recommendation mapping
recommendations = {
    "POSITIVE": [
        "Keep up the positive mindset! 🌞",
        "Celebrate your wins, no matter how small. 🎉",
        "Channel your good energy into something creative!"
    ],
    "NEGATIVE": [
        "Take a deep breath. You’re doing your best. 💙",
        "It’s okay to feel down — this too shall pass.",
        "Consider journaling or talking to a trusted friend. 📝"
    ]
}

def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    label = result['label']

    # Fetch supportive messages
    support_message = recommendations.get(label, ["You're not alone. ❤️"])
    
    return {
        "label": label,
        "score": result['score'],
        "message": support_message
    }
