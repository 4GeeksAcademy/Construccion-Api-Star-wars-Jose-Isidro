
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean , ForeignKey
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fecha_de_subscripcion: Mapped[int] = mapped_column(nullable=False)
    favorite: Mapped[List["Favorite"]] = relationship(back_populates="user")

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
    favorite_person: Mapped[List["People_favorite"]
                            ] = relationship(back_populates="person")

    def serialize(self):
        return {
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
    favorite_planet: Mapped[List["Planet_favorite"]
                             ] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "terrain": self.terrain,
            "population": self.population
        }


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorite")


class People_favorite(Favorite):
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    person: Mapped["People"] = relationship(back_populates="favorite_person")

    def serialize(self):
        return {
            "user_id": self.user_id,
            "person_id": self.person_id
        }


class Planet_favorite(Favorite):
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped["Planet"] = relationship(back_populates="favorite_planet")

    def serialize(self):
        return{
            "user_id": self.user_id,
            "planeta_id": self.planeta_id
        }
