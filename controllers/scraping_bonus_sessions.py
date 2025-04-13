from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

def convert24(time):
  t = datetime.strptime(time, '%I:%M%p')
  return t.strftime('%H:%M')

def scrape(src_path):
  add_events = []
  with open(src_path, 'r') as inf:
    soup = BeautifulSoup(inf, "html.parser")

    title = None
    start_time = None
    end_time = None
    
    events = soup.find_all('li', class_='article-listing__item')
    for e in events:
      description = ''
      title = e.find('div', class_='title').get_text().strip()

      body_para = e.find_all("p")

      # Sunday, April 13, 2025 | 12:30pm – 1:15pm Eastern Time (UTC-4)
      date_time = body_para.pop(0).get_text()
      date, time = date_time.split('|')
      date = date.split(',')
      # date = [month, day, year]
      date = [4, date[1].split()[1].strip(), date[2].strip()]

      # start, end = [HH, MM]
      time = [x.upper().strip() for x in time.split('–')[0:2]]
      start = convert24(time[0]).split(':')
      end = convert24(time[1].split()[0].strip()).split(':')

      date = [int(x) for x in date]
      start = [int(x) for x in start]
      end = [int(x) for x in end]

      # datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
      start_time = timezone('America/New_York').localize((datetime(date[2], date[0], date[1], start[0], start[1], 0))).isoformat()
      end_time = timezone('America/New_York').localize((datetime(date[2], date[0], date[1], end[0], end[1], 0))).isoformat()

      body_para = e.find('div', class_='description')
      for i, c in enumerate(body_para.children):
        if i == 0:
          continue
        for j, cc in enumerate(c.children):
          description += cc.get_text() + ' '
        description += '\n\n'
      
      add_events.append({
        'summary': title,
        'description': description,
        'start': start_time,
        'end': end_time
      })
  
  return add_events