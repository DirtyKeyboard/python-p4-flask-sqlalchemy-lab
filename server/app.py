#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    if not animal:
        return make_response('<h1>404! Animal not found :(</h1>', 404)

    keeper = Zookeeper.query.filter(Zookeeper.id == animal.zookeeper_id).first()
    closure = Enclosure.query.filter(Enclosure.id == animal.enclosure_id).first()
    body = f"""
        <ul>ID: {animal.id}</ul>
        <ul>Name: {animal.name}</ul>
        <ul>Species: {animal.species}</ul>
        <ul>Zookeeper: {keeper.name}</ul>
        <ul>Enclosure: {closure.environment}</ul>
        """
    return make_response(body, 200)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    keeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    if not keeper:
        return make_response("<h1>404!! Zookeeper not found</h1>", 404)
    
    body = f"""<ul>ID: {keeper.id}</ul>
                <ul>Name: {keeper.name}</ul>
                <ul>Birthday: {keeper.birthday}</ul>
    """
    for el in keeper.animals:
        body = f"{body}<ul>Animal: {el.name}</ul>"

    return make_response(body, 200)
    
@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    closure = Enclosure.query.filter(Enclosure.id == id).first()
    if not closure:
        return make_response("<h1>404!! Enclosure not found</h1>", 404)

    body = f"""
    <ul>ID: {closure.id}</ul>
    <ul>Environment: {closure.environment}</ul>
    <ul>Open to Visitors: {closure.open_to_visitors}</ul>
    """
    for el in closure.animals:
        body = f"{body}<ul>Animal:{el.name}</ul>"

    return make_response(body, 200)
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)

"""
Your application should contain three views: animal_by_id, zookeeper_by_id, and enclosure_by_id. Their routes should be animal/<int:id>, zookeeper/<int:id>, and enclosure/<int:id>, respectively.
Each view should display all attributes as line items (ul). If there is a one-to-many relationship, each of the many should have its own line item.
"""