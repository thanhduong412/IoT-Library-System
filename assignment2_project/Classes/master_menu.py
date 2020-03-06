"""Creates MasterPi menu class"""
from Classes.cloud_database import CloudDatabase
from Classes.local_database import LocalDatabase
from Classes.qr_code import QR
from Classes.voice_text import VoiceText
from Classes.google_calendar import GoogleCalendar
# pylint: disable=R0903
class MasterMenu:
    """  This class handles the console application menu """
    def __init__(self, username):
        self.__db = CloudDatabase()
        self.__voice = VoiceText()
        self.__calendar = GoogleCalendar()
        self.__username = username
        self.__name = username
    # pylint: disable=R0912
    def menu(self):
        """
        This function handles the user interaction of the console application

        Parameters:
            user_id (str) = Currently logged in User.
        """
        # If the user doesn't exist, add them to the database
        user_id = self.__db.get_user_id(self.__username, self.__name)[0]
        # Set up Google Calendar account authorisation
        self.__calendar.set_up()

        while True:
            print("Welcome '{}'".format(self.__name))
            print()
            print("1. Search for and borrow a book")
            print("2. Return a book")
            print("3. Logout")
            print()

            text = input("Select an option: ")
            print()

            if text == "1":
                print("1. Search via typing")
                print("2. Search via voice command")
                print()
                text = input("Select an option: ")
                print()
                if text == "1":
                    self.search_book(user_id, "text")
                elif text == "2":
                    self.search_book(user_id, "voice")
                else:
                    break

            elif text == "2":
                borrowed_books = self.__db.get_borrowed_books(user_id)
                if borrowed_books:
                    print("1. Return book via QR code")
                    print("2. Return book via text")
                    print()
                    text = input("Select an option: ")
                    print()
                    if text == "1":
                        self.return_book(user_id, "qr")
                    elif text == "2":
                        self.return_book(user_id, "text")
                    else:
                        break
                else:
                    print("No books have been borrowed under this user.")
                    print()

            elif text == "3":
                break

            else:
                print("Invalid input, try again.")
                print()

    def search_book(self, user_id, action):
        """
        Search for a book using text

        Parameters:
            usr_id (int): ID of the user borrowing books
            action (str): Either "text" or "voice" for search term input method

        Returns:
            All matching books from the search query that have not been borrowed.
        """
        search = True
        while search:
            if action == "text":
                usr_in = input("What book are you searching for? ")
            elif action == "voice":
                usr_in = self.__voice.voice_to_text()

            matching_books = self.__db.get_book(usr_in)

            # Check if any matching books were returned in search
            if matching_books:
                print()
                print("--- Available Matching Books ---")
                print("{:<15} {:<80} {}".format("BookID", "Title", "Author"))

                for book in matching_books:
                    book_id = book[0]
                    title = book[1]
                    author = book[2]

                    print("{:<15} {:<80} {}".format(book_id, title, author))

                print()
                usr_in = input("Would you like to borrow a book (yes/no)? ")
                print()

                if usr_in == "yes":
                    self.borrow_book(user_id)
                    search = self.search_again(user_id)
                elif usr_in == "no":
                    search = self.search_again(user_id)
                    break
                else:
                    print("Invalid input")
                    print()

            else:
                print()
                print("No matching books returned.")
                print()
                # Search again since there were no results returned
                self.search_again(user_id)

    def search_again(self, user_id):
        """Check if the user wants to search again"""
        while True:
            search_again = input("Would you like to search again? (yes/no) ")
            print()

            if search_again == "yes":
                return True
            elif search_again == "no":
                return False
            else:
                print("Invalid input")
                print()

    def validate_book(self, book_id, user_id, action):
        """Checks whether a book ID is valid for borrowing/returning a book"""
        valid_ids = set()
        book_titles = dict()

        # Get books that are available for borrowing
        if action == "borrow":
            book_ids = self.__db.get_book()
        # Get books that the current user has already borrowed
        elif action == "return":
            book_ids = self.__db.get_borrowed_books(user_id)

        for book in book_ids:
            current_book_id = book[0]
            book_title = book[1]
            valid_ids.add(current_book_id)
            book_titles[current_book_id] = book_title

        # User inputted book_id is a string and needs to be converted to int
        # If the book_id is not a number, return empty string
        try:
            book_id = int(book_id)
        except ValueError:
            return ""

        # If the book ID is valid, return the book's title
        if book_id in valid_ids:
            return book_titles.get(book_id)

        # Otherwise, return an empty string
        return ""

    def borrow_book(self, user_id):
        """
        Select and borrow a book.

        Parameters:
            user_id (str): Currently logged in user

        Returns:
            The book will be borrowed by the user.
        """
        # Allow the user to keep borrowing until they type 'exit'
        while True:
            book_id = input(
                "Enter ID of the book you'd like to borrow or type 'exit' to stop borrowing: "
            )
            print()

            if book_id == "exit":
                break

            book_name = self.validate_book(book_id, user_id, "borrow")

            # Check if book is available for borrowing
            if book_name:
                self.__db.borrow_book(user_id, book_id)
                # Add Google Calendar reminder
                self.__calendar.insert_event(book_name)
                print("You have successfully borrowed '{}'.".format(book_name))
                print()
            else:
                print()
                print("Error: You have entered an invalid book ID, please try again.")
                print()

    def return_book(self, user_id, action):
        """
        Select and return a book

        Parameters:
            user_id (str): Currently logged in user
            action (str): Either "text" or "qr" for method of book ID input

        Returns:
            The borrowed book will be returned to the system.
        """
        # Only show list of borrowed books for text input of book ID
        if action == "text":
            print("--- Borrowed Books ---")
            print("{:<15} {:<80} {}".format("BookID", "Title", "Author"))

            for book in self.__db.get_borrowed_books(user_id):
                book_id = book[0]
                title = book[1]
                author = book[2]

                print("{:<15} {:<80} {}".format(book_id, title, author))

            print()

        # Allow the user to keep returning books until they type 'exit'
        while True:
            if action == "text":
                book_id = input(
                    "Enter ID of the book you'd like to return or type 'exit' to stop returning: "
                )
            elif action == "qr":
                book_id = QR().scan_qr()

            if book_id == "exit":
                break

            book_name = self.validate_book(book_id, user_id, "return")

            # Check that the book has been borrowed by this user
            if book_name:
                self.__db.return_book(user_id, book_id)
                print()
                # Remove Google Calendar reminder
                self.__calendar.delete_event(book_name)
                print("You have successfully returned '{}'.\n".format(book_name))
                if action == "qr":
                    break
                print()
            else:
                print()
                if action == "text":
                    print("Error: You have entered an invalid book ID, please try again.")
                elif action == "qr":
                    print("Error: You have scanned an invalid book ID, please try again.")
                print()
