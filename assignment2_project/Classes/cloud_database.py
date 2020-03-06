"""Creates CloudDatabase class"""
import datetime
import json
import sys
# Disable linting error that package is not found locally
# pylint: disable=E0401
import MySQLdb
sys.path.append("..")

class CloudDatabase:
    """Connects to the Google Cloud SQL database and handles associated functions"""
    def __init__(self, connection=None):
        with open("config.json", "r") as file:
            config = json.load(file)
        self.__host = config["cloud_host"]
        self.__user = config["cloud_user"]
        self.__password = config["cloud_password"]
        self.__database = config["cloud_database"]

        if connection is None:
            connection = MySQLdb.connect(
                self.__host,
                self.__user,
                self.__password,
                self.__database
            )
        self.__connection = connection

    def close(self):
        """Close database connection"""
        self.__connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def create_user(self, username, name):
        """
        Creates a user record if the username does not already exist

        Parameters:
            username (str): Username
            name (str): Name
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO LmsUser (UserName, Name) VALUES ('" + username + "', '" + name + "')"
            )
        self.__connection.commit()

    def get_user_id(self, username, name):
        """Gets the currently logged in user's ID"""
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "SELECT LmsUserID FROM LmsUser WHERE UserName = '" + username + "'"
            )
            user_id = cursor.fetchone()

        # Checks if the user exists and gets their ID
        if user_id:
            return user_id

        # Create the new user if they do not and then get their new ID
        self.create_user(username, name)
        return self.get_user_id(username, name)

    def get_borrowed_books(self, user_id):
        """
        Checks for all books that the user has borrowed

        Parameters:
            user_id (str): ID of the logged in user

        Returns:
            All books that the user has borrowed at the moment
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "SELECT BookBorrowed.BookID, Book.Title, Book.Author FROM BookBorrowed " +
                "INNER JOIN Book ON BookBorrowed.BookID = Book.BookID " +
                "WHERE BookBorrowed.LmsUserID = " + str(user_id) +
                " AND BookBorrowed.Status = 'borrowed'"
            )
            return cursor.fetchall()

    def get_book(self, usr_in=""):
        """
        Returns a matching book from the database

        Parameters:
            usr_in (str): Search terms for a book (title/author)

        Returns:
            All matching books from the search query that have not been borrowed
        """
        with self.__connection.cursor() as cursor:
            # Get IDs of borrowed books
            cursor.execute(
                "SELECT BookID FROM BookBorrowed " +
                "WHERE Status = 'borrowed'"
            )
            borrowed_books = cursor.fetchall()
            borrowed_ids = list()
            for book in borrowed_books:
                borrowed_ids.append(str(book[0]))

            # Filter books by search input
            select_query = (
                "SELECT BookID, Title, Author FROM Book " +
                "WHERE (Title LIKE '%" + usr_in + "%' " +
                " OR Author LIKE '%" + usr_in + "%') "
            )

            # Exclude borrowed books if there are any
            if borrowed_ids:
                select_query += "AND BookID NOT IN (" + ','.join(borrowed_ids) + ")"

            cursor.execute(select_query)
            return cursor.fetchall()

    def borrow_book(self, user_id, book_id):
        """Inserts a record of a book being borrowed into BookBorrowed"""
        date = datetime.datetime.now()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO BookBorrowed (LmsUserID, BookID, Status, BorrowedDate) " +
                "VALUES (" +
                str(user_id) + ", " +
                str(book_id) + ", " +
                "'borrowed', '" +
                date.strftime('%Y-%m-%d %H:%M:%S') +
                "')"
            )
        self.__connection.commit()

    def return_book(self, user_id, book_id):
        """Update a borrowed book to returned"""
        date = datetime.datetime.now()
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "UPDATE BookBorrowed " +
                "SET Status = 'returned', " +
                "ReturnedDate = '" + date.strftime('%Y-%m-%d %H:%M:%S') +
                "' WHERE BookID = " + str(book_id) + " AND LmsUserID = " + str(user_id)
            )
        self.__connection.commit()
