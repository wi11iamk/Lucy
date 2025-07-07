# main.py
from auth import authenticate
from response_engine import generate_response_with_llm, log_interaction
from security import enforce_rate_limit, detect_prompt_injection
from safety_monitor import constitutional_safety_filter


def run_chat_flow(user: str, password: str, user_input: str) -> None:
    """End-to-end demo flow for one chat turn."""
    # 1️⃣ authenticate
    if authenticate(user, password) != "Access granted":
        print("Authentication failed.")
        return

    # 2️⃣ rate-limit
    if enforce_rate_limit(user) != "Request allowed.":
        print("⚠️  Rate limit hit — please wait a minute and try again.")
        return

    # 3️⃣ prompt-injection
    clean_input = detect_prompt_injection(user_input)
    if clean_input.startswith("⚠️ Security Alert"):
        print(clean_input)
        return

    # 4️⃣ LLM call
    llm_response, emotion_scores, prompt = generate_response_with_llm(clean_input)

    # 5️⃣ safety filter
    safe_response = constitutional_safety_filter(llm_response)

    # 6️⃣ log + display
    log_interaction(user_input, emotion_scores, prompt, safe_response)
    print("LLM Response:")
    print(safe_response)


def main() -> None:
    """Hard-coded demo credentials & prompt."""
    user = "nurse_anna"
    password = "password123"
    user_input = "I feel like I'm forgetting too much these days and it's really scary."
    run_chat_flow(user, password, user_input)

    
if __name__ == "__main__":
    main()