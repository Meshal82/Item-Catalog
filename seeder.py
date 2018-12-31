from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import *

engine = create_engine('sqlite:///cars.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
user = User(
  name="meshal ahmed", email="meshal.8222@gmail.com")
session.add(user)
session.commit()
# Populate a category with cars for testing
car1 = Car(
  name="corvette", description="v8", category="sport", user_id=1)
session.add(car1)
session.commit()
car2 = Car(
  name="300 c ", description="v8", category="Sport", user_id=1)
session.add(car2)
session.commit()
car3 = Car(
  name="car", description="A car.", category="SUV", user_id=1)
session.add(car3)
session.commit()
car4 = Car(
  name="this is not my car", description="this is a description of a car .",
  category="SUV", user_id=0)
session.add(car4)
session.commit()
print "Database has been populated with fake data!"
