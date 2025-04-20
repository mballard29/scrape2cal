import re
from datetime import datetime, timedelta
from controllers.scraping_bonus_sessions import convert12to24
from pytz import timezone

def from_text(src_path):
    add_events = []
    with open(src_path, 'r') as schedule:
        day = None
        for l in schedule.readlines()[3:]:
            if l == '\n':
                continue
            if re.match(r"Friday", l) or re.match(r"Saturday", l) or re.match(r"Sunday", l):
                date_format = "%A, %B %d, %Y"
                day = datetime.strptime(l.strip(), date_format)
            else:
                data = re.findall(r"(.*?) \((.*?), (.*?)\)", l.strip())[0]
                time = convert12to24(data[1] + 'pm').split(':')
                start = day.replace(hour=int(time[0]), minute=int(time[1]))
                time_delta = timedelta(hours=1)
                end = start + time_delta
                add_events.append({
                    'summary': data[0],
                    'location': data[2],
                    'description': '',
                    'start': timezone('America/Los_Angeles').localize(start).isoformat(),
                    'end': timezone('America/Los_Angeles').localize(end).isoformat(),
                })
    return add_events
