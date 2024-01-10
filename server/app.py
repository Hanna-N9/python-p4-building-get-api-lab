#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# Get all bakeries
@app.route('/bakeries')
def bakeries():   
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        bakeries.append(bakery_dict)
        
    return make_response(jsonify(bakeries), 200)

# Get a single bakery by id
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id = id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(bakery_dict, 200)

    return response

# Get a list of baked goods and sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_serialized = [baked.to_dict() for baked in baked_goods]
    return make_response(baked_goods_serialized, 200)

# Get a single most expensive baked good, sort the baked goods in descending order and limit the number of results
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    return make_response(baked_goods.to_dict(), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
