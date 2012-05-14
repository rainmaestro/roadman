'''
@author: Zack Townsend
@license: MIT
'''

from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class TableUserInfo(Base):
    '''userinfo table'''
    __tablename__ = 'userinfo'

    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    units_type = Column(Boolean)

    def __repr__(self):
        return "USER - id: %s, name: %s %s" % (self.id,  self.fname,  self.lname)

    def get_last_id(self,  session):
        return session.query(self).order_by(self.id.desc()).first()


class TableDevice(Base):
    '''GPS devices table'''
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    purchased = Column(String)
    model = Column(String)
    serial = Column(String)
    data_type = Column(Integer)

    def __repr__(self):
        return "DEVICE - id: %s, name: %s" % (self.id,  self.name)

    def get_last_id(self,  session):
        return session.query(self).order_by(self.id.desc()).first()


class TableTrack(Base):
    '''GPS tracks table'''
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer,  ForeignKey("devices.id"))
    name = Column(String)
    description = Column(String)
    time = Column(String)
    distance = Column(String)
    start_time = Column(String)
    start_lat = Column(String)
    start_lon = Column(String)
    end_time = Column(String)
    end_lat = Column(String)
    end_lon = Column(String)
    device = relationship("TableDevice",  backref=backref("tracks"))

    def __repr__(self):
        return "TRACK - id: %s, name: %s" % (self.id,  self.name)

    def get_last_id(self,  session):
        return session.query(self).order_by(self.id.desc()).first()


class TableTrackSegment(Base):
    '''GPS track segments table'''
    __tablename__ = 'track_segments'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer,  ForeignKey("tracks.id"))
    time = Column(String)
    distance = Column(String)
    start_time = Column(String)
    start_lat = Column(String)
    start_lon = Column(String)
    end_time = Column(String)
    end_lat = Column(String)
    end_lon = Column(String)
    track = relationship("TableTrack",  backref=backref("segments"))

    def __repr__(self):
        return "SEGMENT - id: %s, time: %s" % (self.id,  self.time)

    def get_last_id(self,  session):
        return session.query(self).order_by(self.id.desc()).first()


class TableSegmentPoint(Base):
    '''GPS track segment points table'''
    __tablename__ = 'segment_points'

    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer,  ForeignKey("track_segments.id"))
    time = Column(String)
    lat = Column(String)
    lon = Column(String)
    symbol = Column(String)
    comment = Column(String)
    segment = relationship("TableTrackSegment",  backref=backref("points"))

    def __repr__(self):
        return "POINT - id: %s, time: %s, lat/lon: %s/%s" % (
                    self.id,  self.time,  self.lat,  self.lon)

    def get_last_id(self,  session):
        return session.query(self).order_by(self.id.desc()).first()


class TableRoute(Base):
    '''GPS routes table'''
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer,  ForeignKey("devices.id"))
    name = Column(String)
    description = Column(String)
    time = Column(String)
    distance = Column(String)
    start_time = Column(String)
    start_lat = Column(String)
    start_lon = Column(String)
    end_time = Column(String)
    end_lat = Column(String)
    end_lon = Column(String)
    device = relationship("TableDevice",  backref=backref("routes"))

    def __repr__(self):
        return "ROUTE - id: %s, name: %s" % (self.id,  self.name)

    def get_last_id(self,  session):
        return session.query(self).order_by(self.id.desc()).first()


class TableRoutePoint(Base):
    '''GPS route points table'''
    __tablename__ = 'route_points'

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer,  ForeignKey("routes.id"))
    time = Column(String)
    lat = Column(String)
    lon = Column(String)
    symbol = Column(String)
    comment = Column(String)
    route = relationship("TableRoute",  backref=backref("points"))

    def __repr__(self):
        return "POINT - id: %s, time: %s, lat/lon: %s/%s" % (
                    self.id,  self.time,  self.lat,  self.lon)

    def get_last_id(self,  session):
        return session.query(self).order_by(self.id.desc()).first()


class TableWaypoint(Base):
    '''GPS waypoints table'''
    __tablename__ = 'waypoints'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lat = Column(String)
    lon = Column(String)
    symbol = Column(String)
    comment = Column(String)

    def __repr__(self):
        return "WAYPOINT - id: %s, name: %s, lat/lon: %s/%s" % (
                        self.id,  self.name,  self.lat,  self.lon)

    def get_last_id(self,  session):
        return session.query(self).order_by(self.id.desc()).first()
