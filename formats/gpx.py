'''
@author: Zack
@license: MIT
'''

from copy import deepcopy
import math

class Link:
    """Class for Gpx linkType"""
    def __init__(self, href=None, text=None, type=None):
        self.href = href
        self.text = text
        self.type = type


class Copyright:
    """Class for Gpx coopyrightType"""
    def __init__(self, author=None, year=None, license=None):
        self.author = author
        self.year = year
        self.license = license


class Author:
    """Class for Gpx personType"""
    def __init__(self, name=None, email=None, link=None):
        self.name = name
        self.email = email
        self.link = Link()


class Address:
    """Class fpr GPXX addressType"""
    def __init__(self, sa=None, city=None, state=None, country=None, zip=None):
        self.streetaddress = sa
        self.city = city
        self.state = state
        self.country = country
        self.postalcode = zip


class PhoneNumber:
    """Class for GPXX phonenumberType"""
    def __init__(self, number=None, category=None):
        self.number = number
        self.category = category


class Bounds:
    """Class for Gpx boundsType, with elevation data included"""
    def __init__(self, minlat=None, maxlat=None,
                       minlon=None, maxlon=None,
                       minele=None, maxele=None):
        self.minlat = minlat
        self.minlon = minlon
        self.minele = minele
        self.maxlat = maxlat
        self.maxlon = maxlon
        self.maxele = maxele


class Point:
    """Base class for waypoints, route points and segment points"""
    def __init__(self, lat=None, lon=None, ele=None):
        #Location
        self.lat = lat
        self.lon = lon
        self.ele = ele
        #GPX
        self.id = None
        self.time = None
        self.magvar = None
        self.geoidheight = None
        self.name = None
        self.cmt = None
        self.desc = None
        self.src = None
        self.link = Link()
        self.sym = None
        self.type = None
        self.fix = None
        self.sat = None
        self.hdop = None
        self.vdop = None
        self.pdop = None
        self.ageofdgpsdata = None
        self.dgpsid = None

    def distance_to_point(self, p2, ele=False):
        """Calcuate the distance between this point and another point"""
        #WGS84 mean value for earth's radius
        height = 6371009
        if ele:
            #If 3d distance is needed, add half the height difference to the
            #mean value. Provides a good enough approximation given the
            #typically small distances between points relative to the overall
            #size of Earth.
            height += math.fabs(p2.ele - self.ele)/2
        print self.lat, self.lon, p2.lat, p2.lon
        lat1 = math.radians(float(self.lat))
        lat2 = math.radians(float(p2.lat))
        lon1 = math.radians(float(self.lon))
        lon2 = math.radians(float(p2.lon))
        d_lat = lat2 - lat1
        d_lon = lon2 - lon1
        a = (math.sin(d_lat/2) * math.sin(d_lat/2) +
             math.cos(lat1) * math.cos(lat2) *
             math.sin(d_lon/2) * math.sin(d_lon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return height * c


class Path:
    """Base class for routes and track segments"""
    def __init__(self):
        self.id = None
        self.points = []

    def cleanup(self):
        """Loop through points, removing any with no data"""
        t = []
        for point in self.points:
            if point.lat and point.lon:
                t.append(point)
        self.points = t

    def get_times(self):
        """Get the start and end times. It is possible these values will not be
           from the first and last points, as points can have missing times."""
        start, end = None, None
        for point in self.points:
            if start is None or point.time < start:
                start = point.time
            if end is None or point.time > end:
                end = point.time
        return start, end

    def get_bounds(self):
        """Get the calculated bounds."""
        bounds = Bounds()
        for point in self.points:
            if point.lat is not None and point.lat < bounds.minlat:
                bounds.minlat = point.lat
            if point.lon is not None and point.lon < bounds.minlon:
                bounds.minlon = point.lon
            if point.ele is not None and point.ele < bounds.minele:
                bounds.minele = point.ele
            if point.lat is not None and point.lat > bounds.maxlat:
                bounds.maxlat = point.lat
            if point.lon is not None and point.lon > bounds.maxlon:
                bounds.maxlon = point.lon
            if point.ele is not None and point.ele > bounds.maxele:
                bounds.maxele = point.ele
        return bounds

    def get_length(self, use_ele=False):
        """Get the calculated distance."""
        length = 0
        old_point = None
        for point in self.points:
            if old_point:
                length += old_point.distance_to_point(point, use_ele)
            old_point = point
        return length

    def get_num_points(self):
        """Get the number of data points in this segment."""
        return len(self.points)

    def get_estimated_duration(self):
        """Calculate the total duration of the segment. Only an estimate, as it
           is possible that the segment may not have a full set of times."""
        duration = 0
        start, end = self.get_times()
        if start and end:
            duration = end - start
        return duration

    def get_location_by_time(self, time):
        """Calculate the position at a certain time. Should only return one."""
        start, end = self.get_times()
        if start and end:
            if start < time and end > time:
                lat, lon = self.calculate_location(time)
                if lat and lon:
                    return lat, lon
        return None, None

    def calculate_location(self, time):
        """Estimate location at a given time."""
        start_pt, end_pt = None, None
        for point in self.points:
            if point.time is time:
                #If exact match, return the point values
                return point.lat, point.lon
            if point.time and point.time < time:
                start_pt = point
            if not time and point.time and point.time > time:
                end_pt = point
        if not start_pt or not end_pt:
            #Don't attempt to calculate if we don't have start and end points
            return None
        #Calculated location assumes a straight path between both points.
        delta = float(time - start_pt.time) / (end_pt.time - start_pt.time)
        lat = start_pt.lat + ((end_pt.lat - startpt.lat) * delta)
        lon = start_pt.lon + ((end_pt.lon - startpt.lon) * delta)
        return lat, lon

    def get_outer_locations(self):
        """Determine the starting and ending points. In order for a point to be
            considered acceptable, it must contain both a lat and a lon. This
            means that in some cases the returned locations might not actually
            be the first point and last point."""
        slat, slon = None, None
        elat, elon = None, None
        for point in self.points:
            if point.lat and point.lon:
                slat = point.lat
                slon = point.lon
                break
        for point in reversed(self.points):
            if point.lat and point.lon:
                elat = point.lat
                elon = point.lon
                break
        return slat, slon, elat, elon

    def clone(self):
        return deepcopy(self)


class GpsDevice:
    """Class for GPS Devices"""
    def __init__(self, make=None, model=None, serial=None, purchase_date=None,
                 is_active=0, data_type=0, id=None):
        self.make = make
        self.model = model
        self.serial = serial
        self.purchase_date = purchase_date
        self.is_active = is_active
        self.data_type = data_type
        self.id = id


class Gpx:
    """Class for top-level GPX nodes"""
    def __init__(self):
        #gpxType Data
        self.creator = None
        self.version = None
        #Metadata
        self.name = None
        self.desc = None
        self.author = Author()
        self.copyright = Copyright()
        self.link = Link()
        self.time = None
        self.keywords = None
        self.bounds = Bounds()
        #Child Nodes
        self.waypoints = []
        self.tracks = []
        #Additional Data
        self.device = GpsDevice()
        self.id = None

    def cleanup(self):
        """Remove any empty tracks or track segments"""
        t = []
        for track in self.tracks:
            track.cleanup()
            if track.segments:
                t.append(track)
        self.tracks = t

    def get_times(self):
        """Get the start and end times."""
        start, end = None, None
        for track in tracks:
            s, e = track.get_times()
            if start is None or s < start:
                start = s
            if end is None or e > end:
                end = e
        return start, end

    def get_bounds(self):
        """Get the calculated bounds."""
        t = self.bounds
        if t.minlat and t.minlon and t.maxlat and t.maxlon:
            return self.bounds
        bounds = Bounds()
        for track in self.tracks:
            b = track.get_bounds()
            if b.minlat is not None and b.minlat < bounds.minlat:
                bounds.minlat = b.minlat
            if b.minlon is not None and b.minlon < bounds.minlon:
                bounds.minlon = b.minlon
            if b.minele is not None and b.minele < bounds.minele:
                bounds.minele = b.minele
            if b.maxlat is not None and b.maxlat > bounds.maxlat:
                bounds.maxlat = b.maxlat
            if b.maxlon is not None and b.maxlon > bounds.maxlon:
                bounds.maxlon = b.maxlon
            if b.maxele is not None and b.maxele > bounds.maxele:
                bounds.maxele = b.maxele
        return bounds

    def get_length(self, use_ele=False):
        """Get the calculated distance."""
        length = 0
        for track in self.tracks:
            length += track.get_length(use_ele)
        return length

    def get_num_points(self):
        """Determine the number of data points in this GPX instance."""
        num = 0
        for track in self.tracks:
            num += track.get_num_points()
        return num

    def get_estimated_duration(self):
        """Calculate the total duration of the GPX instance. Only an estimate,
            as it is possible that one or more segments may not have a full
            set of times."""
        duration = 0
        for track in self.tracks:
            duration += track.get_estimated_duration()
        return duration

    def get_location_by_time(self, time):
        """Calculate the position at a certain time. Should only return one."""
        for track in self.tracks:
            lat, lon = track.get_location_by_time(time)
            if lat and lon:
                return lat, lon
        return None, None

    def clone(self):
        return deepcopy(self)


class Waypoint(Point):
    """Class for GPX waypoints"""
    def __init__(self, lat=None, lon=None, ele=None):
        Point.__init__(self, lat, lon, ele)
        #GPXX
        self.gpxx_proximity = None
        self.gpxx_temperature = None
        self.gpxx_depth = None
        self.gpxx_displaymode = None
        self.gpxx_categories = None
        self.gpxx_address = Address()
        self.gpxx_phonenumber = PhoneNumber()


class Track:
    """Class for GPX tracks"""
    def __init__(self, name=None):
        self.name = name
        self.desc = None
        self.number = None
        self.segments = []
        self.id = None
        self.cmt = None
        self.src = None
        self.link = Link()
        self.type = None
        self.gpxx_displaycolor = None

    def cleanup(self):
        """Loop through segments, removing any with no points"""
        t = []
        for segment in self.segments:
            segment.cleanup()
            if segment.points:
                t.append(segment)
        self.segments = t

    def get_times(self):
        """Get the start and end times."""
        start, end = None, None
        for segment in self.segments:
            s, e = segment.get_times()
            if start is None or s < start:
                start = s
            if end is None or e > end:
                end = e
        return start, end

    def get_bounds(self):
        """Get the calculated bounds."""
        bounds = Bounds()
        for segment in self.segments:
            b = segment.get_bounds()
            if b.minlat is not None and b.minlat < bounds.minlat:
                bounds.minlat = b.minlat
            if b.minlon is not None and b.minlon < bounds.minlon:
                bounds.minlon = b.minlon
            if b.minele is not None and b.minele < bounds.minele:
                bounds.minele = b.minele
            if b.maxlat is not None and b.maxlat > bounds.maxlat:
                bounds.maxlat = b.maxlat
            if b.maxlon is not None and b.maxlon > bounds.maxlon:
                bounds.maxlon = b.maxlon
            if b.maxele is not None and b.maxele > bounds.maxele:
                bounds.maxele = b.maxele
        return bounds

    def get_length(self, use_ele=False):
        """Get the calculated distance."""
        length = 0
        for segment in self.segments:
            length += segment.get_length(use_ele)
        return length

    def get_num_points(self):
        """Determine the number of data points in this track instance."""
        num = 0
        for segment in self.segments:
            num += segment.get_num_points()
        return num

    def get_estimated_duration(self):
        """Calculate the total duration of the track instance. Only an estimate,
            as it is possible that one or more segments may not have a full
            set of times."""
        duration = 0
        for segment in self.segments:
            duration += segment.get_estimated_duration()
        return duration

    def get_location_by_time(self, time):
        """Calculate the position at a certain time. Should only return one."""
        for segment in self.segments:
            lat, lon = segment.get_location_by_time(time)
            if lat and lon:
                return lat, lon
        return None, None

    def get_outer_locations(self):
        """Determine the starting and ending points. In order for a point to be
            considered acceptable, it must contain both a lat and a lon. This
            means that in some cases the returned locations might not actually
            be the first point of the first segment and last point of the last
            segment."""
        slat, slon = None, None
        elat, elon = None, None
        for segment in tracks.segments:
            lat, lon = segment.get_start_location()
            if lat and lon:
                slat = lat
                slon = lon
                break
        for segment in reversed(tracks.segments):
            lat, lon = segment.get_end_location()
            if lat and lon:
                elat = lat
                elon = lon
                break
        return slat, slon, elat, elon

    def clone(self):
        return deepcopy(self)


class TrackSegment(Path):
    """Class for Gpx track segments"""
    def __init__(self):
        Path.__init__(self)


class SegmentPoint(Point):
    """Class for Gpx track segment points"""
    def __init__(self, lat=None, lon=None, ele=None):
        Point.__init__(self, lat, lon, ele)
        #GPXX
        self.gpxx_temperature = None
        self.gpxx_depth = None
