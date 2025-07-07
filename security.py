import os
import time
import datetime
from collections import defaultdict
from cryptography.fernet import Fernet
from db.session import SessionLocal
from db.models import RateLimitWindow

from dotenv import load_dotenv

load_dotenv()

# Load encryption key securely from environment variables
key = os.getenv("LUCY_ENCRYPTION_KEY")
if not key:
    raise RuntimeError(
        "⚠️ LUCY_ENCRYPTION_KEY environment variable not set."
        "Define it in your shell, .env file, or CI configuration."
    )

ENCRYPTION_KEY = key.encode()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Define user roles and their permissions
ROLE_PERMISSIONS = {
    "admin": ["read", "write", "delete"],
    "caregiver": ["read", "write"],
    "researcher": ["read"],
}

# Rate-limiting dictionary (tracks user requests over time)
user_request_log = defaultdict(list)

# Define adversarial prompts to block prompt injection attacks
BLOCKED_PROMPTS = [
    "ignore previous instructions",
    "jailbreak",
    "repeat verbatim",
    "act as unrestricted AI",
]


def detect_prompt_injection(user_input):
    """Detects and blocks adversarial prompt manipulation."""
    if any(term in user_input.lower() for term in BLOCKED_PROMPTS):
        return "⚠️ Security Alert: Potential prompt injection attempt detected."
    return user_input


def enforce_rate_limit(user_id: str, limit: int = 5):
    now = time.time()
    with SessionLocal() as db:
        win = db.get(RateLimitWindow, user_id)
        if not win or now > win.window_end.timestamp():
            win = RateLimitWindow(
                user_id=user_id,
                request_cnt=1,
                window_end=datetime.datetime.fromtimestamp(
                    now + 60, tz=datetime.timezone.utc
                ),
            )
            db.merge(win)
            db.commit()
            return "Request allowed."
        if win.request_cnt >= limit:
            return "⚠️ Rate Limit Exceeded: Please slow down."
        win.request_cnt += 1
        db.commit()
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
