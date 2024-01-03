from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Universe(db.Model):
    __tablename__ = 'universes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universe_title = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(50))
    works = db.relationship('Work', back_populates='universe', lazy='dynamic', cascade='all, delete-orphan')
    characters = db.relationship('Character', back_populates='universe', lazy='dynamic', cascade='all, delete-orphan')
    terminology = db.relationship('Terminology', back_populates='universe', lazy='dynamic',
                                  cascade='all, delete-orphan')
    relationships = db.relationship('Relationship', back_populates='universe', lazy='dynamic',
                                    cascade='all, delete-orphan')


class Work(db.Model):
    __tablename__ = 'works'

    work_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universes.id'))
    work_title = db.Column(db.String(50), unique=True)
    link = db.Column(db.String(255))
    universe = db.relationship('Universe')


class Character(db.Model):
    __tablename__ = 'characters'

    char_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universes.id'))
    char_name = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(15), nullable=True)
    biography = db.Column(db.Text, nullable=True)
    universe = db.relationship('Universe', back_populates='characters')


class Terminology(db.Model):
    __tablename__ = 'terminology'

    term_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universes.id'))
    term_name = db.Column(db.String(50), unique=True)
    definition = db.Column(db.Text)
    universe = db.relationship('Universe', back_populates='terminology')


class Relationship(db.Model):
    __tablename__ = 'relationships'

    rel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    universe_id = db.Column(db.Integer, db.ForeignKey('universes.id'))
    character1_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    character2_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    relationship_type = db.Column(db.String(50))
    universe = db.relationship('Universe', foreign_keys=[universe_id])
    character1 = db.relationship('Character', foreign_keys=[character1_id])
    character2 = db.relationship('Character', foreign_keys=[character2_id])


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.user_id)
