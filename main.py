from response_engine import generate_response_with_llm, log_interaction
from auth import authenticate  # from your earlier auth.py
from config import AUTHORIZED_USERS  # Use the centralized credentials from config

# Example user credentials (in a real system, these would come from a secure input mechanism)
user = "nurse_anna"
password = "password123"

if authenticate(user, password) == "Access granted":
    user_input = "I feel like I'm forgetting too much these days and it's really scary."
    
    # Generate the response using our enhanced LLM response engine
    llm_response, emotion_scores, prompt = generate_response_with_llm(user_input)
    
    # Log the interaction (if logging is enabled in your project)
    log_interaction(user_input, emotion_scores, prompt, llm_response)
    
    print("LLM Response:")
    print(llm_response)
else:
    print("Authentication Failed.")
