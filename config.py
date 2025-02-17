# config.py

# AI Model Configuration
MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"

# Speech Analysis Configuration
ENABLE_SPEECH_ANALYSIS = True  # Set to False if speech tracking is not needed
SENTENCE_LENGTH_THRESHOLD = 2  # Threshold for detecting cognitive decline

# Safety Filters
FLAGGED_WORDS = ["alone", "harm", "danger", "leave"]

# Security & Encryption
ENCRYPTION_KEY_PATH = "secure_storage/key.txt"

# Logging
ENABLE_LOGGING = True
LOG_FILE_PATH = "logs/conversation_logs.txt"

# User Authentication
AUTHORIZED_USERS = {
    "nurse_anna": "password123",
    "dr_smith": "securepass"
}
