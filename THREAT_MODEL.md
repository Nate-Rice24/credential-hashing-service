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
    For database compromises, the system stores the users' hashed passwords in the system, so if the database is compromised, the attacker still doesn't know what the actual passwords are. Then the system uses salts and cost parameters to make the original passwords more costly and slower to derive from the hashes.
  ## Rainbow tables
    For rainbow tables, the program uses salts, which are uniquely assigned hashes to each user, so an attacker can't guess users' passwords correctly because each user has a unique salt, basically making rainbow tables useless.
  ## offline guessing
    For offline guessing, the program has many different cost parameters that harden the memory and make offline guessing way slower. This won't prevent the attack, but it can slow it down enough that an attacker might give up because of how much slower these cost parameters make guessing.
# Why Argon2
I chose Argon2 because of different settings for tuning the cost parameter and memory hardening.

Why Argon2id instead of bcrypt?
  I chose Argon2id over bcrypt because bcrypt lacks explicit memory-hardening parameters you can tune, and it has a built-in maximum password length. Not only does Argon2id have cost parameters you can tune, but it also allows the programmer to hard-code a minimum and maximum password length. Overall, I chose Argon2id over bcrypt because of its flexibility to change and  tune the hashing to how I see fit. 
  
Why Argon2id instead of scrypt?
  I chose Argon2id over scrypt because, while scrypt does have memory-hardening features, I have found that Argon2id has a more comprehensive handle on memory hardening and side-channel resistance. For example, 
Why Argon2id instead of PBKDF2?

# The Argon2 parameters — m=65536 means 64 MiB per hash, which caps a 24GB GPU at roughly 375 concurrent attempts instead of billions.
# The length policy — 15 minimum, 64 maximum, citing NIST SP 800-63B Rev 4, and why no complexity rules.
# Corrupt stored hashes — uniform False to the caller, full detail in the logs.
# None in the hash column — fail fast, because it's a violated invariant rather than a user error.

# Pepper
A pepper would add a layer of security in case a hacker got access to the hashes, because it is a global secret that is added to every password.
