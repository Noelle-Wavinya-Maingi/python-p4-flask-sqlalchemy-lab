#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def home():
    return "<h1>Zoo app</h1>"


@app.route("/animal/<int:id>")
def animal_by_id(id):
    session = db.session
    animal = session.get(Animal, id)
    if animal:
        animal_data = f"""
        <ul>ID: {animal.id}</ul>
        <ul>Name: {animal.name}</ul>
        <ul>Species: {animal.species}</ul>
        <ul>Zookeeper: {animal.zookeeper.name}</ul>
        <ul>Enclosure: {animal.enclosure.name}</ul>
        """

        response = make_response(animal_data, 200)
        return response

    else:
        return "Animal not found", 404


@app.route("/zookeeper/<int:id>")
def zookeeper_by_id(id):
    session = db.session
    zookeeper = session.get(Zookeeper, id)  

    if zookeeper:
        response_body = f"""
        <ul>ID: {zookeeper.id}</ul>
        <ul>Name: {zookeeper.name}</ul>
        <ul>Birthday: {zookeeper.birthday}</ul>
        """

        animals = Animal.query.filter(Animal.zookeeper_id == id)
        response_body += "<ul>Animals:</ul>"

        for animal in animals:
            response_body += f"""
                <ul>{animal.name}</ul>
            """

        response = make_response(response_body, 200)
        return response

    else:
        return "Zookeeper not found", 404


@app.route("/enclosure/<int:id>")
def enclosure_by_id(id):
    session = db.session
    enclosure = session.get(Enclosure, id)
    if enclosure:
        enclosure_data = f"""
        <ul>ID: {enclosure.id}</ul>
        <ul>Environment: {enclosure.environment}</ul>
        <ul>Open to visitors: {enclosure.open_to_visitors}</ul>
        """

        animals = enclosure.animals
        if not animals:
            enclosure_data += "No animals found in this enclosure"
        else:
            enclosure_data += "<ul>Animals:</ul>"
            for animal in animals:
                enclosure_data += f"""
                <ul> {animal.name} - {animal.species}</ul>
            """

        response = make_response(enclosure_data, 200)

        return response

    else:
        return "Enclosure not found", 404


if __name__ == "__main__":
    app.run(port=5555, debug=True)
