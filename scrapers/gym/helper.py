def convert_to_timestamp(time, day, month, year):
    
    hours = int(time.split(":")[0])
    mins = int(time.split(":")[1])
    
    if mins >= 60:
        mins = mins % 60
        hours += 1
    
    if hours >= 24:
        hours = hours % 24
        day += 1
    
    if month in [1,3,5,7,8,10,12]:
        if day > 31:
            day = day % 31
            month += 1
            
    elif month in [4,6,9,11]:
        if day > 30:
            day = day % 30
            month += 1
            
    elif month == 2:
        if day > 29 and year % 4 == 0 and (year%100 == 0 and year%400 == 0):
            day = day % 29
            month += 1
        
        elif day > 28:
            day = day % 28
            month += 1
    
    if month > 12:
        month = month % 13
        year += 1
    
    return "{0}-{1}-{2} {3}:{4}:00".format(
        str(year).zfill(4),
        str(month).zfill(2),
        str(day).zfill(2),
        str(hours).zfill(2),
        str(mins).zfill(2)
    )

def convert_to_timestamp_seconds(time, day, month, year):
    if ":" not in time:
        time = "00:00"
    
    import datetime, pytz
    timestamp = convert_to_timestamp(time, day, month, year)
    
    dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    tz = pytz.timezone('America/Los_Angeles')
    dt = tz.localize(dt)
    
    return dt.timestamp()
    
def convert_time_array_to_timestamp_array(open_time, close_time, start_date):
    import datetime
    from datetime import timedelta
    
    today = start_date
    
    values_open = []
    values_close = []
    
    for day_opens, day_closes in zip(open_time, close_time):
        if not isinstance(day_opens, list):
            day_opens = [day_opens]
            day_closes = [day_closes]
        
        values_day_open = []
        values_day_close = []
        
        for i, j in zip(day_opens, day_closes):
            if i == -1:
                values_day_open.append("Closed")
            elif ":" not in i:
                values_day_open.append(i)
            else:
                values_day_open.append(convert_to_timestamp_seconds(i, today.day, today.month, today.year))
            
            if j == -1:
                values_day_close.append("Closed")
            elif ":" not in j:
                values_day_close.append(j)
            else:
                values_day_close.append(convert_to_timestamp_seconds(j, today.day, today.month, today.year))
            
            today += timedelta(days=1)
        
        
        
        for o, c in zip(values_day_open, values_day_close):
            values_open.append(o)
            values_close.append(c)

        print("VO:" , values_open)
        print("VC:" , values_close)
    
    return values_open, values_close


def get_24_hr_time(time_string):
    if not("am" in time_string or "pm" in time_string):
        return time_string
    
    time_string = time_string.split(",")[0]
    
    is_am = time_string[-2:].lower() == "am"
    
    time_string = time_string.replace("am", "").replace("AM", "").replace("pm", "").replace("PM", "")
    time_string_data = time_string.split(":")
    time_string_data += [""]
    
    if is_am:
        return str((int(time_string_data[0]) % 12)).zfill(2) + ":" + str(time_string_data[1]).zfill(2)
    elif int(time_string_data[0]) > 12:
        return str(time_string_data[0]).zfill(2) + ":" + str(time_string_data[1]).zfill(2)
    else:
        return str(int(time_string_data[0]) + 12).zfill(2) + ":" + str(time_string_data[1]).zfill(2)
    

def get_last_sunday():
    import datetime
    
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7  # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
    sun = today - datetime.timedelta(idx)
    
    month = sun.strftime('%B')
    return sun, sun.day, month


def get_next_sunday():
    import datetime
    
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7  # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
    sun = today + datetime.timedelta(7 - idx)
    month = sun.strftime('%B')
    return sun, sun.day, month


def get_week_dates(sunday):
    import datetime
    from datetime import timedelta
    
    dates_array = []
    
    for i in range(7):
        dates_array.append(sunday + timedelta(days=i))
        
    return dates_array

def process_date_string(string_date):
    import datetime
    
    monthstring_to_number = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7,
                             "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    
    date_array = string_date.split(",")[1].strip().split(" ")
    month = monthstring_to_number[date_array[0]]
    day = int(date_array[1])
    year = datetime.date.today().year
    
    return datetime.date(year, month, day)


def fix_phone_number(phone):
    if phone is None:
        return
    
    phone = phone.replace("(", "")
    phone = phone.replace(")", "")
    phone = phone.replace("-", "")
    phone = phone.replace(" ", "")
    
    return "({0}) {1} - {2}".format(phone[:3], phone[3:6], phone[6:])