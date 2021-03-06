from functools import wraps

from flask import Flask, request, Response
from flask import redirect, jsonify
from flask import g
from flask_jwt import verify_jwt
from flask.ext.jwt import current_user

from server import app, jwt, session
from server.models import *

# routing for basic page #
@app.route('/')
def basic_pages(**kwargs):
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(response="Invalid Request"), 404

class UserObj(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

@jwt.authentication_handler
def authenticate(username, password):
    user = session.query(User).filter_by(username = username).first()
    if user and user.verify_password(password):
        return UserObj(id=user.id, username=user.username)

@jwt.user_handler
def load_user(payload):
    user = session.query(User).filter_by(id = payload['user_id']).first()
    if user:
        return UserObj(id=user.id, username=user.username)

def protected(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        verify_jwt()
        g.user = session.query(User).get(current_user.id)

        return func(*args, **kwargs)
    return decorated_function

#******* API v1 ********#

# user #
@app.route('/api/v1/user/', methods=['POST'])
def add_user():
    # parse the json
    json = request.get_json()

    # extract data
    username = json.get('username')
    email = json.get('email')
    password = json.get('password')

    # sanity checks
    if not username:
        return jsonify(response="Could not create User, username is required"), 400

    if not email:
        return jsonify(response="Could not create User, email is required"), 400

    if not password:
        return jsonify(response="Could not create User, password is required"), 400

    # create user and commit 
    new_user = User(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()
    
    # make sure db xact occured
    if not new_user.id:
        return jsonify(response="Could not create User"), 404
    
    # Return user_id on success
    return jsonify(user_id=new_user.id), 201

@app.route('/api/v1/user/', methods=['GET'])
@protected
def get_user():
    # grab authenticated user
    user = g.user

    # return user params
    return user.to_JSON(), 200

@app.route('/api/v1/user/', methods=['PUT'])
@protected
def update_user():
    # grab authenticated user
    user = g.user

    # parse the json
    json = request.get_json()

    # update changed fields
    if json.get('username'):
        user.username = json.get('username')

    if json.get('email'):
        user.email = json.get('email')

    if json.get('password'):
        user.email = json.get('password')

    # commit changes
    session.commit()   

    # Return an auth token on success
    token = user.generate_token()
    return jsonify({ 'token': token.decode('ascii') }), 200

@app.route('/api/v1/user/', methods=['DELETE'])
@protected
def delete_user():
    # grab authenticated user
    user = g.user

    # delete user from db
    session.delete(user)

    # commit changes
    session.commit()

    # return
    return jsonify(response="User deleted."), 200

# constellations #
@app.route('/api/v1/constellations/', methods=['POST'])
@protected
def add_constellation():
    # grab authenticated user
    user = g.user

    # parse the json
    json = request.get_json()

    # extract data
    name = json.get('name')
    vectors = json.get('vectors')

    # sanity checks
    if not name:
        return jsonify(response="Could not create Constellation, name is required"), 400

    if not vectors:
        return jsonify(response="Could not create Constellations, one or more vectors are required"), 400

    # create new constellation for authenticated user
    new_constellation = Constellation(user_id=user.id, name=name)
    session.add(new_constellation)
    session.commit()

    # create vectors for constellation
    for vector in vectors:
        new_vector = Vector(constellation_id=new_constellation.id, a=vector[0], b=vector[1])
        session.add(new_vector)
        session.commit()

    # return constellation id
    return jsonify(constellation_id=new_constellation.id), 201

@app.route('/api/v1/constellations/', methods=['GET'])
@protected
def get_constellations():
    # grab authenticated user
    user = g.user

    # look up all the constellations associated with the user
    constellations = session.query(Constellation).filter_by(user_id=user.id).all()

    # sanity check
    if not constellations:
        return jsonify(response="No constellations found for user: {}".format(user.id)), 404

    # compose each constellation
    return_list = []
    for constellation in constellations:
        vectors = session.query(Vector).filter_by(constellation_id=constellation.id).all()
        return_list.append({"info":constellation.to_obj(), "vectors":[vector.to_array() for vector in vectors]})

    # return
    return jsonify(constellations=return_list), 200

@app.route('/api/v1/constellations/<int:constellation_id>', methods=['GET'])
@protected
def get_constellation(constellation_id):
    # grab authenticated user
    user = g.user

    # get the constellation
    constellation = session.query(Constellation).get(constellation_id)

    # sanity check
    if not constellation:
        return jsonify(response="Constellation {} not found for user: ".format(constellation_id, user.id)), 404

    # grab vectors for constellation
    vectors = session.query(Vector).filter_by(constellation_id=constellation_id).all()

    # compose response and return
    return jsonify(info=constellation.to_obj(), vectors=[vector.to_array() for vector in vectors]), 200

@app.route('/api/v1/constellations/<int:constellation_id>', methods=['PUT'])
@protected
def update_constellation(constellation_id):
    # grab authenticated user
    user = g.user

    # get the constellation
    constellation = session.query(Constellation)\
        .filter((Constellation.id==constellation_id) & (Constellation.user_id==user.id))\
        .first()

    if not constellation:
        return jsonify(response="Constellation not found for authenticated user."), 404

    # parse the json
    json = request.get_json()

    # extract constellation data
    name = json.get('name')
    vectors = json.get('vectors')

    # update the constellation information
    if name:
        constellation.name = name
        session.commit()

    # if we got new vectors
    if vectors:
        # delete all vectors associated with the constellation
        session.query(Vector)

        # associate new vectors with constellation
        for vector in vectors:
            new_vector = Vector(constellation_id=constellation.id, a=vector[0], b=vector[1])
            session.add(new_vector)
            session.commit()

    return jsonify(response="Constellation Added"), 200

@app.route('/api/v1/constellations/star/<int:star_id>', methods=['GET'])
@protected
def get_constellations_with_star(star_id):
    # grab authenticated user
    user = g.user

    # grab all constellation ids with given star_id
    constellation_ids = session.query(Vector.constellation_id).filter((Vector.a == star_id) | (Vector.b == star_id)).all()
    if not constellation_ids:
        return jsonify(response="That star is not in any constellations for this user."), 404

    # reformat to something that doesn't suck
    constellation_ids = [constellation_id[0] for constellation_id in constellation_ids]

    # grab constellations from ids
    constellations = session.query(Constellation).filter(Constellation.id.in_(constellation_ids))

    # grab all vectors for each constellation
    constellation_data = []
    for constellation in constellations:
        # grab vectors for constellation
        vectors = session.query(Vector).filter_by(constellation_id=constellation.id).all()

        # compile into response array
        constellation_data.append({
            'info':constellation.to_obj(),
            'vectors':[vector.to_array() for vector in vectors]
        })

    # return compiled constellation data
    return jsonify(constellations=constellation_data), 200

@app.route('/api/v1/constellations/<int:constellation_id>', methods=['DELETE'])
@protected
def delete_constellation(constellation_id):
    # grab authenticated user
    user = g.user

    # get the constellation
    constellation = session.query(Constellation).get(constellation_id)

    # sanity check
    if not constellation:
        return jsonify(response="Constellation {} not found for user: ".format(constellation_id, user.id)), 404

    # delete constellation from db
    session.delete(constellation)

    # commit changes
    session.commit()

    # return
    return jsonify(response="Constellation deleted."), 200

