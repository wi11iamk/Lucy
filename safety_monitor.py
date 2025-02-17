import logging
from transformers import pipeline

# Configure logging for misalignment tracking
logging.basicConfig(filename="logs/safety_audit.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Load AI classifier for safety filtering
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define AI safety categories
SAFETY_CATEGORIES = [
    "self-harm", 
    "violence", 
    "misleading medical advice", 
    "manipulative language"
]

def log_misalignment(response):
    """Logs potentially misaligned AI responses for future auditing."""
    with open("logs/safety_audit.log", "a") as log_file:
        log_file.write(f"⚠️ Misaligned Response Detected: {response}\n")

def constitutional_safety_filter(response):
    """Uses AI-based classification to detect unsafe or misleading responses."""
    result = classifier(response, SAFETY_CATEGORIES)
    
    # Flag responses if any category exceeds 80% probability
    if any(score > 0.8 for score in result["scores"]):
        log_misalignment(response)  # Log flagged response
        return "⚠️ Safety Warning: This response has been flagged for review."
    
    return response
