from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    diameter: Mapped[str] = mapped_column(String(100), nullable=True)
    rotation_period: Mapped[str] = mapped_column(String(100), nullable=True)
    gravity: Mapped[str] = mapped_column(String(100), nullable=True)
    climate: Mapped[str] = mapped_column(String(100), nullable=True)
    orbital_period: Mapped[str] = mapped_column(String(100), nullable=True)
    population: Mapped[str] = mapped_column(String(100), nullable=True)
    surface_water: Mapped[str] = mapped_column(String(100), nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)
    url: Mapped[str] = mapped_column(String(200), nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", backref="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "gravity": self.gravity,
            "climate": self.climate,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
            "url": self.url
        }
    
class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    gender: Mapped[str] = mapped_column(String(120), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(120), nullable=True)
    mass: Mapped[str] = mapped_column(String(120), nullable=True)
    height: Mapped[str] = mapped_column(String(120), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(120), nullable=True)
    url: Mapped[str] = mapped_column(String(200), nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", backref="people", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "name": self.name,
            "skin_color": self.skin_color,
            "mass": self.mass,
            "height": self.height,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year,
            "url": self.url
        }
        
class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)

    people_ref: Mapped["People"] = relationship("People", backref="favorite_refs")
    planet_ref: Mapped["Planets"] = relationship("Planets", backref="favorite_refs")

    __table_args__ = (
        CheckConstraint('(people_id IS NULL) != (planet_id IS NULL)', name='check_favorite_type'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "type": "people" if self.people_id else "planet"
        }


 
