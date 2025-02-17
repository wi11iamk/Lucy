from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(patient_text):
    return cipher_suite.encrypt(patient_text.encode())

def decrypt_data(encrypted_text):
    return cipher_suite.decrypt(encrypted_text).decode()
