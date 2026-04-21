import json
import hashlib

FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f, indent=4)

def register(username, password):
    users = load_users()

    if username in users:
        return False, "Username đã tồn tại"

    users[username] = {
        "password": hash_password(password),
        "level": 1,
        "points": 0
    }

    save_users(users)
    return True, "Đăng ký thành công"

def login(username, password):
    users = load_users()

    if username not in users:
        return False, "no_user"

    if users[username]["password"] != hash_password(password):
        return False, "wrong_pass"

    return True, users[username]

def update_user(username, data):
    users = load_users()
    users[username].update(data)
    save_users(users)