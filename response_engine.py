from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

def dementia_friendly_response(user_input):
    sentiment = sentiment_model(user_input)[0]['label']
    
    if sentiment == "NEGATIVE":
        return "I understand that might feel difficult. Would you like to talk about something comforting?"
    elif len(user_input.split()) > 20:
        return "Let's take it step by step. Can you tell me more about that?"
    else:
        return "That sounds interesting! Tell me more."
