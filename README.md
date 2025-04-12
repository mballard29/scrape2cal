# Scraping Calendar Imports
Web scraping/scraping a webpage for data to programmatically add events to Google calendar.

### Motivation (example)
If given an event agenda online, and you want to add the items to Google calendar without copy and pasting over and over again.

### General steps taken
1) joined Google developer program
2) created Google cloud project
   - name: `scrape-calendar-imports`
3) added Google Calendar API permissions to project
4) configured Google Auth platform
5) added OAuth credentials, export credentials as json
6) create project folder, add credentials json to folder, create read me
7) create python virtual environment
8) download/ --upgrade packages: `python3 -m pip install -r requirements.txt`
   - as I was building, I would add the needed pack to requirements and rerun command to make sure it was properly added to the python environment/interpreter in vscode
9)  use Google documentation to create program (they have errors, so debug and fix to make work)