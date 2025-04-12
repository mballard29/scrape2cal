from datetime import date

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from controllers.calendar_utilities import create_token, import_events_color

# find available calendar and event colors

CREDS = None

def main():
  CREDS = create_token()

  # METHOD 1: See in Google calendar as all day events starting today +1 day for number of event colors
  # today = date.today()

  # add_events = []
  # for i in range(12):
  #   add_events.append({
  #         'summary': f'color {i}',
  #         'description': 'description',
  #         'start': today.isoformat(),
  #         'end': today.isoformat()
  #       })
  #   import_events_color(CREDS, add_events, 'primary', i)
  #   today = today.replace(day = today.day+1)
  #   add_events.clear()

  # METHOD 2: Export colors to a css file (vscode has extensions to show color swatches in IDE)
  # can uncomment foreground, but they're all black
  service = build("calendar", "v3", credentials=CREDS)
  colors = service.colors().get().execute()

  with open('reference/colors.css', 'w') as of:
    of.write('.calendar {\n')
    for i in colors['calendar'].items():
      of.write(f'\tbackground-{i[0]}: {i[1]['background']};\n')
      # of.write(f'\tforeground-{i[0]}: {i[1]['foreground']};\n')
    of.write('}\n\n')
    of.write('.event {\n')
    for j in colors['event'].items():
      of.write(f'\tbackground-{j[0]}: {j[1]['background']};\n')
      # of.write(f'\tforeground-{j[0]}: {j[1]['foreground']};\n')
    of.write('}\n\n')

if __name__ == "__main__":
  main()



'''
colors
0 = calendar color (special variable based on current calendar)
1 = lavender
2 = sage (light green)
3 = grape
4 = flamingo
5 = banana
6 = tangerine
7 = peacock (light blue)
8 = graphite
9 = blueberry
10 = basil
11 = tomato
'''