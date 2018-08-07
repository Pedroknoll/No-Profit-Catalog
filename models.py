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


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(80), nullable = False)
    organizations = relationship("Organization", cascade="all, delete-orphan")


class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(80), nullable = False)
    description = Column(String(1000), nullable = False)
    site = Column(String(2000))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'site': self.site,
            'category_id': self.category_id,
        }


engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.create_all(engine)
