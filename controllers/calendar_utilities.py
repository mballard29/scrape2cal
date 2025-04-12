from datetime import datetime, timezone
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
  "https://www.googleapis.com/auth/calendar.readonly",
  "https://www.googleapis.com/auth/calendar.events.owned"
]

CREDS = None

def create_token():
  if os.path.exists("token.json"):
    CREDS = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not CREDS or not CREDS.valid:
    if CREDS and CREDS.expired and CREDS.refresh_token:
      CREDS.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      CREDS = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(CREDS.to_json())
    CREDS = Credentials.from_authorized_user_file("token.json", SCOPES)
  return CREDS


def get_my_calendars(CREDS):
  my_calendars = dict()
  try:
    service = build("calendar", "v3", credentials=CREDS)

    page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      for i, c in enumerate([calendar_list_entry for calendar_list_entry in calendar_list['items'] if calendar_list_entry['accessRole'] == "owner"]):
        my_calendars[i+1] = [c['id'], c['summary']]
        my_calendars[i+1] = {
          'id': c['id'], 
          'summary': c['summary']
        }
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break

  except HttpError as error:
    print(f"{error}")

  return my_calendars

def import_events(CREDS, my_events, cal_id):
  try:
    service = build("calendar", "v3", credentials=CREDS)

    for e in my_events:
      event = {
        'summary': e['summary'],
        "colorId": "10",
        'description': e['description'],
        'start': {
          'dateTime': e['start'],
        },
        'end': {
          'dateTime': e['end'],
        }
      }
      event = service.events().insert(calendarId=cal_id, body=event).execute()
      print('Event created: %s' % (event.get('htmlLink')))
    print(f'IMPORTED {len(my_events)} events to {cal_id} calendar.')
  except HttpError as error:
    print(f"{error}")


def import_events_color(CREDS, my_events, cal_id, color):
  try:
    service = build("calendar", "v3", credentials=CREDS)

    for e in my_events:
      event = {
        'summary': e['summary'],
        "colorId": str(color),
        'description': e['description'],
        'start': {'date': e['start']},
        'end': {'date': e['end']}
      }
      event = service.events().insert(calendarId=cal_id, body=event).execute()
      print('Event created: %s' % (event.get('htmlLink')))
    print(f'IMPORTED {len(my_events)} events to {cal_id} calendar.')
  except HttpError as error:
    print(f"{error}")
