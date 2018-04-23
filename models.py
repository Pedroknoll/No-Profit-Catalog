"""Setup to create the projects database with the following:
    1. Category table
    2. Organization table"""

import sys
from getpass import getuser

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

DATABASE = {
    'drivername' : 'postgresql',
    'host' : '',
    'port' : '5432',
    'username' : '{}'.format(getuser()),
    'password' : '',
    'database' : 'noprofit'
    }

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(80), nullable = False)
    organizations = relationship("Organization", cascade="all, delete-orphan")


class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(80), nullable = False)
    description = Column(String(500), nullable = False)
    site = Column(String(2000))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)


engine = create_engine(URL(**DATABASE))
Base.metadata.create_all(engine)
