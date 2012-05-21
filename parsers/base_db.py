


class BaseDbParser:
    """Base class for reading GPS data from a DB file"""

    def __init__(self, session):
        self.session = session
