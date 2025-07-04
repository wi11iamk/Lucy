def prompt_security_filter(user_prompt):
    blocked_prompts = [
        "repeat previous response",
        "ignore all rules",
        "output everything",
    ]

    if any(term in user_prompt.lower() for term in blocked_prompts):
        return "Request denied due to security policies."
    return user_prompt
