import requests
import json
from datetime import datetime
import re
import unidecode as u
from bs4 import BeautifulSoup

def get_curr_week_events_url():
    """
    Returns:
        (str) the page url of the events for the current week.
    """
    now = datetime.now()

    url_p1 = "http://events.berkeley.edu/?view=summary&timeframe=month&date="
    curr_date = "{year}-{month}-{day}".format(year=now.year, month=now.month, day=now.day)
    url_p3 = "&tab=all_events"
    url = url_p1 + curr_date + url_p3
    return url

def clean_str(string):
    """
    Decodes unicode characters, replaces duplicate whitespace with single whitespace, and 
    strips trailing whitespace.
    Args: 
        string (str): The string to clean
    Returns:
        A new copy of the cleaned string.
    """
    decoded = u.unidecode(string)
    return re.sub('\s+', ' ', decoded).strip()

def parse_subtitles(subtitles, event):
    """
    Parses SUBTITLES and assigns them to the correct attribute in EVENT.
    Args:
        subtitles (list[str]): list of subtitle items: Category, Date, Time (optional), Location
        event (dict): JSON object representing event
    Returns:
        None
    """
    if len(subtitles) < 2:
        return

    subtitles = list(map(clean_str, subtitles))
    event["category"] = subtitles[0]

    date = subtitles[1]
    # Add space after comma
    date = re.sub(',\s*', ', ', date)
    event["date"] = date

    if len(subtitles) == 3:
        event["location"] = subtitles[2]
    else:
        event["time"] = subtitles[2]
        event["location"] = subtitles[3]

def parse_paragraphs(paragraphs, event):
    labels = {}
    event["description"] = []
    for p in paragraphs:
        label = p.find('label')
        if label and re.search('Sponsor', label.text):
            sponsors = p.find_all('a', href=True)
            labels["sponsors"] = {}
            for sponsor in sponsors:
                sponsor_name = clean_str(sponsor.text)
                labels["sponsors"][sponsor_name] = sponsor['href']
        elif label and re.search('Speaker', label.text):
            labels["speakers"] = clean_str(p.find(text=True, recursive=False))
        else:
            event["description"].append(clean_str(p.text))
    event["labels"] = labels

def find_event_status(event):
    # FIXME
    return None

def parse_event(event_row):
    """
    Args:
        event_row (bs4.element.Tag): BeautifulSoup Tag object with the class 'event-row' 
        corresponding to an event.
    Returns:
        JSON object representing EVENT. All attributes are strings.
        Schema:
            - title: event title
            - category: event category
            - date: event date
            - time: event time or null if all-day
            - location: event location
            - status: status alert, if available (e.g. canceled)
            - labels: JSON object of accompanying event labels (e.g. sponsors, performers, etc.)
                - sponsors:
                    - sponsor: link to sponsor details
                - speakers: string of speakers and performers
                - other:
                    - label: description
            - description: (list[str]) event details
            - link: event detail link
            - image: event image url, if available
    """
    event = {}
    title = event_row.find('h3', class_='event-title').find('a', href=True)
    paragraphs = event_row.find_all('p')
    event["title"] = clean_str(title.text)
    event["link"] = "http://events.berkeley.edu/" + title['href']
    if paragraphs:
        subtitles = paragraphs[0].text.split("|")
        parse_subtitles(subtitles, event)
    if len(paragraphs) > 1:
        parse_paragraphs(paragraphs[1:], event)
    event["status"] = find_event_status(event_row)
    event["image"] = None
    return event

def get_events(url):
    """
    Args:
        url: (str) the page url of the events for the current week.
    Returns:
        A list of the event JSON objects.
    """
    events = []
    response = requests.get(url)
    html = BeautifulSoup(response.text.encode('utf-16','ignore'), 'html.parser')
    event_rows = html.find_all('div', class_='event row')
    for event in event_rows:
        events.append(parse_event(event))
    return events

def scrape(req):
    result = {}
    result["events"] = get_events(get_curr_week_events_url())
    print(json.dumps(result, indent=2))
    return result

scrape('placeholder')

