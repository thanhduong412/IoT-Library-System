"""
Creates password encryption class
https://www.cyberciti.biz/python-tutorials/securely-hash-passwords-in-python/ 23/4
"""

# Disable package not found error when linting locally
# pylint: disable=E0401
from passlib.hash import pbkdf2_sha256
from Classes.local_database import LocalDatabase

class PasswordEncryption:
    """
    This module handles the encryption for the passwords.
    """
    def __init__(self):
        self.__db = LocalDatabase()

    @staticmethod
    def encrypt(password):
        """
        Takes in a password input and encrypts it.

        Parameters:
            password (str): A string storing the password value.

        Returns:
            str: Returns the encrypted password.
        """
        hashed = pbkdf2_sha256.encrypt(password, rounds=535000, salt_size=16)
        return hashed

    def verify(self, usr_details):
        """
        Searches the database for the password that matches the entered username, then, compares
        the two password values and returns True/False based on whether they match or not.

        Parameters:
            usr_details (list of str): List containing the entered username and password.

        Returns:
            bool: Returns True/False based on whether or not the password is correct.
        """
        try:
            username = usr_details[0]
            password = usr_details[1]

            hashed = self.__db.get_password(username)

            verify = pbkdf2_sha256.verify(password, hashed[0])
            return verify
        except IndexError:
            return False
        except TypeError:
            return False
