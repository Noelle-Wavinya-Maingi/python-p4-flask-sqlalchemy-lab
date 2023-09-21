from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Zookeeper(db.Model):
    __tablename__ = 'zookeepers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birthday = db.Column(db.String)


class Enclosure(db.Model):
    __tablename__ = 'enclosures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    environment = db.Column(db.String)
    open_to_visitors = db.Column(db.Boolean)


class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)
    zookeeper_id = db.Column(db.Integer, ForeignKey('zookeepers.id'))
    enclosure_id = db.Column(db.Integer, ForeignKey('enclosures.id'))

    zookeeper = db.relationship('Zookeeper', backref='animals')
    enclosure = db.relationship('Enclosure', backref='animals')

