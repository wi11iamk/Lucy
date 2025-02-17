def constitutional_safety_filter(response):
    flagged_words = ["alone", "harm", "danger", "leave"]
    
    if any(word in response.lower() for word in flagged_words):
        return "Safety Warning: Response flagged for review."
    
    return response
