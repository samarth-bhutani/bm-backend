class Gym:
    def __init__(self, name, latitude, longitude, phone, picture, description, address, open, close, keycard=False):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.phone = phone
        self.picture = picture
        self.description = description
        self.address = address
        self.open = open
        self.close = close
        self.keycard = keycard
        self.id = None

class GymClass:
    def __init__(self):
        self.trainer = ""
        self.room = ""
        self.start_time = ""
        self.end_time = ""
        self.name = ""
        self.type = ""
