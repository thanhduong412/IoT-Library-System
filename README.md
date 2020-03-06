# Programming Internet of Things: Assignment 2

## Raspberry Pi Console-Based Menu

### Dependencies
```
# Local database and passwords
pip3 install sqlite3
pip3 install getpass

# MySQL
sudo apt update
sudo apt install default-libmysqlclient-dev
sudo apt install mysql-client
pip3 install mysqlclient

# QR code
pip3 install imutil numpy opencv-python pyzbar

# Google Calendar
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install google-api-python-client oauth2client
pip3 install httplib2

# Voice to text recognition
pip3 install SpeechRecognition
sudo apt-get install portaudio19-dev python-all-dev python3-all-dev
pip3 install pyaudio
pip3 install google-api-python-client
sudo apt-get install flac
```

### Configure Microphone And Speakers
```
https://developers.google.com/assistant/sdk/guides/service/python/embed/audio
```

### Set up Google Calendar Reminders
When logging into the Master Pi LMS menu for the first time, you will be asked to grant access to
you Google account to receive reminders in Google Calendar when you have borrowed a book, and remove
these reminders once a book has been returned.

1. Go to the specified link in your browser and follow the instructions to grant access to your
account.
2. Paste the resulting verification code into the console input.

### Running Menu
1. Whitelist the following Master Pi IP address in the Google Cloud SQL console:
```
curl icanhazip.com
```
2. Listen to incoming socket connections from the Reception Pi on the Master Pi:
```
python3 assignment2_project/master.py --noauth_local_webserver
```
3. Login/register from the Reception Pi:
```
python3 assignment2_project/reception.py
```
4. Access the LMS menu from the MasterPi.

## Flask Web Application

### Dependencies
```
pip3 install flask flask_bootstrap flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy
```

### Running Flask Web Application
1. Whitelist the following Master Pi IP address in the Google Cloud SQL console:
```
curl icanhazip.com
```
2. Run the command to launch the Flask application:
```
python3 assignment2_project/webapp/flask_main.py
```

## Authors

* **Tracy Chan** - [GitHub](https://github.com/tracychan277/)
* **Jack Murray** - [GitHub](https://github.com/s3722598/)
* **Thanh Duong** - [GitHub](https://github.com/s3601172/)
* **Kevin Tunacao** - [GitHub](https://github.com/s3600546/)
