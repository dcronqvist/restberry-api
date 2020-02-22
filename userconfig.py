import users as users

def add():
    print("--- Adding a user ---")
    username = input("Username: ")
    password = input("Password: ")
    succ, user = users.add_user(username, password)
    if succ:
        print("Successfully added user '" + username + "'")
    else:
        print("Could not add user.")

while True:
    print("----- Choose action (add/update/delete) -----")
    inpt = input("-> ")

    if inpt == "add":
        add()