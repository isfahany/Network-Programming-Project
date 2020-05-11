import hashlib
import getpass

def encrypt_string(hash_string):
    enc = hashlib.sha256(hash_string.encode()).hexdigest()
    return enc

def login():
    username = input("Username: ")
    password = getpass.getpass('Password: ')
    password = encrypt_string(password)
    for line in open("accountfile.txt","r"): # Read the lines
        login_info = line.split(':')
        if username == login_info[0] and password == login_info[1]:
            print("Correct credentials!")
            print(login_info)
            return True
    print("Incorrect credentials.")
    return False

while True:
    login()