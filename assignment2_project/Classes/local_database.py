"""Create database class for handling local database functions"""
import sqlite3

class LocalDatabase:
    """
    This module handles functions regarding the database.
    """

    def __init__(self, db_name="User.db"):
        self.__connection = sqlite3.connect(db_name)
        self.__cursor = self.__connection.cursor()

    def create_table(self):
        """Creates USERS database table if one doesn't already exist"""
        create_statement = """CREATE TABLE IF NOT EXISTS USERS (
            USERNAME TEXT,
            FN TEXT,
            LN TEXT,
            EMAIL TEXT,
            PASSWORD TEXT,
            USER_TYPE TEXT
        )"""
        self.__cursor.execute(create_statement)

    def insert_user(self, user_details):
        """
        Inserts a new user into the User database.

        Parameters:
            user_details (list of str): A list containing the details of a new user in the following
            format: [First Name, Lastname, Email, Password]
        """
        # Create database table if it doesn't already exist
        self.create_table()
        self.__cursor.execute(
            "INSERT into USERS (USERNAME, FN, LN, EMAIL, PASSWORD, USER_TYPE)" +
            "VALUES (:username, :fn, :ln, :email, :password, :userType)",
            {
                "username": user_details[0],
                "fn": user_details[1],
                "ln": user_details[2],
                "email": user_details[3],
                "password": user_details[4],
                "userType": user_details[5]
            }
        )
        self.__connection.commit()

    def read_db(self, query):
        """Used to search the database.

        Parameters:
            column (str): The name of the column to be searched.

            query (str): The SQL query for the desired information.

        Returns:
            str: Returns the results of the query.
        """
        # Create database table if it doesn't already exist
        self.create_table()
        rows = self.__cursor.execute(query)

        return rows.fetchone()

    def username_exist(self, username):
        """Check if the username already exists in the database.

        Parameters:
            username (str): The username to be checked.

            search (bool): Confirms/denies if the email exists in the database.

        Returns:
            bool: Returns True/False based on whether or not the email exists.
        """
        try:
            search = self.read_db(
                "SELECT USERNAME FROM USERS WHERE USERNAME = '{username}'".format(username=username)
            )

            return bool(search[0] == username)
        except IndexError:
            return False
        except TypeError:
            return False

    def email_exist(self, email):
        """Check if the email already exists in the database.

        Parameters:
            email (str): The email to be checked.

        Returns:
            bool: Returns True/False based on whether or not the email exists.
        """
        try:
            search = self.read_db(
                "SELECT EMAIL FROM USERS WHERE EMAIL = '{email}'".format(email=email)
            )

            return bool(search[0] == email)
        except IndexError:
            return False
        except TypeError:
            return False

    def get_password(self, username):
        """
        Get user's password for verification purposes.

        Parameters:
            username (str): Username of the user to retrieve password for

        Returns:
            (str): Returns the encrypted password for a particular user
        """
        return self.read_db(
            "SELECT PASSWORD FROM USERS WHERE USERNAME = '{username}'".format(username=username)
        )

    def get_user_name(self, username):
        """
        Get the user's first name by their username

        Parameters:
            username (str): Username of the user whose name we want to retrieve

        Returns:
            (str): First name of the user
        """
        return self.read_db(
            "SELECT FN FROM USERS WHERE USERNAME = '{username}'".format(username=username)
        )

    def get_user_email(self, username):
        """
        Get the user's email address by their username

        Parameters:
            username (str): Username of the user whose email we want to retrieve

        Returns:
            (str): Email address of the user
        """
        return self.read_db(
            "SELECT EMAIL FROM USERS WHERE USERNAME = '{username}'".format(username=username)
        )
