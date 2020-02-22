import users as users

def print_user(user):
    print("Username: " + user["username"])
    print("Password: " + user["password"])
    print("Privileges: " + str(user["privileges"]))

def add():
    print("--- Adding a user ---")
    username = input("Username: ")
    password = input("Password: ")
    succ, user = users.add_user(username, password)
    if succ:
        print("Successfully added user '" + username + "'")
    else:
        print("Could not add user.")

def update():
    print("--- Updating a user ---")
    username = input("Username: ")
    succ, user = users.find_user(username)
    if succ:
        # Found user, commence
        print("Found user!\n")
        print_user(user)

        while True:
            action = input("update " + username + "> ")
            if "addpriv" in action:
                spl = action.split()[1]
                succ, newPrivUser = users.add_privilege(username, spl)
                print_user(newPrivUser)
            elif "removepriv" in action:
                spl = action.split()[1]
                succ, newPrivUser = users.remove_privilege(username, spl)
                print_user(newPrivUser)
            elif action == "exit":
                print("Goodbye.")
                break
            else:
                print("invalid command. try again.")
    else:
        # Did not find user, exit.
        print("No such user.")

while True:
    print("----- Choose action (add/update/delete/exit) -----")
    inpt = input("-> ")

    if inpt == "add":
        add()
    elif inpt == "update":
        update()
    elif inpt == "exit":
        print("Goodbye.")
        break