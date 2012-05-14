'''
@author: Zack Townsend
@license: MIT
'''

from sqlalchemy.orm import sessionmaker

from backend.sqlite import TableTrack,  TableTrackSegment,  TableSegmentPoint
from gpxpy.parser import GPXParser

Session = sessionmaker()


class GPXImporter:
    def __init__(self, file, Session):
        self.session = Session()
        f = open(file)
        parser = GPXParser(f)
        self.gpx = parser.parse()
        self.gpx.remove_empty()
        f.close()

    def import_gpx(self, device_id):
        print len(self.gpx.tracks)
        for track in self.gpx.tracks:
            if self.session.query(TableTrack).filter(TableTrack.name==track.name).first() is None:
                t = self.create_new_track(track, device_id)
                self.session.add(t)
                for segment in track.segments:
                    s = self.create_new_segment(t, segment)
                    self.session.add(s)
                    for point in segment.points:
                        p = self.create_new_point(s, point)
                        self.session.add(p)
        self.session.commit()


    def create_new_track(self, track, device_id):
        t = TableTrack()
        t.name = track.name
        t.device_id = device_id
        t.description = None
        t.start_time,  t.end_time = track.get_time_bounds()
        t.time = track.get_duration()
        t.distance = track.length_2d()
        t.start_lat = track.segments[0].points[0].latitude
        t.start_lon = track.segments[0].points[0].longitude
        t.end_lat = track.segments[-1].points[-1].latitude
        t.end_lon = track.segments[-1].points[-1].longitude
        return t

    def create_new_segment(self, track, segment):
        s = TableTrackSegment()
        s.track_id = track.id
        s.start_time,  s.end_time = segment.get_time_bounds()
        s.time = segment.get_duration()
        s.distance = segment.length_2d()
        s.start_lat = segment.points[0].latitude
        s.start_lon = segment.points[0].longitude
        s.end_lat = segment.points[-1].latitude
        s.end_lon = segment.points[-1].longitude
        return s

    def create_new_point(self, segment, point):
        p = TableSegmentPoint()
        p.segment_id = segment.id
        p.time = point.time
        p.lat = point.latitude
        p.lon = point.longitude
        p.symbol = point.symbol
        p.comment = point.comment
        return p
