import math, pprint

R = 6378100  # radius of the earth in m

def deg2rad(d):
    return d * math.pi / 180

def distance(lat1, lon1, lat2, lon2):
    # https://stackoverflow.com/a/27943

    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
        math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * \
        math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
    return R * c    # distance in m


class Event:
    def __init__(self, name, type, lat, lon, time = -1):
        self.name = name
        self.type = type
        self.lat = float(lat)
        self.lon = float(lon)
        self.time = time


class City(Event):
    def __init__(self, name, lat, lon):
        super().__init__(name, "city", lat, lon, -1)


class Earthquake(Event):
    def __init__(self, name, lat, lon, time):
        super().__init__(name, "earthquake", lat, lon, time)


class Volcano(Event):
    def __init__(self, name, lat, lon, time):
        super().__init__(name, "volcano", lat, lon, time)


class Geyser(Event):
    def __init__(self, name, lat, lon, time):
        super().__init__(name, "geyser", lat, lon, time)


class Hotspring(Event):
    def __init__(self, name, lat, lon):
        super().__init__(name, "hotspring", lat, lon, -1)


class Fumarole(Event):
    def __init__(self, name, lat, lon):
        super().__init__(name, "fumarole", lat, lon, -1)

##################################################################

class EventManager:
    def __init__(self, eventList):
        self.events = []
        for event in eventList:
            self.events.append(self._parse_event(event))

    def _parse_event(self, event):
        name, type, lat, lon, time = event.split(":")
        return Event(name, type, float(lat), float(lon), time)

    def add_event(self, event: Event):
        self.events.append(event)

    def findEventsNear(self, lat, lon, maxDist=5000):
        nearby = []

        for event in self.events:
            dist = distance(lat, lon, event.lat, event.lon)
            if dist < maxDist:
                nearby.append(f"{event.name}:{event.type}:{event.lat}:{event.lon}:{event.time}")
        return nearby

    def findEarthquakesNear(self, cityName):
        cityRecord = None

        for event in self.events:
            if event.type == "city" and event.name == cityName:
                cityRecord = event

        if cityRecord is None:
            return None

        earthquakes = []

        for event in self.events:
            if event.type == "earthquake":
                dist = distance(event.lat, event.lon, cityRecord.lat, cityRecord.lon)
                if dist < 5000:
                    earthquakes.append(f"{event.name}:{event.type}:{event.lat}:{event.lon}:{event.time}")
        return earthquakes


    def addVolcanoEvent(self, name, lat, lon, time):
        self.add_event(Volcano(name, lat, lon, time))

    def addEarthquakeEvent(self, name, lat, lon, time):
        self.add_event(Earthquake(name, lat, lon, time))

    def addGeyser(self, name, lat, lon, time):
        self.add_event(Geyser(name, lat, lon, time))

    def addHotspring(self, name, lat, lon):
        self.add_event(Hotspring(name, lat, lon))

    def addFumarole(self, name, lat, lon):
        self.add_event(Fumarole(name, lat, lon))

    def addCity(self, name, lat, lon):
        self.add_event(City(name, lat, lon))

starting_events = [
    "some volcano:volcano:40.12120:-121.3455:21451",
    "some earthquake:earthquake:40.51230:-121.23425:87153",
    "another earthquake:earthquake:39.23890:-120.23985:17354",
    "yet another earthquake:earthquake:39.23223:-120.23125:16524",
    "another volcano:volcano:43.32890:-122.3289:23856",
    "a geyser:geyser:39.23223:-120.23125:-1",
    "Townville:city:44.05645:-121.30812:-1"
]

em = EventManager(starting_events)

em.addHotspring("my favorite hotspring", 46.1231, -115.23234)
em.addCity("Cityton", 40.5232, -121.23453)
em.addVolcanoEvent("yet another volcano", 15.52232, -107.03521, 256923)

x = em.findEventsNear(40.5, -121.2, 163000)
pprint.pprint(x)

print("------------------------")

x = em.findEarthquakesNear("Cityton")
pprint.pprint(x)