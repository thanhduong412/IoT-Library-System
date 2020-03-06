"""Creates GoogleCalendar class"""
from __future__ import print_function
from datetime import datetime, timedelta
import warnings
# Disable linting error that packages are not found locally
# pylint: disable=E0401
# Google CalendarAPI
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# pylint: disable=R0903
class GoogleCalendar:
    """Handles Google calendar related functions such as creating or showing events"""
    def __init__(self):
        self.__service = ""

    def set_up(self):
        """Set up Google calendar access authorisation"""
        scopes = "https://www.googleapis.com/auth/calendar"

        # Catch 'token.json' not found warning
        warnings.filterwarnings("error")
        try:
            store = file.Storage("token.json")
            creds = store.get()
            self.__service = build("calendar", "v3", http=creds.authorize(Http()))
        except UserWarning:
            print("--- Google Calendar account authorisation ---")
            flow = client.flow_from_clientsecrets("credentials.json", scopes)
            creds = tools.run_flow(flow, store)
            self.__service = build("calendar", "v3", http=creds.authorize(Http()))
            print()

    def show_events(self):
        """
        If a user wants to see their upcoming events, prints the 10 events they have coming up.
        """
        # Call the Calendar API.
        now = datetime.utcnow().isoformat() + "Z"
        events_result = self.__service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        # Print upcoming events
        if not events:
            print("No upcoming events found.")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])
        print()

    def insert_event(self, book_name):
        """
        This method creates an event in the users calendar for when they
        need to return a book.
        """
        date = datetime.now()
        # Make the return date in one weeks' time
        return_date = (date + timedelta(days=7)).strftime("%Y-%m-%d")
        time_start = "{}T06:00:00+10:00".format(return_date)
        time_end = "{}T07:00:00+10:00".format(return_date)
        event = {
            "summary": "Reminder: Your book is due",
            "description": book_name,
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 5},
                ],
            }
        }
        event = self.__service.events().insert(calendarId="primary", body=event).execute()
        print("Event reminder created: {}".format(event.get("htmlLink")))

    def delete_event(self, book_name):
        """
        Will delete the event when a book borrowed has been returned.
        """
        event = self.__service.events().list(
            calendarId="primary",
            q=book_name,
            singleEvents=True
        ).execute()
        event_id = event.get("items", [])[0]["id"]
        delete_event = self.__service.events().delete(calendarId="primary", eventId=event_id)
        delete_event.sendNotifications = True
        delete_event.execute()
        print("Your event reminder has been deleted.")
