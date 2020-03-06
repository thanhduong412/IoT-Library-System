"""Creates Menu class to display user login/registration menu"""
import getpass
from Classes.password_encryption import PasswordEncryption
from Classes.local_database import LocalDatabase
from Classes.input_verification import InputVerification
from Classes.socket_connection import SocketConnection
from Classes.facial_recognition import FacialRecognition

class Menu:

    """
    This class handles all the menu functions for login/registration of a user.
    """

    def __init__(self):
        self.__encrypt = PasswordEncryption()
        self.__db = LocalDatabase()
        self.__validate = InputVerification()
        self.__socket = SocketConnection()
        self.__face = FacialRecognition()


    def main_menu(self):
        """
        Prints the main menu to the console and depending on the user's choice sends them to
        the relevant menu or exits the program.
        """
        while True:
            print("\nWelcome!")
            print("\n 1. Login")
            print("\n 2. Register as a new user")
            print("\n 3. Register facial recognition to account")
            print("\n 4. Quit")
            user_input = input("\nPlease select from the list above: ")

            if user_input == "1":
                print("\n1. Login via username and password")
                print("\n2. Login via facial recognition")
                user_input = input("\nPlease select from the list above: ")
                if user_input == "1":
                    self.login_menu()
                    break
                elif user_input == "2":
                    user_face = self.__face.face_scan()
                    self.__socket.reception_connecting(user_face)
                    break
                else:
                    print("\n Invalid Input - Must be an integer from 1-3.")
                break
            elif user_input == "2":
                self.register_menu()
            elif user_input == "3":
                self.face_menu()
            elif user_input == "4":
                print("\nGoodbye!")
                break
            else:
                print("\n Invalid Input - Must be an integer from 1-3.")

    def login_menu(self):
        """
        Takes the user input and verifies them. Once verified, the user is logged into the
        application.
        """
        while True:
            username_value = input("\nUsername: ")
            pw_value = getpass.getpass("\nPassword: ")
            user_detail = [username_value, pw_value]
            user_valid = self.__validate.username_valid(username_value)

            if user_valid:
                user_exist = self.__db.username_exist(user_detail[0])
                pw_exist = self.__encrypt.verify(user_detail)
            else:
                user_exist = False
                pw_exist = False

            if not user_exist or not pw_exist:
                print(
                    "User/Password is incorrect." +
                    " Please ensure you are entering the correct details."
                )
            elif user_exist and pw_exist:
                print("\nLogin successful.")
                self.__socket.reception_connecting(user_detail[0])
                break

    def register_menu(self):
        """
        Requests a number of details from the user in order to create a new entry in the database.
        """
        while True:
            print("\nPlease fill in the following details:")
            username = self.verify_username()
            first_name = self.verify_fn()
            last_name = self.verify_ln()
            email = self.verify_email()
            pw_input = self.verify_password()
            pw_hashed = self.__encrypt.encrypt(pw_input)
            user_detail = [
                username,
                first_name,
                last_name,
                email,
                pw_hashed,
                "USER"
            ]
            self.__db.insert_user(user_detail)
            print("\nUser '{}' created! Feel free to login.".format(username))
            break

    def verify_username(self):
        """Check that username does not already exist or is invalid"""
        while True:
            username_input = input("\nUsername: ")
            username_valid = self.__validate.username_valid(username_input)

            if username_valid:
                if self.__db.username_exist(username_input):
                    print("Error: Username already in use.")
                else:
                    return username_input
            else:
                print(
                    "Error: Do not put any special characters in your username." +
                    " '.', '_', '-' are allowed."
                )

    def verify_fn(self):
        """Check that first name is valid"""
        while True:
            fn_input = input("\nFirst Name: ")
            fn_valid = self.__validate.name_valid(fn_input)
            if fn_valid:
                return fn_input
            print("Error: Do not put any special characters in your name")

    def verify_ln(self):
        """Check that last name is valid"""
        while True:
            ln_input = input("\nLast Name: ")
            ln_valid = self.__validate.name_valid(ln_input)
            if ln_valid:
                return ln_input
            print("Error: Do not put any special characters in your name")

    def verify_email(self):
        """Check that does not exist already and is valid"""
        while True:
            email_input = input("\nEmail: ")
            email_repeat = input("\nRe-enter Email: ")
            if email_input == email_repeat:
                email_valid = self.__validate.email_valid(email_input)

                if email_valid:
                    if self.__db.email_exist(email_input):
                        print("Error: Email already in use.")
                    else:
                        return email_input
                else:
                    print("\nError: Email needs to be a gmail account.")
            else:
                print(
                    "\nError: Emails do not match. Please enter the same email twice.")

    def verify_password(self):
        """Check that password is valid"""
        while True:
            pw_input = getpass.getpass("\nPassword: ")
            pw_repeat = getpass.getpass("\nRe-enter Password: ")
            if pw_input == pw_repeat:
                pw_validation = self.__validate.pw_valid(pw_input)

                if pw_validation:
                    return pw_input
                print(
                    "\nError: Passwords should at least have one capital and number in "
                    "it. Minimum 8 character length."
                )
            else:
                print(
                    "\nError: Passwords do not match. Please enter the same password twice.")

    def face_menu(self):
        """Shows facial recognition registration menu"""
        while True:
            username_value = input("\nUsername: ")
            pw_value = getpass.getpass("\nPassword: ")
            user_detail = [username_value, pw_value]
            user_valid = self.__validate.username_valid(username_value)

            if user_valid:
                user_exist = self.__db.username_exist(user_detail[0])
                pw_exist = self.__encrypt.verify(user_detail)
            else:
                user_exist = False
                pw_exist = False

            if not user_exist or not pw_exist:
                print(
                    "User/Password is incorrect." +
                    " Please ensure you are entering the correct details."
                )
            elif user_exist and pw_exist:
                print("\nLogin successful.")
                self.__face.register_face(user_detail[0])
                break
