#!/usr/bin/python
'''
@author: Zack
@license: MIT
'''

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from importers.gpx import GPXImporter

if __name__ == '__main__':
    engine = sqlalchemy.create_engine('sqlite:///records_v03', echo=True)
    Sessionmaker = scoped_session(sessionmaker(bind=engine))
    imp = GPXImporter('Current.gpx', Sessionmaker)
    imp.save_gpx(1)
