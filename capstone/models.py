import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from config import database_config

#----------------------------------------------------------------------------#
# Database Setup 
#----------------------------------------------------------------------------#

#Heroku postgres databaes_path
database_path = os.environ['DATABASE_URL']
#local postgres database_path
#database_path = "postgres://{}:{}@{}:{}/{}".format(database_config['user_name'], database_config['password'], database_config['server_name'], database_config['port'],  database_config['database_name'])

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():   
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''initialize the database with some test data.''' 
    movie1 = (Movie(
      title = 'movie1',
      release_date = date.today()
    ))
    movie1.insert()

    movie2 = (Movie(
      title = 'movie2',
      release_date = date.today()
    ))
    movie2.insert()  

    actor1 = (Actor(
      name = 'actor1',
      gender = 'male',
      age = 33      
    ))
    actor1.movies = [movie1, movie2]
    actor1.insert()

    actor2 = (Actor(
      name = 'actor2',
      gender = 'female',
      age = 30      
    ))
    actor2.movies = [movie1]
    actor2.insert()

    actor3 = (Actor(
      name = 'actor3',
      gender = 'female',
      age = 27      
    ))
    actor3.movies = [movie2]
    actor3.insert()


#----------------------------------------------------------------------------#
# starring association N:N 
#----------------------------------------------------------------------------#

starring = db.Table('starring', db.Model.metadata,
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'))    
)

#----------------------------------------------------------------------------#
# Actors Model 
#----------------------------------------------------------------------------#

class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String(), nullable=False)
  gender = Column(db.String())
  age = Column(db.Integer)
  #movies = db.relationship('Movie', secondary=starring, backref=db.backref('actors', lazy='joined'))

  def __init__(self, name, gender, age):
    self.name = name
    self.gender = gender
    self.age = age

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name' : self.name,
      'gender': self.gender,
      'age': self.age
    }

#----------------------------------------------------------------------------#
# Movies Model 
#----------------------------------------------------------------------------#

class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(db.String())
  release_date = Column(db.Date)
  actors = db.relationship('Actor', secondary=starring, backref=db.backref('movies', lazy='joined'))

  def __init__(self, title, release_date) :
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title' : self.title,
      'release_date': self.release_date
    }
