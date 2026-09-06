from src.credentials import hash_password, verify_password
import pytest

def test_salts():
    password = "HelloWorld12345"
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)
    assert hashed1.startswith("$argon2id$")
    assert hashed2.startswith("$argon2id$")

    assert hashed1 != hashed2

def test_verify_accepts():
    password = "HelloWorld12345"
    hashed = hash_password(password)
    assert hashed.startswith("$argon2id$")

    assert verify_password(password, hashed) is True

def test_verify_rejects():
    password1 = "HelloWorld12345"
    password2 = "HelloWorld12346"
    hashed = hash_password(password1)
    assert hashed.startswith("$argon2id$")

    assert verify_password(password2, hashed) is False

def test_tampering_mismatch():
    password = "HelloWorld12345"
    hashed = hash_password(password)
    assert hashed.startswith("$argon2id$")

    prefix, separator, hash_part = hashed.rpartition("$")

    replacement = "c" if hash_part[5] != "c" else "d"
    tampered_hash = prefix + separator + hash_part[:5] + replacement + hash_part[6:]

    assert tampered_hash != hashed
    assert verify_password(password, tampered_hash) is False

def test_invalid_hash():
    password = "HelloWorld12345"
    invalid_hash = "this-is-not-a-valid-argon2-hash"

    assert verify_password(password, invalid_hash) is False

def test_minpassword():
    password = "Hidghniutvaskl"
    with pytest.raises(ValueError, match="Password is below the minimum length of 15 characters"):
        hash_password(password)

def test_maxpassword():
    password = "hefgakefbfaefageavefjgaeakvgesksvfhvwskjvfkjwavfjkwvfagfkavjhvwal"
    with pytest.raises(ValueError, match="Password exceeds 64 characters"):
        hash_password(password)