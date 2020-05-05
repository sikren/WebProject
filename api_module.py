# module works with Yandex Maps Static Api
import requests
from data import db_session
from data.offer import Offer


class StaticApi:
    api_link = "http://static-maps.yandex.ru/1.x/?"
    api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

    def __init__(self, lonlat, z=None):
        """lonlat; implied like a list
        for ex. [-81.692684, 12.508890]"""
        self.lonlat = lonlat
        self.z = 5 if z is None else z

    def set_z(self, z):
        self.z = z

    def get_map(self):
        session = db_session.create_session()

        lon, lat = self.lonlat

        # разброс долготы [-180; 180] => d(lon) = 360
        # для широты d(lat) = 180
        d_lon = 0.5 * (360 / 2 ** (self.z - 1))
        d_lat = 0.5 * (180 / 2 ** (self.z - 1))

        # фильтр меток по координатам карты
        tags = []
        for offer in session.query(Offer).filter(Offer.lon > lon - d_lon, Offer.lon < lon + d_lon,
                                                 Offer.lat > lat - d_lat, Offer.lat < lat + d_lat).all():
            tags.append(f"{offer.lon},{offer.lat},comma")

        parameters = {
            "apikey": self.api_key,
            "z": self.z,
            "ll": f"{lon},{lat}",
            "l": "map",
            "pt": "~".join(tags)
        }

        response = requests.get(self.api_link, params=parameters)
        if response:
            return response.url
        return None
