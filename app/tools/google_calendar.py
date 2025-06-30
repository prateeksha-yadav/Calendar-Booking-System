import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    
    # Securely load credentials for cloud deployment
    creds_json_str = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    token_json_str = os.environ.get('GOOGLE_TOKEN_JSON')

    if creds_json_str:
        # If running in the cloud, write the env vars to temporary files
        with open('credentials.json', 'w') as f:
            f.write(creds_json_str)
        if token_json_str:
            with open('token.json', 'w') as f:
                f.write(token_json_str)

    creds = None
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except (FileNotFoundError, json.JSONDecodeError):
        pass # It's ok if the token doesn't exist yet

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
        else:
            # Check if running in a deployed environment like Streamlit Cloud
            if 'STREAMLIT_SERVER_PORT' in os.environ or token_json_str:
                raise ValueError(
                    "Google Calendar authentication failed. "
                    "The token is missing, invalid, or expired and couldn't be refreshed. "
                    "If you are the app owner, please re-run the authentication locally "
                    "to generate a new 'token.json' and update the 'GOOGLE_TOKEN_JSON' secret in your deployment environment."
                )
            
            # Fallback to local interactive flow if not in a deployed environment
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "credentials.json not found. Please follow the setup instructions in the README.md to get this file."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_available_slots(date):
    """
    Get available slots for a given date.
    For simplicity, we'll assume a working day from 9 AM to 5 PM,
    and each slot is 1 hour long.
    We'll check for events in the calendar and return the slots that are free.
    """
    service = get_calendar_service()
    
    # The date string is now guaranteed to be clean (YYYY-MM-DD)
    # Time range for the given day (9 AM to 5 PM)
    start_time = datetime.datetime.fromisoformat(date + "T09:00:00")
    end_time = datetime.datetime.fromisoformat(date + "T17:00:00")

    # Get events from the calendar
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time.isoformat() + 'Z',
        timeMax=end_time.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    # Generate potential slots
    potential_slots = []
    current_time = start_time
    while current_time < end_time:
        potential_slots.append(current_time)
        current_time += datetime.timedelta(hours=1)
    
    # Filter out busy slots
    busy_slots = []
    for event in events:
        event_start_str = event['start'].get('dateTime')
        # Handle timezone-aware strings from Google Calendar API
        if event_start_str.endswith('Z'):
            event_start_str = event_start_str.replace('Z', '+00:00')
        event_start = datetime.datetime.fromisoformat(event_start_str)
        busy_slots.append(event_start)

    available_slots = [
        slot.strftime("%Y-%m-%dT%H:%M:%S") 
        for slot in potential_slots 
        if slot not in busy_slots
    ]
    
    return available_slots

def book_appointment(slot, summary="Appointment"):
    """
    Book an appointment for a given slot.
    """
    service = get_calendar_service()
    
    start_time = datetime.datetime.fromisoformat(slot)
    end_time = start_time + datetime.timedelta(hours=1)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    
    return created_event.get('htmlLink') 