import hashlib
import getpass

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def decrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.decode()).hexdigest()
    return sha_signature

code = getpass.getpass('Password:')
enkripsi = encrypt_string(code)
print(enkripsi)
