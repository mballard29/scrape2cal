import csv
from datetime import datetime

def from_csv(src_path, count):
    add_events = []
    this_mo = int(datetime.today().strftime("%m"))
    this_year = int(datetime.today().strftime("%Y"))

    for i in range(count):
        with open(src_path, 'rt') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row_num, row in enumerate(csv_reader):
                if row_num==0:
                    pass
                else:
                    add_events.append({
                        'summary': row[0],
                        'location': '',
                        'description': '',
                        'start': datetime(this_year, this_mo+i, int(row[1])).strftime(r"%Y-%m-%d"),
                        'end': datetime(this_year, this_mo+i, int(row[1])).strftime(r"%Y-%m-%d"),
                    })
    return add_events
