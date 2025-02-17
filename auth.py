authorized_users = {"nurse_anna": "password123", "dr_smith": "securepass"}

def authenticate(user, password):
    if user in authorized_users and authorized_users[user] == password:
        return "Access granted"
    return "Access denied"
