#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Bakery(db.Model):
    __tablename__ = 'bakeries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

class BakedGood(db.Model):
    __tablename__ = 'baked_goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

db.create_all()

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    response = make_response(jsonify(bakeries_serialized), 200)
    return response

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    bakery = Bakery.query.get(id)

    if bakery is None:
        return jsonify({'message': 'Bakery not found'}), 404

    new_name = request.form.get('name')
    if new_name is not None:
        bakery.name = new_name

    db.session.commit()
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')

    new_baked_good = BakedGood(name=name, price=price)
    db.session.add(new_baked_good)
    db.session.commit()

    return jsonify(new_baked_good.to_dict()), 201

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if baked_good is None:
        return jsonify({'message': 'Baked good not found'}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({'message': 'Baked good deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)

