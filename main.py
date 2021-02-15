"""
This piece of code was created by JagTheFriend
"""
import json
import getpass

db = "data.json"  # name of the database
with open(db, "r") as file:  # load the data into local variable
    users: {str: str} = json.load(file)


def menu() -> str:
    """This is menu, where user picks a letter"""

    # user makes their choice and enters a number
    return str(input("\nPlease enter \n1) To login \n2) To make a new account \n3) To quit \n:"))


def login():
    """Allows user to login"""

    # get password and username
    user_name = str(input("\nPlease enter username: "))
    password = getpass.getpass("Password: ")

    # check whether the user name is registered
    if not user_name in users.keys():
        print("\nInvalid username")
        return main()

    # check whether the password is valid
    if users[user_name] != password:
        print("\nInvalid password")

    print("\nYou have logged in")
    return main()


def register():
    """Allows users to get registered"""

    # get password and username
    user_name = str(input("\nEnter username: "))
    user_pass = str(input("Enter password: "))

    # check whether the password or user name is already not registered
    if user_name in users.keys() or user_pass in users.values():
        print(
            f"\nThe user name {user_name} is already registered or the \npassword {user_pass} is also already registered \n")
        return register()

    print("\nYou have been registered")
    globals()["users"][user_name] = user_pass
    return main()


def _save_data(user_data: {str: str}):
    """Saves the data"""

    with open(db, "w") as file:
        return json.dump(user_data, file, indent=4)


def main():
    """
    1) To login
    2) To make a new account
    3) To quit
    """

    choice = menu()
    if choice.isdigit():
        choice = int(choice)
        if choice == 3:
            _save_data(users)
            print("\nBye")
            return

        if choice == 2:
            return register()

        if choice == 1:
            return login()

    print("\nPlease enter a valid number")
    return menu()


main()
