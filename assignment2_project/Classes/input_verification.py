"""Creates class for handling input verification"""
import re


class InputVerification:
    """
    This module handles all the verification processes for the user inputs.
    """
    def __init__(self):
        pass

    @staticmethod
    def username_valid(username_input):
        """
        Takes the username entered by the user and check if it's valid.

        Parameters:
            username_input (str): Stores the username value entered by the user.

        Returns:
            bool: Returns True/False based on whether or not the username is valid.
        """
        username_regex = r"^[^!@#$%^&*'()\s]+$"
        username_valid = re.match(username_regex, username_input)

        return bool(username_valid)

    @staticmethod
    def email_valid(email_input):
        """
        Takes the email entered by the user and checks if it's valid.

        Parameters:
            email_input (str): Stores the email value entered by the user.

        Returns:
            bool: Returns True/False based on whether or not the email is valid.
        """
        email_regex = r".*\w@gmail.com"
        email_valid = re.match(email_regex, email_input)

        return bool(email_valid)

    @staticmethod
    def pw_valid(pw_input):
        """
        Takes the password entered by the user and checks if it's valid.

        Parameters:
            pw_input (str): Stores the password value entered by the user.

        Returns:
            bool: Returns True/False based on whether or not the password is valid.
        """
        pw_regex = r"^(?=.*[\d])(?=.*[A-Z])[\w\d@#$]{8,}"
        pw_valid = re.match(pw_regex, pw_input)

        return bool(pw_valid)

    @staticmethod
    def name_valid(name_input):
        """
        Takes either the first or last name value entered by the user and check if it's valid.

        Parameters:
            name_input (str): Stores either the first or last name value that the user entered.

        Returns:
            bool: Returns True/False based on whether or not the name is valid.
        """
        name_regex = r"^[\w]+$"
        name_valid = re.match(name_regex, name_input)

        return bool(name_valid)
