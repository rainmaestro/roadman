'''
@author: Zack Townsend
@license: MIT
'''

from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class TableUserInfo(Base):
    """Table for storing user data"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    units_type = Column(Boolean)

    def __repr__(self):
        return "USER - id: %s, name: %s %s" % (self.id, self.fname, self.lname)


class TableFix(Base):
    """Table for storing GPS fix values"""
    __tablename__ = 'fixes'

    id = Column(Integer, primary_key=True)
    value = Column(String)

    def __repr__(self):
        return "FIX - id: %s, value: %s" % (self.id, self.value)


class TableGpxxDisplayMode(Base):
    """Table for storing allowed GPXX display modes (Garmin extension)"""
    __tablename__ = 'gpxx_displaymodes'

    id = Column(Integer, primary_key=True)
    value = Column(String)

    def __repr__(self):
        return "GPXX_DISPLAYMODE - id: %s, value: %s" % (self.id, self.value)


class TableGpxxDisplayColor(Base):
    """Table for storing allowed GPXX display colors (Garmin extension)"""
    __tablename__ = 'gpxx_displaycolors'

    id = Column(Integer, primary_key=True)
    value = Column(String)

    def __repr__(self):
        return "GPXX_DISPLAYCOLOR - id: %s, value: %s" % (self.id, self.value)


class TableDevice(Base):
    """Table for storing GPS Device info"""
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    make = Column(String)
    model = Column(String)
    serial = Column(String)
    purchase_date = Column(Date)
    is_active = Column(Boolean)
    data_type = Column(Integer)

    def __repr__(self):
        return "DEVICE - id: %s, make/model: %s/%s" % (self.id, self.make, self.model)


class TableTrack(Base):
    """Table for storing GPS Track records"""
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    gpx_id = Column(Integer, ForeignKey("gpxs.id"))
    name = Column(String)
    cmt = Column(String)
    desc = Column(String)
    src = Column(String)
    link_href = Column(String)
    link_text = Column(String)
    link_type = Column(String)
    number = Column(Integer)
    type = Column(String)
    gpxx_displaycolor_id = Column(Integer, ForeignKey("gpxx_displaycolors.id"))
    device = relationship("TableGpx", backref=backref("tracks"))
    displaycolor = relationship("TableGpxxDisplayColor")

    def __repr__(self):
        return "TRACK - id: %s, name: %s" % (self.id,  self.name)


class TableTrackSegment(Base):
    """Table for storing track segment data"""
    __tablename__ = 'track_segments'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer,  ForeignKey("tracks.id"))
    track = relationship("TableTrack",  backref=backref("segments"))

    def __repr__(self):
        return "SEGMENT - id: %s, time: %s" % (self.id,  self.time)


class TableSegmentPoint(Base):
    """Table for storing segment points data"""
    __tablename__ = 'segment_points'

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer,  ForeignKey("track_segments.id"))
    lat = Column(String)
    lon = Column(String)
    ele = Column(String)
    time = Column(String)
    magvar = Column(String)
    geoidheight = Column(String)
    name = Column(String)
    cmt = Column(String)
    desc = Column(String)
    link_href = Column(String)
    link_text = Column(String)
    link_type = Column(String)
    sym = Column(String)
    type = Column(String)
    fix_id = Column(Integer, ForeignKey("fixes.id"))
    sat = Column(Integer)
    hdop = Column(String)
    vdop = Column(String)
    pdop = Column(String)
    ageofdgpsdata = Column(String)
    dgpsid = Column(Integer)
    gpxx_temperature = Column(String)
    gpxx_depth = Column(String)
    segment = relationship("TableTrackSegment",  backref=backref("points"))
    fix = relationship("TableFix")

    def __repr__(self):
        return "POINT - id: %s, time: %s, lat/lon: %s/%s" % (
                    self.id,  self.time,  self.lat,  self.lon)


class TableWaypoint(Base):
    """Table for storing waypoints data"""
    __tablename__ = 'waypoints'

    id = Column(Integer, primary_key=True)
    gpx_id = Column(Integer,  ForeignKey("gpxs.id"))
    lat = Column(String)
    lon = Column(String)
    ele = Column(String)
    time = Column(String)
    magvar = Column(String)
    geoidheight = Column(String)
    name = Column(String)
    cmt = Column(String)
    desc = Column(String)
    link_href = Column(String)
    link_text = Column(String)
    link_type = Column(String)
    sym = Column(String)
    type = Column(String)
    fix_id = Column(Integer, ForeignKey("fixes.id"))
    sat = Column(Integer)
    hdop = Column(String)
    vdop = Column(String)
    pdop = Column(String)
    ageofdgpsdata = Column(String)
    dgpsid = Column(Integer)
    gpxx_proximity = Column(String)
    gpxx_temperature = Column(String)
    gpxx_depth = Column(String)
    gpxx_displaymode_id = Column(Integer, ForeignKey("gpxx_displaymodes.id"))
    gpxx_categories = Column(String)
    gpxx_address_streetaddress = Column(String)
    gpxx_address_city = Column(String)
    gpxx_address_state = Column(String)
    gpxx_address_country = Column(String)
    gpxx_address_postalcode = Column(String)
    gpxx_phonenumber = Column(String)
    gpxx_phonenumber_category = Column(String)
    segment = relationship("TableGpx",  backref=backref("waypoints"))
    fix = relationship("TableFix")
    displaymode = relationship("TableGpxxDisplayMode")

    def __repr__(self):
        return "WAYPOINT - id: %s, time: %s, lat/lon: %s/%s" % (
                    self.id,  self.time,  self.lat,  self.lon)


class TableGpx(Base):
    """Table for storing GPX data"""
    __tablename__ = 'gpxs'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer,  ForeignKey("devices.id"))
    version = Column(String)
    creator = Column(String)
    name = Column(String)
    desc = Column(String)
    author_name = Column(String)
    author_email = Column(String)
    author_link_href = Column(String)
    author_link_text = Column(String)
    author_link_type = Column(String)
    copyright_author = Column(String)
    copyright_year = Column(String)
    copyright_license = Column(String)
    link_href = Column(String)
    link_text = Column(String)
    link_type = Column(String)
    time = Column(Date)
    keywords = Column(String)
    bounds_minlat = Column(String)
    bounds_minlon = Column(String)
    bounds_maxlat = Column(String)
    bounds_maxlon = Column(String)
    segment = relationship("TableDevice",  backref=backref("gpxs"))

    def __repr__(self):
        return "GPX - id: %s, name: %s" % (self.id,  self.name)
