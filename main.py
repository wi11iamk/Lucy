from response_engine import dementia_friendly_response
from speech_analysis import analyze_speech_patterns
from safety_monitor import constitutional_safety_filter
from security import encrypt_data, decrypt_data
from auth import authenticate

user = "nurse_anna"
password = "password123"

if authenticate(user, password) == "Access granted":
    user_input = "I feel like I'm forgetting too much these days."
    
    ai_response = dementia_friendly_response(user_input)
    speech_report = analyze_speech_patterns(user_input)
    safe_response = constitutional_safety_filter(ai_response)
    
    encrypted_log = encrypt_data(f"Patient Input: {user_input} | AI Response: {safe_response}")
    
    print(f"AI Response: {safe_response}")
    print(f"Cognitive Report: {speech_report}")
    print(f"Encrypted Log: {encrypted_log}")
else:
    print("Authentication Failed.")
