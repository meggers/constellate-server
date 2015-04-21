from flask import Flask, request, Response
from flask import redirect, jsonify
from flask import g

from server import app, auth, db, session
from server.models import *

# routing for basic page #
@app.route('/')
def basic_pages(**kwargs):
    return redirect('/static/index.html')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(response="Invalid Request"), 404

# authentication wrapper #
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False

    g.user = user
    return True


#******* API v1 ********#

# api authentication #
@app.route('/api/v1/login', methods=['GET'])
@auth.login_required
def login():
    token = g.user.generate_token()
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/api/v1/logout', methods=['GET'])
def logout():
    return {'':''}, 200

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
    
    # Return an auth token on success
    token = new_user.generate_token()
    return jsonify({ 'token': token.decode('ascii') }), 201

@app.route('/api/v1/user/', methods=['GET'])
def get_user():
    return {'':''}, 200

@app.route('/api/v1/user/', methods=['PUT'])
def update_user():
    return {'':''}, 200

@app.route('/api/v1/user/', methods=['DELETE'])
def delete_user():
    return {'':''}, 200

# constellations #
@app.route('/api/v1/constellations/', methods=['POST'])
def add_constellation(constellation_id):
    return {'':''}, 200

@app.route('/api/v1/constellations/', methods=['GET'])
def get_constellations():
    return {'':''}, 200

@app.route('/api/v1/constellations/<int:constellation_id>', methods=['GET'])
def get_constellation(constellation_id):
    return {'':''}, 200

@app.route('/api/v1/constellations/<int:constellation_id>', methods=['PUT'])
def update_constellation(constellation_id):
    return {'':''}, 200

@app.route('/api/v1/constellations/star/<int:star_id>', methods=['GET'])
def get_constellations_with_star(star_id):
    return {'':''}, 200

@app.route('/api/v1/constellations/<int:constellation_id>', methods=['DELETE'])
def delete_constellation(constellation_id):
    return {'':''}, 200

