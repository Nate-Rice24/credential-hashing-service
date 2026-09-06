# Threat Model

The system protects users' passwords by hashing them with Argon2id, making the cost of offline guessing very computationally and memory expensive for the attacker who obtains the stored password hashes.

## Attacker
The primary threat actor is the attacker who gets unauthorized read access to the database or a database backup containing the password hashes.

## Attacker Capabilities
If the attacker obtains the database or a database backup, they can:

- Obtain password hashes.
- Copy the hashes for offline analysis.
- Perform offline password-guessing attacks.
- Use dictionary and common-password lists.
- Attempt brute-force attacks.
- Perform guesses without interacting with the application or triggering application-level rate limits.

## Defenses
### Database compromise
For database compromises, the system stores the users' hashed passwords in the system, so if the database is compromised, the attacker must perform password guessing against the hashes rather than immediately obtaining the plain-text passwords. The system uses unique salts and Argon2id's configurable cost parameters to increase the cost of this attack.
### Rainbow tables
For rainbow tables, the program uses a unique random salt for each password. This means that two identical passwords can have different hashes, making rainbow tables impractical.
### Offline guessing
For offline guessing, the program has many different cost parameters that harden the memory and increase the computational and memory cost of each password. This won't prevent offline guessing, but it can increase the resources required to perform large numbers of guesses.
## Why Argon2id
I chose Argon2 because it provides configurable time, memory, and parallelism costs, allowing the password-hashing workload to be tuned to make offline attacks more expensive.

### Argon2id vs. bcrypt?
I chose Argon2id over bcrypt because bcrypt lacks explicit memory-hardening parameters you can tune, and it has a built-in maximum password length of 72 bytes. Not only does Argon2id have cost parameters you can tune, but it also doesn't have a required maximum password length. Overall, I chose Argon2id over bcrypt because of its flexibility to change and  tune the hashing to how I see fit. 
  
### Argon2id vs. scrypt?
I chose Argon2id over scrypt because, while scrypt does have memory-hardening features and is a strong password-hashing algorithm. Argon2id has more design/configurability options for memory hardening and side-channel resistance. For this project, Argon2id provides the combination of properties I wanted.
  
### Argon2id vs. PBKDF2?
I chose Argon2id over PBKDF2 because PBKDF2's primary cost parameter is increasing the number of iterations and does not provide the same configurable memory-cost parameter as Argon2id

### The Argon2id parameters
| Parameter         |     Value | Purpose                           |
| ----------------- | --------: | --------------------------------- |
| Memory (`m`)      | 65536 KiB | Controls memory used by each hash |
| Time (`t`)        |         3 | Controls the number of passes     |
| Parallelism (`p`) |         4 | Controls parallelism              |
As a simplified memory-only illustration, 24 GB / 64 MiB is approximately 375 concurrent 64 MiB allocations. Actual password-cracking performance depends on the GPU architecture, implementation, parallelism, memory overhead, and other Argon2id parameters.
# In this system, I imposed

### Password Policy
In this system, I imposed a 15-character minimum and 64-character maximum as part of its password policy. The length policy — 15 minimum, 64 maximum- follows NIST SP 800-63B Rev 4 guidelines, and there are no complexity rules.
### Error Handling
Corrupt stored hashes — uniform False to the caller, full detail in the logs. This prevents the API from giving away unnecessary internal details while allowing operators to investigate the problem.
None in the hash column — fail fast, because it's a violated invariant rather than a user error. This is important because it fails fast and loud, allowing for the problem to be fixed right away instead of going under the radar for a while.

## Salt VS Pepper
A salt is public and stored with the hash; a pepper is secret and stored separately. A pepper would add a layer of security in case a hacker got access to the hashes, because it is a global secret that is added to every password. The pepper would be stored separately from the database in a secure place, so that even if the attacker got the hash from the database, they would still be missing the pepper.

## Out Of Scope
### Compromised Application
If the attacker has access to the application server, they could potentially capture the password before it gets hashed.

### Malware/Keyloggers
If the user's device is compromised, the password could be captured before it reaches the application.

### Weak Passwords
Argon2id just makes the guessing more expensive. It won't actually make weak passwords stronger.

### Denial Of Service
The system intentionally uses computational and memory resources for hashing. An attacker could potentially consume these resources by abusing the password-hashing endpoint.

### Phishing
This system does not protect against a user voluntarily giving their password to someone.

## Security Assumptions
This threat model assumes that the attacker has access to the stored password hashes but does not have access to the application's secret values or the ability to directly observe passwords before hashing.

## References

- [NIST SP 800-63B: Digital Identity Guidelines — Authentication and Lifecycle Management, Revision 4](...)

## Summary

The primary threat addressed by this project is offline password cracking following a database compromise. Argon2id, unique salts, and configurable memory and computational costs increase the resources required to perform password guesses. This design does not protect against attacks that compromise the application, the user's device, or the user's behavior.
