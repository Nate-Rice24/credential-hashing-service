from argon2 import PasswordHasher

_hasher = PasswordHasher()

def hash_password(password):
    return _hasher.hash(password)

password = "Hi"

print(hash_password(password))