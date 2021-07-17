from models.users.users import user_client

def print_user(user):
    print("Username: " + user["username"])
    print("Password: " + user["password"])
    print("Privileges: " + str(user["privileges"]))

def add():
    print("--- Adding a user ---")
    username = input("Username: ")
    password = input("Password: ")
    succ, user = user_client.add_user(username, password)
    if succ:
        print("Successfully added user '" + username + "'")
    else:
        print("Could not add user.")

def update():
    print("--- Updating a user ---")
    username = input("Username: ")
    succ, user = user_client.find_user(username)
    if succ:
        # Found user, commence
        print("Found user!\n")
        print_user(user)

        while True:
            action = input(f"update (addpriv/removepriv/viewtokens/checktoken/createtoken/exit) " + username + "> ")
            if "addpriv" in action:
                spl = action.split()[1]
                succ, newPrivUser = user_client.add_privilege(username, spl)
                print_user(newPrivUser)
            elif "removepriv" in action:
                spl = action.split()[1]
                succ, newPrivUser = user_client.remove_privilege(username, spl)
                print_user(newPrivUser)
            elif action == "exit":
                print("Goodbye.")
                break
            elif action == "viewtokens":
                tokens = user_client.get_all_tokens_for_user(username)
                print(tokens)
            elif action == "checktoken":
                token = input("token> ")
                succ, check = user_client.validate_token_for_user(username, token)
                print(succ, check)
            elif action == "createtoken":
                succ, tokens = user_client.create_token_for_user(username)
                print(succ, tokens)
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