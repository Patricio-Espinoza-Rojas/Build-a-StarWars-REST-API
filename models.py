import email
from enum import unique
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


favorite_character = db.Table('favorite_character',
    db.Column('char_id',db.Integer,db.ForeignKey('characters.id'),primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey('user.id'),primary_key=True)
)

favorite_planet = db.Table('favorite_planet',
    db.Column('planet_id',db.Integer,db.ForeignKey('planets.id'),primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey('user.id'),primary_key=True)
)

favorite_vehicle = db.Table('favorite_vehicle',
    db.Column('planet_id',db.Integer,db.ForeignKey('vehicles.id'),primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey('user.id'),primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    favorite_character = db.relationship('Characters',secondary=favorite_character)
    favorite_planet = db.relationship('Planets',secondary=favorite_planet)
    favorite_vehicle = db.relationship('Vehicles',secondary=favorite_vehicle)

    def serialize(self):
        return{
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

    def serialize_with_favorites(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites": self.get_favorites()

        }
    
    def get_favorites(self):
        array = []
        characters = list(map(lambda characters: characters.serialize(),self.favorite_character))
        planets = list(map(lambda planets: planets.serialize(),self.favorite_planet))
        vehicles = list(map(lambda vehicles: vehicles.serialize(),self.favorite_vehicle))
        for character in characters: array.append(character)
        for planet in planets: array.append(planet)
        for vehicle in vehicles: array.append(vehicle)
        return array
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()





class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gravity = db.Column(db.String(255))
    terrain = db.Column(db.String(255))
    population = db.Column(db.Integer)
    users =  db.relationship('User',secondary=favorite_planet)

    def serialize(self):
        return{
            "id" :  self.id,
            "name" : self.name,
            "gravity" : self.gravity,
            "terrain" : self.terrain,
            "population" : self.population
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    height = db.Column(db.String(255))
    mass = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    # Foreign Key of Vehicles Table , ONE TO MANY
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    char_vehicles = db.relationship('Vehicles', backref='characters')
    users =  db.relationship('User',secondary=favorite_character)
    
    def serialize(self):
        return{
            "id" : self.id,
            "name" : self.name,
            "height" : self.height,
            "mass" : self.mass,
            "gender" : self.gender,
            "vehicle_id" : self.vehicle_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    model = db.Column(db.String(255))
    cost = db.Column(db.Integer)
    max_speed = db.Column(db.Integer)
    pilots = db.Column(db.Integer)
    users =  db.relationship('User',secondary=favorite_vehicle)

    def serialize(self):
        return{
            "id" : self.id,
            "name" : self.name,
            "model" : self.model,
            "cost" : self.cost,
            "max_speed" : self.max_speed,
            "pilots" : self.pilots
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()