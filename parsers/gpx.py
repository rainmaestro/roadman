from parsers.base import BaseXmlParser
import formats.gpx as GPX

class GpxXmlParser(BaseXmlParser):
    """Parser for GPX-formatted XML"""
    data = None

    def __init__(self,  file):
        BaseXmlParser.__init__(self, file)
        self.gpx = GPX.Gpx()

    def parse(self):
        """Currently only parses a .gpx file."""
        self.__parse_raw_xml()
        return self.gpx

    def __parse_raw_xml(self):
        """Find the root 'gpx' node and pass it along."""
        nodes = self.raw_xml.childNodes
        for node in nodes:
            if node.nodeName == 'gpx':
                self.__parse_root_node(node)

    def __parse_root_node(self, root):
        """Parse the top-level 'gpx' node."""
        #version and creator are attributes, not child nodes
        if root.hasAttribute('creator'):
            self.gpx.creator = root.getAttribute('creator')
        if root.hasAttribute('version'):
            self.gpx.version = root.getAttribute('version')
        for node in root.childNodes:
            #Need to handle wpt, rte and trk separately
            if node.nodeName == 'wpt':
                self.__parse_wpt(node)
            elif node.nodeName == 'trk':
                self.__parse_trk(node)
            #Some Gpx data stored inside metadata instead of child nodes
            elif node.nodeName == 'metadata':
                self.__parse_metadata(node, self.gpx)
            elif node.nodeName == 'author':
                self.__parse_author(node, self.gpx)
            elif node.nodeName == 'copyright':
                self.__parse_copyright(node, self.gpx)
            elif node.nodeName == 'link':
                self.__parse_link(node, self.gpx)
            elif node.nodeName == 'bounds':
                self.__parse_bounds(node, self.gpx)
            #Failing all special cases, check attr against Gpx attr list
            elif hasattr(self.gpx, node.nodeName):
                setattr(self.gpx, node.nodeName, node.nodeValue)

    def __parse_bounds(self, node, obj):
        """Parse a bounds node."""
        b = GPX.Bounds()
        for (n, v) in node.attributes.items():
            if hasattr(b, n):
                setattr(b, n, v)
        obj.bounds = b

    def __parse_link(self, node, obj):
        """Parse a link node."""
        link = GPX.Link()
        if node.hasAttribute('href'):
            link.href = node.getAttribute('href')
        for n in node.childNodes:
            if hasattr(link, n.nodeName):
                setattr(link, n.nodeName, n.nodeValue)
        obj.link = link

    def __parse_copyright(self, node, obj):
        """Parse a copyright node."""
        copyright = GPX.Copyright()
        if node.hasAttribute('author'):
            copyright.author = node.getAttribute('author')
        for n in node.childNodes:
            if hasattr(copyright, n.nodeName):
                setattr(copyright, n.nodeName, n.nodeValue)
        obj.copyright = copyright

    def __parse_email(self, node, obj):
        """Parse an email node."""
        id = None
        domain = None
        if node.hasAttribute('id'):
            id = node.getAttribute('id')
        if node.hasAttribute('domain'):
            domain = node.getAttribute('domain')
        if id and domain:
            obj.email = id + '@' + domain

    def __parse_author(self, node, obj):
        """Parse an author node."""
        author = GPX.Author()
        for n in node.childNodes:
            if n.nodeName == 'name':
                author.name = n.nodeValue
            elif n.nodeName == 'email':
                self.__parse_email(author, n)
            elif n.nodeName == 'link':
                self.__parse_link(author, n)
        obj.author = author

    def __parse_metadata(self, node, obj):
        """Parse metadata node."""
        #Some Gpx data stored inside metadata instead of child nodes
        for n in node.childNodes:
            if n.nodeName == 'author':
                self.__parse_author(n, obj)
            elif n.nodeName == 'copyright':
                self.__parse_copyright(n, obj)
            elif n.nodeName == 'link':
                self.__parse_link(n, obj)
            elif n.nodeName == 'bounds':
                self.__parse_bounds(n, obj)
            #Failing all special cases, check attr against Gpx attr list
            elif hasattr(obj, n.nodeName):
                setattr(obj, n.nodeName, n.nodeValue)

    def __parse_wpt(self, node):
        """Parse waypoint node."""
        wpt = GPX.Waypoint()
        if node.hasAttribute('lat'):
            wpt.lat = node.getAttribute('lat')
        if node.hasAttribute('lon'):
            wpt.lon = node.getAttribute('lon')
        for n in node.childNodes:
            if n.nodeName == 'link':
                self.__parse_link(n, wpt)
            elif n.nodeName == 'extensions':
                self.__parse_wpt_extensions(n, wpt)
            elif hasattr(wpt, n.nodeName):
                setattr(wpt, n.nodeName, n.nodeValue)
        if wpt.lat and wpt.lon:
            self.gpx.waypoints.append(wpt)

    def __parse_wpt_extensions(self, node, wpt):
        """Parse waypoint extensions node."""
        for c in node.childNodes:
            #Parse the GPXX WaypointExtensions node
            if c.nodeName == 'gpxx:WaypointExtension':
                self.__parse_wpt_gpxx_extensions(c, wpt)

    def __parse_wpt_gpxx_extensions(self, node, wpt):
        """Parse GPXX-specific waypoint extensions."""
        for n in node.childNodes:
            if n.nodeName == 'gpxx:Proximity':
                wpt.gpxx_proximity = n.nodeValue
            elif n.nodeName == 'gpxx:Temperature':
                wpt.gpxx_temperature = n.nodeValue
            elif n.nodeName == 'gpxx:Depth':
                wpt.gpxx_depth = n.nodeValue
            elif n.nodeName == 'gpxx:DisplayMode':
                wpt.gpxx_displaymode = n.nodeValue
            elif n.nodeName == 'gpxx:Categories':
                wpt.gpxx_categories = n.nodeValue
            elif n.nodeName == 'gpxx:Address':
                address = GPX.Address()
                if n.childNodes:
                    for c in n.childNodes:
                        #Get text following 'gpxx:' in lowercase format
                        name = c.nodeName.split(':')[1].lower()
                        if hasattr(address, name):
                            setattr(address, name, c.nodeValue)
                    wpt.gpxx_address = address
            elif n.nodeName == 'gpxx:PhoneNumber':
                phone = GPX.PhoneNumber()
                if n.hasAttribute('Category'):
                    phone.category = n.getAttribute('Category')
                phone.number = n.nodeValue
                wpt.gpxx_phonenumber = phone

    def __parse_trk(self, node):
        """Parse track."""
        track = GPX.Track()
        for n in node.childNodes:
            if n.nodeName == 'link':
                self.__parse_link(n, track)
            elif n.nodeName == 'extensions':
                self.__parse_trk_extensions(n, track)
            elif n.nodeName == 'trkseg':
                self.__parse_trkseg(n, track)
            elif hasattr(track, n.nodeName):
                setattr(track, n.nodeName, n.nodeValue)
        track.cleanup()
        if track.segments:
            self.gpx.tracks.append(track)

    def __parse_trk_extensions(self, node, track):
        """Parse track extensions"""
        for c in node.childNodes:
            #Parse the GPXX TrackExtension node
            if c.nodeName == 'gpxx:TrackExtension':
                self.__parse_trk_gpxx_extensions(c, track)

    def __parse_trk_gpxx_extensions(self, node, track):
        """Parse GPXX-specific track extensions."""
        for n in node.childNodes:
            if n.nodeName == 'gpxx:DisplayColor':
                track.gpxx_displaycolor = n.nodeValue

    def __parse_trkseg(self, node, track):
        """Parse track segment"""
        trkseg = GPX.TrackSegment()
        for n in node.childNodes:
            if n.nodeName == 'trkpt':
                self.__parse_trkseg_pt(n, trkseg)
            elif n.nodeName == 'extensions':
                self.__parse_trkseg_extensions(n, trkseg)
            elif hasattr(trkseg, n.nodeName):
                setattr(trkseg, n.nodeName, n.nodeValue)
        track.segments.append(trkseg)

    def __parse_trkseg_extensions(self, node, trkseg):
        """Parse track segment extensions"""
        for c in node.childNodes:
            if hasattr(trkseg, c.nodeName):
                setattr(trkseg, c.nodeName, c.nodeValue)

    def __parse_trkseg_pt(self, node, trkseg):
        """Parse track segment point."""
        trkpt = GPX.SegmentPoint()
        if node.hasAttribute('lat'):
            trkpt.lat = node.getAttribute('lat')
        if node.hasAttribute('lon'):
            trkpt.lon = node.getAttribute('lon')
        for n in node.childNodes:
            if n.nodeName == 'link':
                self.__parse_link(n, trkpt)
            elif n.nodeName == 'extensions':
                self.__parse_trkseg_pt_extensions(n, trkpt)
            elif hasattr(trkpt, n.nodeName):
                setattr(trkpt, n.nodeName, n.nodeValue)
        if trkpt.lat and trkpt.lon:
            trkseg.points.append(trkpt)

    def __parse_trkseg_pt_extensions(self, node, trkpt):
        """Parse track point extensions node."""
        for c in node.childNodes:
            #Parse the GPXX TrackPointExtension node
            if c.nodeName == 'gpxx:TrackPointExtension':
                self.__parse_trkseg_pt_gpxx_extensions(c, trkpt)

    def __parse_trkseg_pt_gpxx_extensions(self, node, trkpt):
        """Parse GPXX-specific track point extensions."""
        for n in node.childNodes:
            if n.nodeName == 'gpxx:Temperature':
                trkpt.gpxx_temperature = n.nodeValue
            elif n.nodeName == 'gpxx:Depth':
                trkpt.gpxx_depth = n.nodeValue
