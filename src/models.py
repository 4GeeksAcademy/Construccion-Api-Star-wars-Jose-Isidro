from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fecha_de_subscripcion: Mapped[int] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "fecha_de_subscripcion": self.fecha_de_subscripcion
        }



class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=True)
    height: Mapped[float] = mapped_column(nullable=False)
    eye_color:  Mapped[str] = mapped_column(nullable=True)
    skin_color: Mapped[str] = mapped_column(nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "terrain": self.terrain,
            "population": self.population
        }


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped['User'] = relationship()

class People_favorite(Favorite):
    people_id: Mapped['People'] = relationship()

    def serialize(self):
        return{
             "people_id": self.people_id
        }


class Planet_favorite(Favorite):
    planeta_id: Mapped['Planet'] = relationship()

    def serialize(self):
        return{
             "planeta_id": self.planeta_id
        }
