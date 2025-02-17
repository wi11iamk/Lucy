# config.py

# API and Model Configuration
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"  # Securely load this (e.g., from an environment variable in production)
SENTIMENT_MODEL = "sentiment-analysis"
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"

# Few-Shot Examples for LLM prompt engineering
FEW_SHOT_EXAMPLES = [
    {
        "input": "I'm feeling really overwhelmed and confused lately.",
        "emotion_summary": "fear: 0.70, sadness: 0.60",
        "response": "I'm sorry you're feeling overwhelmed. It might help to take a moment to breathe and focus on something familiar. I'm here to listen if you want to share more."
    },
    {
        "input": "I feel isolated and alone.",
        "emotion_summary": "loneliness: 0.85, sadness: 0.75",
        "response": "It sounds like you're feeling very lonely right now. Remember, you're not alone, and it's okay to seek support. Would you like to talk about what might help you feel more connected?"
    }
]

# Logging
ENABLE_LOGGING = True
LOG_FILE_PATH = "logs/interaction_log.jsonl"

# Security and Authentication (reused from earlier)
AUTHORIZED_USERS = {
    "nurse_anna": "password123",
    "dr_smith": "securepass"
}

# Other configuration parameters
ENABLE_SPEECH_ANALYSIS = True  # example parameter from earlier
SENTENCE_LENGTH_THRESHOLD = 2  # example parameter from earlier
