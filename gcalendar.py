from __future__ import print_function
from keys import cal_key
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import GoogleAuthError

class Gcalendar:
    def __init__(self):
        self.events = []

    def gcal_connect(self):
        """Connects to the Google Calendar API and retrieves the next 2 events."""
        
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None

        try:
            # Load or refresh credentials from token.pickle
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            
            # If no credentials or they are expired, refresh or get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            
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

        except GoogleAuthError as e:
            # Handle Google authentication errors
            print(f"GoogleAuthError: {e}")
            return []

        except Exception as e:
            # Catch any other exceptions and log the error
            print(f"An error occurred while fetching Google Calendar events: {e}")
            return []

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
