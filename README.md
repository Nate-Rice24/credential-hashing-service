![tests](https://github.com/Nate-Rice24/notes-app/actions/workflows/tests.yml/badge.svg)
# credential-hashing-service

## Problem
  A database breach can expose password hashes, allowing an attacker to perform unlimited offline guesses. This project uses Argon2id, making the hashing operation memory-hard and the offline guessing computationally and memory-wise expensive.
  
## Design

### Password Hashing
  For password hashing, the system takes a plain-text password and hashes it using Argon2id. Then the output is a hashed password containing a salt that is used to solve the problem of rainbow tables, since two identical passwords will have different hashes. Then this hash will be stored in a database.
### Password Verification
  Password verification takes in the input password and the hashed password from the database and then uses Argon2id's built-in verify function to verify that the hashes match. The library uses the information encoded in the stored Argon2id hash to perform verification.
### Password Policy
  For the password policy, I was informed by NIST guidance and decided to set the minimum password length to 15 characters and the maximum password length to 64 characters. I also didn't require any special characters as to not give information to give attackers of what characters might be in a user's password.
### Error Handling
  For error handling, I implemented value errors in case the input password isn't between the required byte lengths. Then, for verifying the password, I handled mismatch errors and invalid hashes on the back end, so that if there is an attacker, the errors don't give them any information about why the system errored.
## Tradeoffs

### Security vs. Performance
In order to implement security against certain attacks, the system's performance did suffer. One example of this is the cost parameters that I have included to slow down and limit offline guessing. These parameters would slow down the login process for the user, but I tried to find a happy medium between secure and still fast enough for the system to feel responsive.
### Argon2id vs. Other Algorithms
By choosing Argon2id, I did open up the possibility to fine-tune the system's cost parameters, but I gave up the speed and efficiency of other hashing services. 
### Password Length
While I did set the password length requirements at what I feel is pretty conservative, the major trade-off here is that the shorter the password, the easier it is to guess, and hashing can't make up for a bad password. So I tried to make the minimum password length long enough to be secure but not annoying for the user to remember or try to come up with.
### Pepper
Argon2id gave me the option to add peppers, which seem great for security, but add an extra layer, as the person/company using this service must find a separate safe space, besides the database where the hashes are stored, to store this global secret. This doesn't, however, protect against the attacker controlling the environment running the application.

## How To Run

### Clone the repository

``bash
git clone <repository-url>
cd credential-hashing-service
python -m venv .venv
Activate for Windows
.venv\Scripts\activate
Activate for Mac/Linux
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest

Obviously, **use the commands that actually match your repository**. Don't add commands for things you haven't implemented.

---

## 5. Tests
- successful password verification
- incorrect password
- invalid/malformed hash
- password length requirements
- hash uniqueness due to salts
- tampered hashes
- `None`/invalid stored values, if that's tested

And mention CI if your GitHub Actions workflow is working:

``markdown
Tests are also executed automatically through GitHub Actions CI.

## What's Next
I would like to add:
- Hash migration: As hardware improves, Argon2id parameters may need to increase. A future version could detect outdated parameters during authentication and transparently rehash the password using the newer configuration.
- Containerize the Service: Package the application and its dependencies into a reproducible container to simplify deployment, improve environment consistency, and make the service easier to run in CI and production.
- Add a pepper backed by environment variables or a secret manager: Additional protection against database-only compromise
