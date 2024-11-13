from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Character Model
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    homeworld = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    favorites = db.relationship("Favorites", back_populates="person")

    def __repr__(self):
        return f"<People {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld": self.homeworld,
            "birth_year": self.birth_year,
            "hair_color": self.hair_color,
        }


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(550), nullable=False, unique=True)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites = db.relationship("Favorites", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }


# Planet Model
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    terrain = db.Column(db.String(250), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    favorites = db.relationship("Favorites", back_populates="planet")

    def __repr__(self):
        return f"<Planets {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
        }


# Favorites Model
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    person = db.relationship("People", back_populates="favorites")
    user = db.relationship("User", back_populates="favorites")
    planet = db.relationship("Planets", back_populates="favorites")

    def __repr__(self):
        return f"<Favorites id={self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "user_id": self.user_id,
            "planets_id": self.planets_id,
        }
