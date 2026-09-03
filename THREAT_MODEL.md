# Threat Model

Protects users' passwords by hashing them and making the cost of deriving the original password from the hash very expensive for the attacker.

# Attacker
The primary attacker is the person who gets unauthorized read access to the database or a database backup containing the password hashes.

# Attacker Capabilities
If the attacker has the database, they can:
  Obtain password hashes
  Copy them
  Perform offline password-guessing attacks
  Use dictionaries
  Use lists of commonly used passwords
  Attempt brute-force guesses
  Run those guesses against the stolen hashes without interacting with your server
  The attacker can perform these password guesses offline without triggering application-level rate limits.

# Defenses
  ## Database compromise
  ## Rainbow tables
  ## offline guessing

# Why Argon2
I chose Argon2 because of different settings for tuning the cost parameter and memory hardening.

Why Argon2id instead of bcrypt?
Why Argon2id instead of scrypt?
Why Argon2id instead of PBKDF2?

# The Argon2 parameters — m=65536 means 64 MiB per hash, which caps a 24GB GPU at roughly 375 concurrent attempts instead of billions.
# The length policy — 15 minimum, 64 maximum, citing NIST SP 800-63B Rev 4, and why no complexity rules.
# Corrupt stored hashes — uniform False to the caller, full detail in the logs.
# None in the hash column — fail fast, because it's a violated invariant rather than a user error.

# Pepper
A pepper would add a layer of security in case a hacker got access to the hashes, because it is a global secret that is added to every password.
