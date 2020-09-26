import requests
import json
import helper
from textwrap import wrap

def get_handshake_data():
    url = "https://berkeley.joinhandshake.com/events/unified_search?category=Event&ajax=true&including_all_facets_in_searches=true&page=1&per_page=25&sort_direction=asc&sort_column=default&is_posted_by_my_school=true&_=1600914896866"
    d = {
        "_ga":"GA1.2.685451758.1600914878",
        "_gid":"GA1.2.1882145345.1600914878",
         "_gat":'1',
        "ajs_anonymous_id":'%22611784bd-5a2f-463d-8546-c0e500531469%22',
        "_gcl_au":'1.1.791654829.1600914879',
        "_fbp=fb":'1.1600914878910.1941707510',
        "_gat_UA-58165706-1":'1',
        "production_auth_token":"b3Y3YUF0L045QUgwTnRaWjd1cTVrUWVPM1JpcTBReTA4VXlMR2JZT29lVVNNS2liS3lVM3BnTFZYUDlpbThZQWVyRGUwK2M5V2dGVDM2K210Z2dpZDdqR29BQy93NFhpRXFJbjQwYlNTdWtXQ3lkcjRDTVp0K1drbnkzQ1hrMEFSOUoyT0tMSEhiZVVOM04vTldMNVZnRnVqQ1ZpTWk4OGpmeTBiRWVJbDVOa1l1Qmt5ajF1aTVycTdNWUtnZmh0cHk3TWF1a3dDU084bnh4SUFBV0d1VVMwWnVEWmtpWmlLVlZpYVhnMkZUekNCM0NXSFZwMGFMV0VSMjRZdkdDYjFRd3ZXQ01NNjB0THVlMzJkN3pMWnNzTU40MFBHdnl1VWo0VExzeXFpTUJ4ZzJRU1RvQjZITTVzcXgwcDFlRFJkeDUvUzgvemtvejFYcXZmUTlqK1FkN3hyYVZ2RTFPZE91enpHc21mcVhSeXlCSWUwZS9SbnN0QnNTNEpDdFc0WjRJNUtZRjRZWUdoQ3cvQTArSmhFaXlOcStPOEt2OEVMZGRySHJkTkpUMDVaZTRJTW9PbFFQOWk4Rm93ZTV3Yi0tK0oyU0NaWitsU1NJcFY5R21ubFNuQT09--f2169d79acc13933b2dfb1c7671090a2aaafdf1a",
        "production_js_on":'true',
        "_gat_schoolTracker":'1',
        "ajs_user_id":'14477374',
        "_trajectory_session":"dWhjZ0U2VWxJNHpXRDh6djdhZ2xKRGpOMDFieVRwL3FqeVR1ZmJ6a1lZV0FVQVlYYnJpY1kwcWFoOFlxSEZBd2pITVZkY09mQkowRGkyOVRYYVhXeEhwVUhIV0lja3E4cUtJYXE2dUxoS2U5YUN3RnovajVuUmtZTkM4SysvRnVTdSt4TUlwM0J6TzRYd1pIWmVwb1Y1M2lXU29INjUvMzRHVWttQlNjZElma2p6QXJPdUllVS9FZ284QU5OenZSazZxYzdNZGQvNFBPTUJvRGNFaUxSUkR1aURQcFd6Ymhub2k5WkQrY1ltL2xRcGpRUnp2ZXBNOVNyY2lFYlNZTEJUaXBORVRWSy9mUHY3dTJCbnhKNk1nUXFaWWN0eTBwdzF1MjUxQW9hcms9LS1sUzZ5LzBFT2xLRE5xV1lrUGhQaWpnPT0%3D--b843cc8d713720869f6db3eb551497f28cc89ce0"
    }
    
    r = requests.get(url, cookies=d)
    result = r.text
    result = json.loads(result)
    array = result['results']

    JSON_array = []

    for i in array:

        event_dict = {}

        # Get Data
        name = i['name']
        link = "https://app.joinhandshake.com" + i['entity_path'] + "?ref=events-search"
        date = i['start_date'].split("T")[0].split("-")
        time = wrap(i['start_date'].split("T")[1],5)[0]
        
        #Convert date to POSIX
        date_posix = helper.convert_to_posix(time,int(date[2]),int(date[1]),int(date[0]))

        #Put in dictionary
        event_dict["name"] = name
        event_dict['link'] = link
        event_dict['date'] = date_posix

        #Append to array
        JSON_array.append(event_dict)
       

    return JSON_array
    

if __name__ == "__main__":
    get_handshake_data()

    
    