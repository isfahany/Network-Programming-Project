account = {}
status = ""
try:
    def displayMenu():
        print("Welome to the FTP room!!!")
        status = input("Are you registered? yes/no? || Press a to login as anonymous: ")
        if status == "yes":
            oldAccount()
        elif status == "no":
            newAccount()
        elif status == "a":
            print("Login as anonymous")
            home()
        
    def newAccount():
        username = input("Create username: ")      
        if username in account:
            print("Username already exist!\n")
        else:
            Password = input("Create password: ")
            account[username] = Password
            print("Account created\n")

    def oldAccount():
        login = input("Username: ")
        passwd = input("Password: ")
        if login in account and account[login] == passwd:
            print("Login successful!\n")
            home()
        else:
            print("User doesn't exist or wrong password!\n")

    def home():
        print("Welcome Master!!!\n")
        print("Please choose your waifu")
    
    while status != "exit":
        displayMenu()

except KeyboardInterrupt:
        print("Shut Down")
        
