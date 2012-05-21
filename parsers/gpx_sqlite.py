from backend.sqlite import *
from parsers.base_db import BaseDbParser
from formats.gpx import Gpx

class GpxSqliteParser(BaseDbParser):
    """Populate GPX instance from am SQLite database"""
    def __init__(self, session):
        BaseDbParser.__init__(self, session)
        self.gpxs = []

    def parse(self):
        self.__parse()
        return self.gpxs

    def __parse(self):
        gpxs = self.session.query(TableGpx)
        if gpxs is None:
            return None
        for g in gpxs:
            self.__parse_gpx(g)

    def __parse_gpx(self, g):
        gpx = Gpx()
        gpx.id = g.id
        gpx.version = g.version
        gpx.creator = g.creator
        gpx.name = g.name
        gpx.desc = g.desc
        gpx.author.name = g.author_name
        gpx.author.email = g.author_email
        gpx.author.link.href = g.author_link_href
        gpx.author.link.text = g.author_link_text
        gpx.author.link.type = g.author_link_type
        gpx.copyright.author = g.copyright_author
        gpx.copyright.year = g.copyright_year
        gpx.copyright.license = g.copyright_license
        gpx.link.href = g.link_href
        gpx.link.text = g.link_text
        gpx.link.type = g.link_type
        gpx.time = g.time
        gpx.keywords = g.keywords
        gpx.bounds.minlat = g.bounds_minlat
        gpx.bounds.minlon = g.bounds_minlon
        gpx.bounds.maxlat = g.bounds_maxlat
        gpx.bounds.maxlon = g.bounds_maxlon
        gpx.device.id = g.device.id
        gpx.device.make = g.device.make
        gpx.device.model = g.device.model
        gpx.device.serial = g.device.serial
        gpx.device.purchase_date = g.device.purchase_date
        gpx.device.is_active = g.device.is_active
        gpx.device.data_type = g.device.data_type
        for w in g.waypoints:
            gpx.waypoints.append(self.__parse_waypoint(g.id, w))
        for t in g.tracks:
            gpx.tracks.append(self.__parse_tracks(g.id, t))
        gpx.cleanup()
        return gpx

    def __parse_waypoint(self, gpx_id, w):
        wpt = WayPoint()
        wpt.id = w.id
        wpt.gpx_id = w.gpx_id
        wpt.lat = w.lat
        wpt.lon = w.lon
        wpt.ele = w.ele
        wpt.time = w.time
        wpt.magvar = w.magvar
        wpt.geoidheight = w.geoidheight
        wpt.name = w.name
        wpt.cmt = w.cmt
        wpt.desc = w.desc
        wpt.link.href = w.link_href
        wpt.link.text = w.link_text
        wpt.link.type = w.link_type
        wpt.sym = w.sym
        wpt.type = w.type
        wpt.fix = w.fix.value
        wpt.sat = w.sat
        wpt.hdop = w.hdop
        wpt.vdop = w.vdop
        wpt.pdop = w.pdop
        wpt.ageofdgpsdata = w.ageofdgpsdata
        wpt.dgpsid = w.dgpsid
        wpt.gpxx_proximity = w.gpxx_proximity
        wpt.gpxx_temperature = w.gpxx_temperature
        wpt.gpxx_depth = w.gpxx_depth
        wpt.gpxx_displaymode = w.displaymode.value
        wpt.gpxx_categories = w.gpxx_categories
        wpt.gpxx_address.streetaddress = w.gpxx_address_streetaddress
        wpt.gpxx_address.city = w.gpxx_address_city
        wpt.gpxx_address.state = w.gpxx_address_state
        wpt.gpxx_address.country = w.gpxx_address_country
        wpt.gpxx_address.postalcode = w.gpxx_address_postalcode
        wpt.gpxx_phonenumber.number = w.gpxx_phonenumber
        wpt.gpxx_phonenumber.category = w.gpxx_phonenumber_category
        return wpt

    def __parse_tracks(self, gpx_id, t):
        trk = Track()

        return trk
