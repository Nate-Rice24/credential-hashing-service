# credential-hashing-service
![tests](https://github.com/Nate-Rice24/credential-hashing-service/actions/workflows/tests.yml/badge.svg)

## Problem
A database breach can expose password hashes, allowing an attacker to perform unlimited offline guesses. This project uses Argon2id to make the hashing operation memory-hard, increasing the computational and memory cost of offline guessing.
  
## Design

### Password Hashing
The resulting Argon2id encoded hash includes a unique random salt. Because identical passwords receive different salts, they produce different stored hashes, making precomputed rainbow tables impractical.
### Password Verification
Password verification takes in the input password and the hashed password from the database and then uses Argon2id's built-in verify function, which uses the information encoded in the stored Argon2id hash to perform verification.
### Password Policy
For the password policy, I based this policy on NIST guidance and decided to set the minimum password length to 15 characters and the maximum password length to 64 characters. I also didn't require any special characters, as arbitrary complexity requirements don't necessarily make passwords stronger and can make them harder for the user to remember.
### Error Handling
For error handling, the system raises ValueError when the input password isn't within the required character length. Then, for verifying the password, I handled mismatch errors and invalid hashes on the back end, so that internal error details aren't unnecessarily exposed to callers.
  
## Tradeoffs

### Security vs. Performance
In order to implement security against certain attacks, these security improvements come with a performance cost. One example of this is the cost parameters that I have included to slow down and limit offline guessing. These parameters would slow down the login process for the user. So I chose parameters that provide meaningful resistance to offline guessing while keeping legitimate password verification responsive.
### Password Length
The major trade-off here is that the shorter the password, the easier it is to guess, and hashing can't make up for a bad password. So I tried to make the minimum password length long enough to be secure without unnecessarily burdening users.
### Pepper
Adding a pepper provides another layer of protection, but introduces secret-management requirements because the pepper must be stored separately from the database. This doesn't, however, protect against the attacker controlling the environment running the application.

## How To Run

### Clone the repository

```bash
git clone <repository-url>
cd credential-hashing-service
python -m venv .venv

#Activate for Windows
.venv\Scripts\activate

#Activate for Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m pytest
```


## Tests

The project includes tests covering:

- Successful password verification
- Incorrect passwords
- Invalid/malformed hashes
- Password length requirements
- Hash uniqueness due to unique salts
- Tampered hashes
- Invalid stored values

## What's Next
I would like to add:
- **Hash migration:** As hardware improves, Argon2id parameters may need to increase. A future version could detect outdated parameters during authentication and transparently rehash the password using the newer configuration.
- **Containerize the Service:** Package the application and its dependencies into a reproducible container to simplify deployment, improve environment consistency, and make the service easier to run in CI and production.
- **Managed pepper:** Store a secret pepper outside the database using environment-based secret injection or a dedicated secret manager. This would provide additional protection against database-only compromise while introducing additional secret-management requirements.

## Security

For a detailed analysis of the attacker model, security assumptions, defenses, and out-of-scope threats, see [THREAT_MODEL.md](THREAT_MODEL.md).
