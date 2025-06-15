import secrets
import string

# Generate a secure secret key
length = 32  # 32 bytes = 256 bits
characters = string.ascii_letters + string.digits + string.punctuation
secret_key = ''.join(secrets.choice(characters) for _ in range(length))

print("Here's your secure secret key for JWT authentication:")
print(secret_key)

# Save to a temporary file
with open('.secret_key.txt', 'w') as f:
    f.write(secret_key)

print("\nNote: Please copy this key and save it in a secure place.")
print("You'll need to add this as an environment variable in Render.")
