import json, helper, re, requests
from datetime import datetime, timedelta
import unidecode as u
from bs4 import BeautifulSoup

EVENTS_URL = "http://events.berkeley.edu/"

# Number of days of events to fetch
NUM_DAYS = 28

def get_date(offset=0):
    """
    Args:
        offset (int): Number of days from now the date returned should correspond to
    Returns:
        Datetime object
    """
    now = datetime.now()
    return now + timedelta(days=offset)


def format_date(date):
    """
    Args:
        date (datetime object): the date to format
    Returns:
        (str) date formatted in year-month-day
    """
    return "{year}-{month}-{day}".format(year=date.year, month=date.month, day=date.day)


def get_events_url(date):

    """
    Get the event url for a given date.
    Args:
        date (datetime object): The day the date should correspond to
    Returns:
        (str) the page url of the events
    """

    url_p2 = "?view=summary&timeframe=day&date="
    curr_date = format_date(date)
    url_p4 = "&tab=all_events"
    url = EVENTS_URL + url_p2 + curr_date + url_p4
    return url


def clean_str(string):
    """
    Decodes unicode characters, replaces duplicate whitespace with single whitespace, and 
    strips trailing and beginning whitespace.
    Args: 
        string (str): The string to clean
    Returns:
        (str) A new copy of the cleaned string.
    """
    decoded = u.unidecode(string)
    return re.sub('\s+', ' ', decoded).strip()


def parse_subtitles(subtitles, event):
    """
    Parses SUBTITLES and assigns them to the correct attribute in EVENT.
    Args:
        subtitles (list<str>): list of subtitle items: Category, Date, Time (optional), Location
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

    if len(subtitles) > 3:
        event["time"] = subtitles[2]
        event["location"] = subtitles[3]
    else:
        event["location"] = subtitles[2]


def parse_paragraphs(paragraphs, event):
    """
        Parses paragraph tags in an event row to populate description and labels fields in event.
        Args:
            paragraphs (list<bs4.element.Tag>): List of paragraphs in event row
            event (dict): The event JSON object
        Returns:
            None
    """

    labels = {}
    labels["other"] = []
    event["description"] = {}
    event["description"]["text"] = None
    event["description"]["truncated"] = False
    event["status"] = None
    for p in paragraphs:
        label = p.find('label')
        status_alert = p.find('span', class_='statusAlert')
        if status_alert:
            event["status"] = clean_str(status_alert.text)
        if label:
            if re.search('sponsor', label.text.lower()):
                sponsors = p.find_all('a', href=True)
                labels["sponsors"] = {}
                for sponsor in sponsors:
                    sponsor_name = clean_str(sponsor.text)
                    labels["sponsors"][sponsor_name] = sponsor['href']
            elif re.search('speaker', label.text.lower()):
                labels["speakers"] = clean_str(p.find(text=True, recursive=False))
            else:
                labels["other"] = clean_str(p.text)
        else:
            # Parse event description
            links = p.find_all('a', href=True)
            if links and re.search('More >', clean_str(links[-1].text)):
                event["description"]["text"] = clean_str(p.text)[0:-6].strip()
                event["description"]["truncated"] = True
            else:
                event["description"]["text"] = clean_str(p.text)
    event["labels"] = labels


def parse_event(event_row):
    """
    Args:
        event_row (bs4.element.Tag): BeautifulSoup Tag object with the class 'event-row' 
        corresponding to an event.
    Returns:
        JSON object representing EVENT. 
        Schema:
            - title (str): event title
            - category (str): event category
            - date (str): event date
            - time (str): event time or null if all-day
            - location (str): event location
            - status (str): status alert, if available (e.g. canceled)
            - labels: (dict)
                - sponsors:
                    - sponsor: link to sponsor details
                - speakers: string of speakers and performers
                - other: (list<str>) event details with a label
            - description (dict):
                - truncated: (bool) True if description is truncated
                - text: (str) event details
            - link (str): event detail link
            - image (str): event image url, if available
    """
    event = {}
    title = event_row.find('h3', class_='event-title').find('a', href=True)
    paragraphs = event_row.find_all('p')
    event["title"] = clean_str(title.text)
    event["link"] = EVENTS_URL + title['href']
    if paragraphs:
        subtitles = paragraphs[0].text.split("|")
        parse_subtitles(subtitles, event)
    if len(paragraphs) > 1:
        parse_paragraphs(paragraphs[1:], event)
    img_src = event_row.find('img', class_='cc-image', src=True)
    if img_src:
        if re.match('/*images/', img_src["src"]):
            event["image"] = EVENTS_URL + img_src["src"]
        else:
            event["image"] = img_src["src"]
    else:
        event["image"] = None
    return event


def get_events(url):
    """
    Args:
        url (str): the page url of the events to fetch.
    Returns:
        A list of the event JSON objects.
    """
    events = []
    search = True
    while search:
        response = requests.get(url)
        html = BeautifulSoup(response.text.encode('utf-16','ignore'), 'html.parser')
        event_rows = html.find_all('div', class_='event row')
        for event in event_rows:
            events.append(parse_event(event))
        prev_next_page = html.find('div', class_='previousNextPage')

        # If there are more pages, get link of next page
        if prev_next_page:
            links = prev_next_page.find_all('a', href=True)
            if len(links) == 2:
                url = EVENTS_URL + links[1]["href"]
            else:
                search = False
        else:
            search = False

    return events


def scrape(req):
    result = {}
    for i in range(NUM_DAYS):
        date = get_date(i)
        result[format_date(date)] = get_events(get_events_url(date))
    print(json.dumps(result, indent=2))
    return result

scrape('placeholder')

