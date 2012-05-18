from xml.dom import minidom


class BaseXmlParser:
    """Base class for parsing XML data"""

    def __init__(self, file):
        self.raw_xml = minidom.parse(file)
