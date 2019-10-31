# ----------------------------------------------------------------------------------------------------------------------

# Date Retreival
'''
Gets the Sunday that happened during the start of this week. If today is a Monday/Tuesday..../Saturday, it would be
the Sunday before today. If it is Sunday today, it will return today.
'''
def get_last_sunday():
    import datetime
    
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7  # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
    sun = today - datetime.timedelta(idx)
    return sun

'''
Gets the Sunday that will happen during the start of next week. If today is a Monday/Tuesday..../Saturday, it would be 
the Sunday after today. If it is Sunday today, it will return next Sunday.
'''
def get_next_sunday():
    import datetime
    
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7  # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
    sun = today + datetime.timedelta(7 - idx)
    return sun

'''
Gets the entire week's worth of dates starting from get_last_sunday()
'''
def get_this_week_dates():
    sunday = get_last_sunday()
    from datetime import timedelta
    
    dates_array = []
    
    for i in range(7):
        dates_array.append(sunday + timedelta(days=i))
        
    return dates_array


'''
Gets the entire next week's worth of dates starting from get_next_sunday()
'''
def get_next_week_dates():
    sunday = get_next_sunday()
    from datetime import timedelta

    dates_array = []

    for i in range(7):
        dates_array.append(sunday + timedelta(days=i))

    return dates_array


'''
Gets the next seven days worth of dates starting from today
'''
def get_next_7_days():
    import datetime

    today = datetime.date.today()
    from datetime import timedelta

    dates_array = []

    for i in range(7):
        dates_array.append(today + timedelta(days=i))

    return dates_array


# ----------------------------------------------------------------------------------------------------------------------


# Data Manipulation Helpers
'''
The function takes in a timestring in AM/PM format (7am or 7:30pm or 17:00) and changes it to HH:MM format (17:00)
'''
def standarize_timestring(time_string):
    if not ("am" in time_string or "pm" in time_string):
        if ":" in time_string:
            return time_string
        elif "." in time_string:
            time_string = time_string.split(".")
            return time_string[0] + ":" + time_string[1]
        else:
            if len(time_string) == 3:
                return time_string[0] + ":" + time_string[-2:]
            return time_string[0:2] + ":" + time_string[-2:]

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

'''
Standardizes phone numbers to a (xxx) xxx - xxxx format; It has an optional parameter delimeters, which takes in an array of 
possible delimeters that can be used to to process the input. By default it is ["(", ")", "-", ".", " "]
'''
def fix_phone_number(phone, delimeters=["(", ")", "-", ".", " "]):
    if phone is None:
        return

    for deli in delimeters:
        phone = phone.replace(deli, "")

    return "({0}) {1} - {2}".format(phone[:3], phone[3:6], phone[6:])


# ----------------------------------------------------------------------------------------------------------------------


# Conversion Helpers
'''
Given a time, day, month and year, the function converts it to a datetime object timestamp
'''
def convert_to_timestamp(time, day, month, year):
    hours = int(time.split(":")[0])
    mins = int(time.split(":")[1])

    if mins >= 60:
        mins = mins % 60
        hours += 1

    if hours >= 24:
        hours = hours % 24
        day += 1

    if month in [1, 3, 5, 7, 8, 10, 12]:
        if day > 31:
            day = day % 31
            month += 1

    elif month in [4, 6, 9, 11]:
        if day > 30:
            day = day % 30
            month += 1

    elif month == 2:
        if day > 29 and year % 4 == 0 and (year % 100 == 0 and year % 400 == 0):
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

'''
Given a time, day, month and year, the function converts it to a POSIX timestamp; uses convert_to_timestamp in the conversion process
'''
def convert_to_posix(time, day, month, year):
    if ":" not in time:
        time = "00:00"

    import datetime, pytz
    timestamp = convert_to_timestamp(time, day, month, year)

    dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    tz = pytz.timezone('America/Los_Angeles')
    dt = tz.localize(dt)

    return dt.timestamp()


'''
Builds a POSIX-timestamp based interval object that adheres to BM Backend Standardization (ref-link:    ) 
Returns a tuple with opening time in POSIX format, closing time in POSIX format, notes about a place
'''
def build_time_interval(open, close, date, notes="", is_closed=False):
    if is_closed:
        return {"open_time":convert_to_posix("00:00", date.day, date.month, date.year),
            "close_time":convert_to_posix("00:00", date.day, date.month, date.year),
            "notes":notes}
    else:
        return {"open_time":convert_to_posix(open, date.day, date.month, date.year),
            "close_time":convert_to_posix(close, date.day, date.month, date.year),
            "notes":notes}


'''
Uses build_time_interval to convert an array of (open, close, date, notes) into format that adheres to BM Backend Standardization (ref-link:    )
'''
def convert_array_of_time_intervals(arr):
    return [build_time_interval(*x) for x in arr]
