import os
import time
from collections import defaultdict
from cryptography.fernet import Fernet

from dotenv import load_dotenv
load_dotenv()

# Load encryption key securely from environment variables
ENCRYPTION_KEY = os.getenv("LUCY_ENCRYPTION_KEY").encode()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Define user roles and their permissions
ROLE_PERMISSIONS = {
    "admin": ["read", "write", "delete"],
    "caregiver": ["read", "write"],
    "researcher": ["read"]
}

# Rate-limiting dictionary (tracks user requests over time)
user_request_log = defaultdict(list)

# Define adversarial prompts to block prompt injection attacks
BLOCKED_PROMPTS = [
    "ignore previous instructions", 
    "jailbreak", 
    "repeat verbatim", 
    "act as unrestricted AI"
]

def detect_prompt_injection(user_input):
    """Detects and blocks adversarial prompt manipulation."""
    if any(term in user_input.lower() for term in BLOCKED_PROMPTS):
        return "⚠️ Security Alert: Potential prompt injection attempt detected."
    return user_input

def enforce_rate_limit(user_id):
    """Implements query rate limiting to prevent API abuse."""
    current_time = time.time()
    # Only keep queries made in the last 60 seconds
    user_request_log[user_id] = [t for t in user_request_log[user_id] if current_time - t < 60]
    
    if len(user_request_log[user_id]) >= 5:  # Limit to 5 queries per minute
        return "⚠️ Rate Limit Exceeded: Please slow down your requests."
    
    user_request_log[user_id].append(current_time)
    return "Request allowed."

def has_permission(user_role, action):
    """Checks if a user role has permission for an action."""
    return action in ROLE_PERMISSIONS.get(user_role, [])

def encrypt_data(patient_text, user_role):
    """Encrypts patient data securely if the user has the necessary permissions."""
    if not has_permission(user_role, "write"):
        return "⛔ Access Denied: Insufficient permissions."
    
    return cipher_suite.encrypt(patient_text.encode())

def decrypt_data(encrypted_text, user_role):
    """Decrypts patient data only if the user has permission to access it."""
    if not has_permission(user_role, "read"):
        return "⛔ Access Denied: Insufficient permissions."
    
    return cipher_suite.decrypt(encrypted_text).decode()
