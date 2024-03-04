from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites_people = db.relationship('Favorites_people', back_populates='user')
    favorites_planets = db.relationship('Favorites_planets', back_populates='user')

# backpopilates cascade

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "favorites_planets": [favorite.planet.serialize() for favorite in self.favorites_planets if favorite.planet is not None], 
            "favorites_people": [favorite.people.serialize() for favorite in self.favorites_people if favorite.people is not None]
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    # homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    # homeworld = db.relationship('Planets')
    favorites_people = db.relationship('Favorites_people', back_populates='people')
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "gender": self.gender,
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    # Aquí definimos las columnas para la tabla address.
    # Observa que cada columna también es un atributo de instancia de Python normal.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250))
    gravity = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)  
    favorites_planets = db.relationship('Favorites_planets', back_populates='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "gravity": self.gravity,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "surface_water": self.surface_water
        }
    
class Favorites_planets(db.Model):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='favorites_planets')
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship('Planets', back_populates='favorites_planets')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet": self.planet.serialize()  # Accede a través de la relación planet
        }



class Favorites_people(db.Model):
    __tablename__ = 'favorites_people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='favorites_people')
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship('People', back_populates='favorites_people')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "people": self.people.serialize()
        }
