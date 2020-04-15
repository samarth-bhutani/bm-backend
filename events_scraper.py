import re, requests
from datetime import datetime, timedelta
import unidecode as u
from bs4 import BeautifulSoup

EVENTS_URL = "http://events.berkeley.edu/"

# Number of days of events to fetch
NUM_DAYS = 28

def get_date(offset):
    """
    Args:
        offset (int): Number of days from now the date returned should correspond to
    Returns:
        Datetime object
    """
    now = datetime.now()
    return now + timedelta(days=offset)


def get_events_url(date):

    """
    Get the event url for a given date.
    Args:
        date (datetime object): The day the date should correspond to
    Returns:
        (str) the page url of the events
    """

    url_p2 = "?view=summary&timeframe=day&date="
    curr_date = date.strftime("%Y-%m-%d")
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


def parse_subtitles(p, event):
    """
    Parses P and assigns subtitles to correct attribute in EVENT.
    Args:
        p (bs4.element.Tag): paragraph with subtitle items:
            Category, Date, Time (optional), Location, Status Alert
        event (dict): JSON object representing event
    Returns:
        None
    """
    status_alert = p.find('span', class_='statusAlert')
    subtitles = p.text.split("|")

    if len(subtitles) < 2:
        return

    if status_alert:
        event["status"] = clean_str(status_alert.text)
        subtitles.pop()

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


def parse_paragraphs(paragraphs, event, link):
    """
        Parses paragraph tags in an event row.
        Args:
            paragraphs (list<bs4.element.Tag>): List of paragraphs in event row
            event (dict): The event JSON object
            link (str): url for the event
        Returns:
            None
    """
    subtitles = paragraphs[0].text.split("|")
    parse_subtitles(paragraphs[0], event)
    if len(paragraphs) < 1:
        return

    for p in paragraphs[1:]:
        label = p.find('label')
        if label:
            if re.search('sponsor', label.text.lower()):
                sponsors = p.find_all('a', href=True)
                for sponsor in sponsors:
                    sponsor_name = clean_str(sponsor.text)
                    event["labels"]["sponsors"][sponsor_name] = sponsor['href']
            elif re.search('speaker', label.text.lower()):
                event["labels"]["speakers"] = clean_str(p.find(text=True, recursive=False))
            else:
                event["labels"]["other"] = clean_str(p.text)
        else:
            # Parse event description
            links = p.find_all('a', href=True)
            if links and re.search('More >', clean_str(links[-1].text)):
                # Event description is truncated, query event page for full description
                response = requests.get(link)
                html = BeautifulSoup(response.text.encode('utf-8','ignore'), 'html.parser')
                event_row = html.find('div', class_='event row')
                event_ps = event_row.find_all('p')
                for event_p in event_ps:
                    if not event_p.find('label'):
                        event["description"] = clean_str(event_p.text)
            else:
                event["description"] = clean_str(p.text)

def initialize_event():
    """
        Returns an empty event object.
    """
    event = {}
    event["title"] = None
    event["link"] = event["image"] = None
    event["status"] = None
    event["time"] = event["location"] = event["date"] = None
    event["description"] = event["category"] = None
    labels = {}
    labels["other"] = []
    labels["speakers"] = None
    labels["sponsors"] = {}
    event["labels"] = labels
    return event

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
            - description (str): event details
            - link (str): event detail link
            - image (str): event image url, if available
    """
    event = initialize_event()
    title_tag = event_row.find('h3', class_='event-title').find('a', href=True)
    event["title"] = clean_str(title_tag.text)
    event["link"] = EVENTS_URL + title_tag["href"]
    if re.search("CANCELED", event["title"].upper()):
        event["status"] = "Canceled"

    paragraphs = event_row.find_all('p')
    if paragraphs:
        parse_paragraphs(paragraphs, event, event["link"])

    img_src = event_row.find('img', class_='cc-image', src=True)
    if img_src:
        if re.match('/images/', img_src["src"]):
            event["image"] = EVENTS_URL + img_src["src"]
        else:
            event["image"] = img_src["src"]
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
        html = BeautifulSoup(response.text.encode('utf-8','ignore'), 'html.parser')
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


def scrape():
    result = {}
    for i in range(NUM_DAYS):
        date = get_date(i)
        result[date.strftime("%Y-%m-%d")] = get_events(get_events_url(date))
    return result

scrape()