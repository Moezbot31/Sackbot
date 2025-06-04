import hashlib
import os
import json

class AuthManager:
    def __init__(self, db_path='users.json'):
        self.db_path = db_path
        self.users = self._load_users()
        self.current_user = None

    def _load_users(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_users(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.users, f)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        if username in self.users:
            return False, 'User already exists.'
        self.users[username] = self.hash_password(password)
        self._save_users()
        return True, 'Registration successful.'

    def login(self, username, password):
        if username not in self.users:
            return False, 'User not found.'
        if self.users[username] != self.hash_password(password):
            return False, 'Incorrect password.'
        self.current_user = username
        return True, 'Login successful.'

    def logout(self):
        self.current_user = None

    def is_authenticated(self):
        return self.current_user is not None

    def recover_password(self, username, new_password):
        if username not in self.users:
            return False, 'User not found.'
        self.users[username] = self.hash_password(new_password)
        self._save_users()
        return True, 'Password reset successful.'

    def get_user_profile(self, username):
        if username not in self.users:
            return None
        return {'username': username}

if __name__ == "__main__":
    auth = AuthManager()
    print("Registering user: ", auth.register('alice', 'password123'))
    print("Logging in: ", auth.login('alice', 'password123'))
    print("Is authenticated? ", auth.is_authenticated())
    print("User profile: ", auth.get_user_profile('alice'))
    print("Password recovery: ", auth.recover_password('alice', 'newpass456'))
    print("Logging in with new password: ", auth.login('alice', 'newpass456'))
    print("Logout.")
    auth.logout()
    print("Is authenticated? ", auth.is_authenticated())
