from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

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
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    diameter: Mapped[str] = mapped_column(String(100), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(100), nullable=False)
    gravity: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    orbital_period: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped[str] = mapped_column(String(100), nullable=False)
    surface_water: Mapped[str] = mapped_column(String(100), nullable=False)
    terrain: Mapped[str] = mapped_column(String(100), nullable=False)

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
            "terrain": self.terrain
        }
    
    class People(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True)
        gender: Mapped[str] = mapped_column(String(120), nullable=False)
        eye_color: Mapped[str] = mapped_column(String(120), nullable=False)
        name: Mapped[str] = mapped_column(String(120), nullable=False)
        skin_color: Mapped[str] = mapped_column(String(120), nullable=False)
        mass: Mapped[str] = mapped_column(String(120), nullable=False)
        height: Mapped[str] = mapped_column(String(120), nullable=False)
        hair_color: Mapped[str] = mapped_column(String(120), nullable=False)
        birth_year: Mapped[str] = mapped_column(String(120), nullable=False)

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
                "birth_year": self.birth_year
            }
        
        





 
