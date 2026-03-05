import requests
from controllers.calendar_utilities import create_token, get_my_calendars, import_events, import_allday_events, import_events_color
from controllers.scraping_bonus_sessions import scrape, dynamic_scrape
from controllers.read_text import from_text
from controllers.read_csv import from_csv

CREDS = None

def main():
  CREDS = create_token()

  my_calendars = get_my_calendars(CREDS)

  # print menu
  for i in my_calendars.keys():
    print(i, my_calendars[i]['summary'])

  # select from menu
  item = int(input("Enter the number of the calendar you would like to add events to: "))
  print('Importing to: ', my_calendars[item]['summary'])
  
  # scraping a static webpage
  # src_path = 'reference/source.html'
  # my_events = dynamic_scrape(src_path)

  # scraping a dynamic webpage by saving to html file
  # src_path = 'reference/source.html'
  # my_events = dynamic_scrape(src_path)

  # get import event data from textfile
  # src_path = 'reference/coachella-w2-lineup.txt'
  # my_events = from_text(src_path)

  # add bills - repeated events occurring on the same date every month
  src_path = 'reference/events.csv'
  my_events = from_csv(src_path, count=10)

  import_allday_events(CREDS, my_events, my_calendars[item]['id'])
  # BASIC SYNTAX
  # import_events(<credentials, <list of dictionaries of events>, <id of target calendar>)
  # IMPORT ALL WITH A GIVEN COLOR ID
  # import_events_color("", "", "", <color id of color to make imported event(s)>)
  # IMPORT ALL DAY REPETITIVE EVENTS (always same num day)
  # import_allday_events(CREDS, <list of dictionaries of events>, <id of target calendar>)



if __name__ == "__main__":
  main()