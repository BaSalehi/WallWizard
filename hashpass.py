import hashlib
import json
import os

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest() 


def check_password(username, password):
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            users = json.load(f)

        for user in users:
            if user['username'] == username:
                hashed_input_password = hash_password(password)
                if user['password'] == hashed_input_password:
                    return True
                else:
                    return False