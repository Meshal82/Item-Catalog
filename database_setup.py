import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# class to store user info
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


# class for cars Database
class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(), nullable=False)
    category = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    picture = Column(String(250))

    @property
    def serialize(self):
        # return a car data in serializable format
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category
        }


engine = create_engine('sqlite:///cars.db')
Base.metadata.create_all(engine)
