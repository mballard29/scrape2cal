from controllers.calendar_utilities import create_token, get_my_calendars, import_events
from controllers.scraping_bonus_sessions import scrape

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
  
  src_path = 'reference/source.html'
  my_events = scrape(src_path)

  import_events(CREDS, my_events, my_calendars[item]['id'])
  # import_events(<credentials, <list of dictionaries of events>, <id of target calendar>)
  # import_events_color("", "", "", <color id of color to make imported event(s)>)



if __name__ == "__main__":
  main()