'''
@author: Zack
@license: LGPL
'''

from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class TableUserInfo(Base):
    '''userinfo table'''
    __tablename__ = 'userinfo'

    id = Column(Integer,  primary_key=True)
    fname = Column(String)
    lname = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    units_type = Column(Boolean)

    def __repr__(self):
        return "USER - id: %s, name: %s %s" % (self.id,  self.fname,  self.lname)

class TableDevice(Base):
    '''GPS devices table'''
    __tablename__ = 'devices'

