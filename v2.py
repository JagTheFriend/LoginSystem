import json
import time
from getpass import getpass

DB = "v2_db.json"


class Main(object):
    def __init__(self):
        self.login_attempts: int = 1
        with open(DB, "r") as file:
            self.data: dict = json.load(file)

        self.signup_login()

    def signup_or_login(function):
        """
        Asks whether the user wants to be signed up or login
        """
        def main_question(self):
            print("1) Login \n2) Sign Up")
            number: int = int(input("Please enter a number: "))
            self.login_attempts = 0  # rest the login attempts
            return self.login() \
                if number == 1 \
                else self.signup() if number == 2 \
                else f"Please enter a valid number! {self.signup_or_login()}"

        return main_question

    @signup_or_login
    def signup_login(self):
        pass

    def signup(self):
        self.user_name: str = str(input("Enter your username: "))
        # check whether user name is already registered
        if self.user_name in list(self.data.keys()):
            print(f"\nUsername: {self.user_name} is already registered!")
            return self.signup()

        self.user_password: str = str(input("Enter your password: "))
        # check whether user password is already registered
        if self.user_password in [
                self.data[i]["password"]
                for i in self.data.keys()
                ]:
            print(f"\nPassword: {self.user_password} is already registered!")
            return self.signup()

        self.__save_data()
        print("\nYou have successfully signed up!\n")
        return self.signup_login()

    def __save_data(self, signup: bool = False):
        if not signup:
            self.data[self.user_name]: dict = {}
            self.data[self.user_name]["password"]: str = self.user_password
            self.data[self.user_name]["notes"]: [str] = []
        with open(DB, "w") as file:
            return json.dump(self.data, file, indent=4)

    def login(self):
        """
        Gets the username and password
        To check whether it is a valid user or not
        """
        self.user_name: str = str(input("Please enter your name: "))
        self.user_password: str = str(getpass("Please enter your password: "))

        if self.__login():
            return self.notes()

        # as long as more than 5 attempts isn't made,
        # the user can keep retrying
        if self.login_attempts < 5:
            print("\nInvalid username or password")
            print("Please try again\n")
            self.login_attempts += 1
            return self.login()

        return self.signup_or_login()

    def __login(self) -> bool:
        """
        Check if the user name and password are correct.
        """
        return (
            self.user_name in self.data.keys() and
            self.user_password == self.data[self.user_name]["password"]
        )

    def notes(self):
        print("\nWould you like to")
        print("1) See your notes")
        print("2) Enter new notes")
        notes = str(input("Enter the correct number: "))

        # if a number is not given
        if not notes.isdigit():
            print("\nPlease enter a number!!\n")
            return self.notes()

        for e, i in zip(["1", "2"], ["self.see_notes()", "self.new_notes()"]):
            if notes == e:
                return eval(i)

        print("Please enter a valid number! \n")
        return self.notes()

    def see_notes(self):
        print("\nYour notes: ")
        print("\n\n".join(self.data[self.user_name]["notes"]))
        return self.notes()

    def new_notes(self):
        print("\nPress enter 2x if you want to stop entering notes\n")
        notes = '\n'.join(iter(input, ''))  # getting userinput
        # saving the data
        current_time = time.ctime(time.time())
        self.data[self.user_name]["notes"].append(
            f"{current_time}: {notes}"
        )
        self.__save_data(True)
        return self.notes()


Main()
