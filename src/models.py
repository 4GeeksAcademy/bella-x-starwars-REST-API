from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250)) 
    eye_color = db.Column(db.String(250)) 
    hair_color = db.Column(db.String(250)) 
    height = db.Column(db.String(250)) 
    skin_color = db.Column(db.String(250)) 
    mass = db.Column(db.String(250)) 

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "skin_color": self.skin_color,
            "mass": self.mass,
            # do not serialize the password, its a security breach
        }    

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250)) 
    mass = db.Column(db.String(250)) 
    population = db.Column(db.String(250)) 
    gravity = db.Column(db.String(250)) 
    terrain = db.Column(db.String(250)) 
    rotation_period = db.Column(db.String(250)) 

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "mass": self.mass,
            "population": self.population,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "rotation_period": self.rotation_period,
            # do not serialize the password, its a security breach
        }    

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    catagory = db.Column(db.String(250)) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship('Character')    
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship('Planet')
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle = db.relationship('Vehicle')

    def __repr__(self):
        return '<Favorites %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "catagory": self.catagory,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,

            # do not serialize the password, its a security breach
        }    