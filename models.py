import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Person(db.Model):  
  __tablename__ = 'People'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String()))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean)
    shows = db.relationship('Show', backref="venue", lazy=True)

    def __repr__(self):
        return '<Venue {}>'.format(self.name)

class Artist(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    seeking_description = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    shows = db.relationship('Show', backref="artist", lazy=True)

    def __repr__(self):
        return '<Artist {}>'.format(self.name)

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Show {}{}>'.format(self.artist_id, self.venue_id)
