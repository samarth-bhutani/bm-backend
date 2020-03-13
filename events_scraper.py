import json, re, requests
from datetime import datetime
import unidecode as u
from bs4 import BeautifulSoup

EVENTS_URL = "http://events.berkeley.edu/"

# Number of weeks of events to fetch
NUM_WEEKS = 3

def get_events_url(offset=0):
    """
    Get the event url of the current week or OFFSET weeks from now.

    Args:
        offset (int) - optional: how many weeks from now the event URL should represent
    Returns:
        (str) the page url of the events
    """
    now = datetime.now()

    url_p2 = "?view=summary&timeframe=week&date="
    curr_date = "{year}-{month}-{day}".format(year=now.year, month=now.month, day=now.day)
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


def parse_paragraphs(paragraphs, event_link, event):
    """
        Parses paragraph tags in an event row to populate description and labels fields in event.
        Args:
            paragraphs (list<bs4.element.Tag>) List of paragraphs in event row
            event_link (str) The attributes of an event link following 'events.berkeley.edu/'
                e.g. '?event_ID=132387&date=2020-03-29&filter=tab&filtersel=all_events'
            event (dict) The event JSON object
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
            if re.search('Sponsor', label.text):
                sponsors = p.find_all('a', href=True)
                labels["sponsors"] = {}
                for sponsor in sponsors:
                    sponsor_name = clean_str(sponsor.text)
                    labels["sponsors"][sponsor_name] = sponsor['href']
            elif re.search('Speaker', label.text):
                labels["speakers"] = clean_str(p.find(text=True, recursive=False))
            else:
                labels["other"] = clean_str(p.text)
        else:
            # Parse event description
            links = p.find_all('a', href=True)
            if links and links[-1]["href"] == event_link:
                # Event description is truncated and ends with 'More >'
                event["description"]["text"] = clean_str(p.text[0:-6])
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
        parse_paragraphs(paragraphs[1:], title["href"], event)
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
        url: (str) the page url of the events to fetch for a given week.
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
    result["events"] = get_events(get_events_url())
    print(json.dumps(result, indent=2))
    return result

scrape('placeholder')

