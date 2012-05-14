#!/usr/bin/python
'''
@author: Zack
@license: MIT
'''

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from importers.gpx import GPXImporter

engine = sqlalchemy.create_engine('sqlite:///records_v01', echo=True)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    imp = GPXImporter('Current.gpx', Session)
    imp.import_gpx(1)
