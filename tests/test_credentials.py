from src.credentials import hash_password, verify_password
import pytest

def test_salts():
    password = "HelloWorld12345"
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)

    assert hashed1 != hashed2

def test_verify_accepts():
    password = "HelloWorld12345"
    hashed = hash_password(password)

    assert verify_password(password, hashed) == True

def test_verify_rejects():
    password1 = "HelloWorld12345"
    password2 = "HelloWorld12346"
    hashed = hash_password(password1)

    assert verify_password(password2, hashed) == False

def test_tampering_mismattch():
    password = "HelloWorld12345"
    hashed = hash_password(password)
    hashed = hashed[:5] + 'c' + hashed[:6]

    assert verify_password(password, hashed) == False

def test_tampering_invalidhash():
    password = "HelloWorld12345"
    hashed = hash_password(password)
    hashed = hashed[:9] + 'c' + hashed[:10]

    assert verify_password(password, hashed) == False

def test_minpassword():
    password = "Hi"
    with pytest.raises(ValueError, match="Password is below the minimum length of 15 characters"):
        hash_password(password)

def test_maxpassword():
    password = "hefgakefbfaefageavefjgaeakvgesksvfhvwskjvfkjwavfjkwvfagfkavjhvwaekalwhu"
    with pytest.raises(ValueError, match="Password exceeds 64 characters"):
        hash_password(password)