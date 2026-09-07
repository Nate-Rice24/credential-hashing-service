import logging
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError, InvalidHash

logger = logging.getLogger(__name__)

MAX_LENGTH = 64
MIN_LENGTH = 15
_hasher = PasswordHasher(
    time_cost=3,        
    memory_cost=65536,   
    parallelism=4,      
    hash_len=32,        
    salt_len=16,         
    type=Type.ID
)

def hash_password(password) -> str:
    if len(password) > MAX_LENGTH:
        raise ValueError("Password exceeds 64 characters")
    elif len(password) < MIN_LENGTH:
        raise ValueError("Password is below the minimum length of 15 characters")

    return _hasher.hash(password)


def verify_password(guess, stored_hash):
    try:
        _hasher.verify(stored_hash, guess)
        return True
    except VerifyMismatchError:
        return False
    except InvalidHash:
        logger.exception("Stored credential is not a valid Argon2 encoded hash")
        return False