import datetime
import json
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Shows basic usage of the Google Calendar API."""
    creds = None
    token_json_str = os.environ.get('GOOGLE_TOKEN_JSON')

    # Deployed environment: load credentials directly from environment variables
    if token_json_str:
        try:
            token_info = json.loads(token_json_str)
            creds = Credentials.from_authorized_user_info(token_info, SCOPES)
        except json.JSONDecodeError:
            raise ValueError("Could not parse GOOGLE_TOKEN_JSON.")
    # Local development: load from files
    elif os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, refresh or create new ones.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # In local dev, save the refreshed token for next run
            if not token_json_str:
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
        else:
            # This block is for local development only to create the first token.
            is_deployed = os.environ.get('RENDER') or os.environ.get('STREAMLIT_SERVER_PORT')
            if is_deployed:
                raise ValueError(
                    "Authentication failed. The token is missing, invalid, or expired. "
                    "The app owner needs to re-authenticate locally and update the GOOGLE_TOKEN_JSON secret."
                )
            
            # In local dev, we need credentials.json to create a new token
            if not os.path.exists('credentials.json'):
                 raise FileNotFoundError(
                    "credentials.json not found. This file is required for local development. "
                    "Please follow the setup instructions in the README."
                )

            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the new credentials for the next run
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
    
    start_time = datetime.datetime.fromisoformat(date + "T09:00:00")
    end_time = datetime.datetime.fromisoformat(date + "T17:00:00")

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time.isoformat() + 'Z',
        timeMax=end_time.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    potential_slots = []
    current_time = start_time
    while current_time < end_time:
        potential_slots.append(current_time)
        current_time += datetime.timedelta(hours=1)
    
    busy_slots = []
    for event in events:
        event_start_str = event['start'].get('dateTime')
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