'''
@author: Zack Townsend
@license: MIT
'''

from parsers.gpx import GpxXmlParser
from backend.sqlite import *

#Session = sessionmaker()


class GPXImporter:
    """Import data from GPX files. Currently supports v1.1 only."""
    def __init__(self, file, sessionmaker):
        self.session = sessionmaker()
        f = open(file)
        parser = GpxXmlParser(f)
        f.close()
        self.gpx = parser.parse()
        self.gpx.cleanup()
        print self.gpx.link

    def save_gpx(self, device_id):
        g = self.create_new_gpx(self.gpx, device_id)
        print g.creator
        self.session.add(g)
        self.session.flush()
        for track in self.gpx.tracks:
            t = self.create_new_track(track, g.id)
            self.session.add(t)
            self.session.flush()
            for segment in track.segments:
                s = self.create_new_segment(t.id, segment)
                self.session.add(s)
                self.session.flush()
                for point in segment.points:
                    p = self.create_new_segment_point(s.id, point)
                    self.session.add(p)
        for waypoint in self.gpx.waypoints:
            if self.session.query(TableWaypoint).filter(TableWaypoint.lat==waypoint.lat).filter(TableWaypoint.lon==waypoint.lon).first() is None:
                w = self.create_new_waypoint(waypoint, g.id)
                self.session.add(w)
        self.session.commit()

    def create_new_gpx(self, gpx, device_id):
        t = TableGpx()
        t.device_id = device_id
        t.version = gpx.version
        t.creator = gpx.creator
        t.name = gpx.name
        t.desc = gpx.desc
        t.author_name = gpx.author.name
        t.author_email = gpx.author.email
        t.author_link_href = gpx.author.link.href
        t.author_link_text = gpx.author.link.text
        t.author_link_type = gpx.author.link.type
        t.copyright_author = gpx.copyright.author
        t.copyright_year = gpx.copyright.year
        t.copyright_license = gpx.copyright.license
        t.link_href = gpx.link.href
        t.link_text = gpx.link.text
        t.link_type = gpx.link.type
        t.time = gpx.time
        t.keywords = gpx.keywords
        t.bounds_minlat = gpx.bounds.minlat
        t.bounds_minlon = gpx.bounds.minlon
        t.bounds_maxlat = gpx.bounds.maxlat
        t.bounds_maxlon = gpx.bounds.maxlon
        return t

    def create_new_track(self, track, gpxid):
        t = TableTrack()
        t.name = track.name
        t.gpx_id = gpxid
        t.desc = track.desc
        t.cmt = track.cmt
        t.src = track.src
        t.link_href = track.link.href
        t.link_text = track.link.text
        t.link_type = track.link.type
        t.number = track.number
        t.type = track.type
        #TODO: Pull from Table
        t.gpxx_display_color_id = None
        return t

    def create_new_segment(self, trkid, segment):
        s = TableTrackSegment()
        s.track_id = trkid
        return s

    def create_new_segment_point(self, segid, point):
        p = TableSegmentPoint()
        p.segment_id = segid
        p.lat = point.lat
        p.lon = point.lon
        p.ele = point.ele
        p.time = point.time
        p.magvar = point.magvar
        p.geoidheight = point.geoidheight
        p.name = point.name
        p.cmt = point.cmt
        p.desc = point.desc
        p.link_href = point.link.href
        p.link_name = point.link.text
        p.link_type = point.link.type
        p.sym = point.sym
        p.type = point.type
        #TODO: Pull from Table
        p.fix_id = None
        p.sat = point.sat
        p.hdop = point.hdop
        p.vdop = point.vdop
        p.pdop = point.pdop
        p.ageofdgpsdata = point.ageofdgpsdata
        p.dgpsid = point.dgpsid
        p.gpxx_temperature = point.gpxx_temperature
        p.gpxx_depth = point.gpxx_depth
        return p

    def create_new_waypoint(self, waypoint, gpxid):
        w = TableWaypoint()
        w.gpx_id = gpxid
        w.lat = waypoint.lat
        w.lon = waypoint.lon
        w.ele = waypoint.ele
        w.time = waypoint.time
        w.magvar = waypoint.magvar
        w.geoidheight = waypoint.geoidheight
        w.name = waypoint.name
        w.cmt = waypoint.cmt
        w.desc = waypoint.desc
        w.link_href = waypoint.link.href
        w.link_name = waypoint.link.text
        w.link_type = waypoint.link.type
        w.sym = waypoint.sym
        w.type = waypoint.type
        #TODO: Pull from Table
        w.fix_id = None
        w.sat = waypoint.sat
        w.hdop = waypoint.hdop
        w.vdop = waypoint.vdop
        w.pdop = waypoint.pdop
        w.ageofdgpsdata = waypoint.ageofdgpsdata
        w.dgpsid = waypoint.dgpsid
        w.gpxx_temperature = waypoint.gpxx_temperature
        w.gpxx_depth = waypoint.gpxx_depth
        w.gpxx_proximity = waypoint.gpxx_proximity
        #TODO: Pull from Table
        w.gpxx_displaymode_id = None
        w.gpxx_categories = waypoint.gpxx_categories
        w.gpxx_address_streetaddress = waypoint.gpxx_address.streetaddress
        w.gpxx_address_city = waypoint.gpxx_address.city
        w.gpxx_address_state = waypoint.gpxx_address.state
        w.gpxx_address_country = waypoint.gpxx_address.country
        w.gpxx_address_postalcode = waypoint.gpxx_address.postalcode
        w.gpxx_phonenumber = waypoint.gpxx_phonenumber.number
        w.gpxx_phonenumber_category = waypoint.gpxx_phonenumber.category
        return w
