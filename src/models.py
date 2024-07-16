from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum

db = SQLAlchemy()

class Gender(PyEnum):
    FEMALE = "Female"
    MALE = "Male"
    UNDEFINED = "Undefined"

class Specie(PyEnum):
    HUMAN = "Human"
    ALIEN = "Alien"

class LocationType(PyEnum):
    PLANET ="Planet"
    STATION = "Space Station"
    UNKNOWN = "Unknown"

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    specie = db.Column(db.Enum(Specie), nullable=False)
    dimension = db.Column(db.String(20), nullable=False)
    episode = db.relationship("CharacterApperences", backref="character")

    def serialize(self):
        return{ 
            "id": self.id,
            "name": self.name,
            "gender": self.value,
            "specie": self.value,
            "dimension": self.dimension,
            "episode": self.episode,
        }
    
    def __repr__ (self):
        return f"<Character{self.name}>"

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    number = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    characters = db.relationship("CharacterApperences", backref="episode")
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"))    

    def serialize(self):
        return{ 
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "number": self.number,
            "release_date": self.release_date,
            "characters": self.characters,
            "season_id": self.season_id
        }
    
    def __repr__ (self):
        return f"<Episode{self.name}>"

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    dimension = db.Column(db.String(40), nullable=False)
    location_type = db.Column(db.Enum(LocationType), nullable=False, default=LocationType.UNKNOWN)

    def serialize(self):
        return{ 
            "id": self.id,
            "name": self.name,
            "dimension": self.dimension,
            "location_type": self.location_type
        }
    
    def __repr__ (self):
        return f"<Location{self.name}>"

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    episode = db.relationship("Episode", backref="season")

    def serialize(self):
        return{ 
            "id": self.id,
            "number": self.number,
            "release_date": self.release_date,
            "end_date": self.end_date,
            "episodes": self.episode
        }
    
    def __repr__ (self):
        return f"<Seasion{self.number}>"

class CharacterApperences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey("episode.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))


    def serialize(self):
        return{ 
            "id": self.id,
            "episodes": self.episode_id,
            "characters": self.character_id
        }
    
    def __repr__(self):
        return f'<CharacterApperences character: {self.character_id} episode: {self.episode_id}>'
    