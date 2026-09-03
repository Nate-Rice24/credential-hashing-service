import logging
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError, InvalidHash

logger = logging.getLogger(__name__)

max_length = 64
min_length = 15
_hasher = PasswordHasher(
    time_cost=3,        
    memory_cost=65536,   
    parallelism=4,      
    hash_len=32,        
    salt_len=16,         
    type=Type.ID
)

def hash_password(password):

    if(len(password) > max_length):
        raise ValueError("Password exceeds 64 characters")
    elif(len(password) < min_length):
        raise ValueError("Password is below the minimum length of 15 characters")

    stored_hash = _hasher.hash(password)
    return stored_hash

def verify_password(guess, stored_hash):
    try:
        _hasher.verify(stored_hash, guess)
        return True
    except VerifyMismatchError:
        return False
    except InvalidHash:
        #log here in production
        logger.error("malformed stored hash encountered")
        return False

# The Argon2 parameters — m=65536 means 64 MiB per hash, which caps a 24GB GPU at roughly 375 concurrent attempts instead of billions.
# The length policy — 15 minimum, 64 maximum, citing NIST SP 800-63B Rev 4, and why no complexity rules.
# Corrupt stored hashes — uniform False to the caller, full detail in the logs.
# None in the hash column — fail fast, because it's a violated invariant rather than a user error.