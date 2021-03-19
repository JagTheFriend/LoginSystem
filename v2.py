import json
import time
from getpass import getpass

DB = "v2_db.json"


class Main(object):
    def __init__(self):
        """
        Loads the data from the database
        :return: Function
        """
        self.login_attempts: int = 1
        with open(DB, "r") as file:
            self.data: dict = json.load(file)

        self.signup_login()

    def signup_login(self) -> ():
        """
        Asks whether the user wants to be signed up or login
        :return: Function
        """
        print("1) Login \n2) Sign Up")
        number: int = int(input("Please enter a number: "))
        self.login_attempts = 0  # rest the login attempts
        return self.login() if number == 1 \
            else self.signup() if number == 2 \
            else f"Please enter a valid number! {self.signup_or_login()}"

    def signup(self) -> ():
        """
        Allows user to signup
        :return: Function
        """
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

    def __save_data(self, signup: bool = True) -> None:
        """
        Saves the changed data
        :param signup: Boolean
        """
        if signup:
            self.data[self.user_name]: dict = {}
            self.data[self.user_name]["password"]: str = self.user_password
            self.data[self.user_name]["notes"]: [str] = []
        with open(DB, "w") as file:
            return json.dump(self.data, file, indent=4)

    def login(self) -> ():
        """
        Gets the username and password
        To check whether it is a valid user or not
        :return: Function
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
        :return: Boolean
        """
        return (
            self.user_name in self.data.keys() and
            self.user_password == self.data[self.user_name]["password"]
        )

    def notes(self) -> ():
        """
        Asks whether the user want to:
            + make new notes
            + view previously made notes
            + edit previously made notes
        :return: Function
        """
        print("\nWould you like to")
        print("1) See your notes")
        print("2) Enter new notes")
        print("3) Edit notes")
        notes = str(input("Enter the correct number: "))

        for e, i in zip(
                        ["1", "2", "3"],
                        ["self.see_notes()",
                         "self.new_notes()",
                         "self.edit_notes()"
                         ]  # TODO backspace before deployment
                    ):
            if notes == e:  # a valid number is given
                return eval(i)

        # a invalid number is not given
        print("Please enter a valid number! \n")
        return self.notes()

    def see_notes(self) -> ():
        """
        Allows the user to see the previously made notes
        :return: Function
        """
        print("\nYour notes: ")
        print("\n\n".join(self.data[self.user_name]["notes"]))
        return self.notes()

    def new_notes(self) -> ():
        """
        Allows the user to create new notes
        :return: Function
        """
        print("\nPress `enter` 2 times, if you want to stop entering notes\n")
        notes = '\n'.join(iter(input, ''))  # getting userinput
        # saving the data
        current_time = time.ctime(time.time(()))
        self.data[self.user_name]["notes"].append(
            f"{current_time}: {notes}"
        )
        print("\nYou notes has been saved!\n")
        self.__save_data(False)
        return self.notes()

    def edit_notes(self) -> ():
        """
        Allows user to edit notes
        :return: Function
        """
        notes: [str] = [f"{i[1]}" for i in self.data[self.user_name]["notes"]]
        index: [str] = list(map(
                    str, range(1, len(self.data[self.user_name]["notes"])+1)
                ))
        print("\nYou notes: ")
        for i in zip(index, notes):
            print(f"{i[0]} | {i[1]}")

        while True:
            number: str = str(input("Please enter a valid number: "))
            if number in index:  # check whether the number is a int
                break
            print("\nPlease enter a vaid number!!")

        print("\nPress `enter` 2 times, if you want to stop entering notes\n")
        # getting userinput
        notes = '\n'.join(iter(input, ''))
        # saving the data
        current_time = time.ctime(time.time())
        self.data[self.user_name]["notes"][number] = f"{current_time}: {notes}"
        self.__save_data(False)
        return self.notes()


Main()
