#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Hero, HeroPower, Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''
#  route for all HEROES
@app.route('/heroes', methods = ['GET' ,'POST'])
def heroes():
    # GET for HERO by ID
    if request.method == 'GET':
        heroes = Hero.query.all()
        heroes_dict = [hero.to_dict() for hero in heroes]
        return make_response(jsonify(heroes_dict), 200)
    # POST for HERO by ID
    elif request.method == 'POST':
        body = request.get_json()
        new_hero = Hero()
        for key, value in body.items():
            setattr(new_hero, key, value)
        db.session.add(new_hero)   
        db.session.commit() 
        return make_response(jsonify(new_hero.to_dict()), 201)

#  route for HERO by ID
@app.route('/heroes/<int:id>', methods = ['GET', 'DELETE', 'PATCH'])
def hero_by_id(id):
    hero_exists = Hero.query.get(id)
    # validates if hero exists or not
    if not hero_exists:
        return make_response(jsonify({"error": "Hero not found"}), 404)
    # if hero_exists is True:
    if hero_exists:
        # GET for HERO by ID 
        if request.method == 'GET':
            return make_response(jsonify(hero_exists.to_dict()), 200)
        # DELETE for HERO by ID
        elif request.method == 'DELETE':
            db.session.delete(hero_exists)
            db.session.commit()
            return make_response(jsonify({"status": "DELETE successful"}), 200)
        # PATCH for HERO by ID
        elif request.method == 'PATCH':
            body = request.get_json()
            for key, value in body.items():
                setattr(hero_exists, key, value)
            db.session.add(hero_exists)
            db.session.commit()
            return make_response(jsonify(hero_exists.to_dict()), 200)    
    
# route for all POWERS
@app.route('/powers', methods = ['GET', 'POST'])
def powers():
    # GET for all POWERS
    if request.method == 'GET':
        powers = Power.query.all()
        powers_dict = [power.to_dict() for power in powers]
        return make_response(jsonify(powers_dict), 200)
    # POST for all POWERS
    elif request.method == 'POST':
        body = request.get_json()
        new_power = Power()
        for key, value in body.items():
            setattr(new_power, key, value)
        db.session.add(new_power)
        db.session.commit()
        return make_response(jsonify(new_power.to_dict()), 201)    

# route for POWER by ID
@app.route('/powers/<int:id>', methods = ['GET', 'DELETE', 'PATCH'])
def power_by_id(id):
    power_exists = Power.query.get(id)
    # validate if power exists or not
    if not power_exists:
        return make_response(jsonify({ "error": "Power not found"}), 404)
    # if power_exists is True:
    if power_exists:
        # GET for POWER by ID
        if request.method == 'GET':
            return make_response(jsonify(power_exists.to_dict()), 200)
        # DELETE for POWERS by ID
        elif request.method == 'DELETE':
            db.session.delete(power_exists)
            db.session.commit()
            return make_response(jsonify({"status": "DELETE successful"}), 200)
        # PATCH for POWER by ID
        if request.method == 'PATCH':
            body = request.get_json()
            for key, value in body.items():
                setattr(power_exists, key, value)   
            db.session.add(power_exists)
            db.session.commit()
            return make_response(jsonify(power_exists.to_dict()), 200)

# route for all HeroPower
@app.route('/hero_powers', methods = ['GET', 'POST'])
def hero_powers():
    # GET for all HeroPower (the lazy sort way)
    if request.method == 'GET':
        return make_response(jsonify([hp.to_dict() for hp in HeroPower.query.all()]), 200)
    # POST for HeroPower
    if request.method == 'POST':
        body = request.get_json()
        new_hero_power = HeroPower()
        for key, value in body.items():
            setattr(new_hero_power, key, value)
        #  validates hero, power and strength all exist, if not, returns correct error (also the lazy way)
        hero_exists = Hero.query.get(new_hero_power.hero_id) 
        power_exists = Power.query.get(new_hero_power.power_id) 
        strengths = ['Strong', 'Average', 'Weak'] 
        if not hero_exists:
            return {"error": "hero does not exist"}, 422 
        elif not power_exists:
            return {"error": "power does not exist"}, 422
        elif new_hero_power.strength not in strengths:
            return {"error": "invalid strength"}, 422
        # and if all both exist, creates it
        elif hero_exists and power_exists and new_hero_power.strength in strengths:
            db.session.add(new_hero_power)
            db.session.commit()
            return make_response(jsonify(hero_exists.to_dict()), 201)    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
