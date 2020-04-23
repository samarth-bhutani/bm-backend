import re, requests
from datetime import datetime, timedelta
import unidecode as u
from bs4 import BeautifulSoup
from multiprocessing import Pool

EVENTS_URL = "http://events.berkeley.edu/"

# Number of days of events to fetch
NUM_DAYS = 28

# Number of worker threads to run
NUM_WORKERS = 10

# Number of attempts to fetch event description
NUM_ATTEMPTS = 3

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
            label_type = clean_str(label.text).replace(":", "")
            event["labels"][label_type] = clean_str(p.text.replace(label.text, ""))
        else:
            # Parse event description
            links = p.find_all('a', href=True)
            if links and re.search('More >', clean_str(links[-1].text)):
                # Event description is truncated, query event page for full description
                i = 0
                while i < NUM_ATTEMPTS:
                    response = requests.get(link)
                    html = BeautifulSoup(response.text.encode('utf-8','ignore'), 'html.parser')
                    event_row = html.find('div', class_='event row')
                    if event_row:
                        event_ps = event_row.find_all('p')
                        for event_p in event_ps:
                            if not event_p.find('label'):
                                event["description"] = clean_str(event_p.text)
                        break
                    else:
                        i += 1
                        if i >= NUM_ATTEMPTS:
                            print("Failed to fetch full description for {}. Using truncated description.".format(event["title"]))
                            event["description"] = clean_str(p.text)
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
    event["labels"] = {}
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
                - label: label text (e.g. sponsors: 'BAMPFA, John Green, PhD.')
            - description (str): event details
            - link (str): event detail link
            - image (str): event image url, if available
    """
    event = initialize_event()
    try:
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
    except Exception as e:
        print(e)
        print("An error occurred scraping " + event_row.text[:100])
    return event


def get_events(url):
    """
    Args:
        url (str): the page url of the events to fetch.
    Returns:
        A list of the event JSON objects.
    """
    events = {}
    try:
        search = True
        while search:
            response = requests.get(url)
            html = BeautifulSoup(response.text.encode('utf-8','ignore'), 'html.parser')
            event_rows = html.find_all('div', class_='event row')
            count = 0
            for row in event_rows:
                event = parse_event(row)
                if event:
                    events[str(count)] = event
                    count += 1
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
    except Exception as e:
        print(e)
        print("An error occurred scraping " + url)
    return events


def scrape():
    result = {}
    p = Pool(NUM_WORKERS)
    urls = [get_events_url(get_date(i)) for i in range(NUM_DAYS)]
    events = p.map(get_events, urls)
    p.terminate()
    p.join()
    for i in range(NUM_DAYS):
        if events[i]:
            date = get_date(i)
            result[date.strftime("%Y-%m-%d")] = events[i]
    return result
