from __future__ import print_function
from keys import cal_key
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import GoogleAuthError

# Paths for token and credentials files
TOKEN_PATH = 'token.pickle'
CREDENTIALS_PATH = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Gcalendar:
    def __init__(self):
        self.events = []

    def gcal_connect(self):
        """Connects to the Google Calendar API and retrieves the next 2 events."""
        
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None

        # Load or refresh credentials from token.pickle
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)

        try:
            # Refresh the token if it's expired
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            # If no valid credentials, run OAuth flow to generate new ones
            if not creds or not creds.valid:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the refreshed or new token to file
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        except GoogleAuthError as e:
            # Handle invalid_grant error by removing the token and restarting OAuth flow
            if 'invalid_grant' in str(e):
                print("Token has been expired or revoked. Re-authenticating...")
                if os.path.exists(TOKEN_PATH):
                    os.remove(TOKEN_PATH)  # Delete the invalid token file
                # Run the OAuth flow to get new credentials
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the new token
                with open(TOKEN_PATH, 'wb') as token:
                    pickle.dump(creds, token)
            else:
                print(f"GoogleAuthError: {e}")  # Raise any other exceptions
                return []

        except Exception as e:
            # Catch any other exceptions and log the error
            print(f"An error occurred while fetching Google Calendar events: {e}")
            return []

        # Build the service to interact with the Google Calendar API
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API to retrieve events
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId=cal_key, timeMin=now, maxResults=2, 
            singleEvents=True, orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        if not events:
            return 'No upcoming events found.'

        return self.set_data(events)

    def set_data(self, events):
        """Formats the retrieved events."""
        self.events = []  # Clear previous events to avoid duplication
        for event in events:
            self.events.append(
                dict(
                    summary=event.get('summary', 'No title'),
                    start=event['start'].get('dateTime', event['start'].get('date')),
                    location=event.get('location', '')
                )
            )
        return tuple(self.events)


if __name__ == '__main__':
    cal = Gcalendar()
    print(cal.gcal_connect())
