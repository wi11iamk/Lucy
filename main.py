# main.py  (replace entire file)

import sys
from auth import authenticate
from response_engine import generate_response_with_llm, log_interaction

# 🔐 NEW imports
from security import (
    enforce_rate_limit,
    detect_prompt_injection,
)
from safety_monitor import constitutional_safety_filter

# --------------------------------------------------
# 1  Authenticate caller
user = "nurse_anna"
password = "password123"

if authenticate(user, password) != "Access granted":
    print("Authentication failed.")
    sys.exit()

user_id = user  # could be email / UUID in real app
user_input = "I feel like I'm forgetting too much these days and it's really scary."

# --------------------------------------------------
# 2  Rate-limit check
if enforce_rate_limit(user_id) != "Request allowed.":
    print("⚠️  Rate limit hit — please wait a minute and try again.")
    sys.exit()

# --------------------------------------------------
# 3  Prompt-injection guard
clean_input = detect_prompt_injection(user_input)
if clean_input.startswith("⚠️ Security Alert"):
    print(clean_input)  # prints the warning message
    sys.exit()

# --------------------------------------------------
# 4  Generate LLM response
llm_response, emotion_scores, prompt = generate_response_with_llm(clean_input)

# --------------------------------------------------
# 5  Constitutional safety filter on output
safe_response = constitutional_safety_filter(llm_response)

# --------------------------------------------------
# 6  Log + display
log_interaction(user_input, emotion_scores, prompt, safe_response)

print("LLM Response:")
print(safe_response)
