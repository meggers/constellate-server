from server import app, db, session
from flask import Flask, request, Response

# routing for basic page #
@app.route('/')
def basic_pages(**kwargs):
    return redirect('/static/index.html')


#******* API v1 ********#

# api authentication #
@app.route('/api/v1/login', methods=['GET'])
def login():
    return {'':''}, 200

@app.route('/api/v1/logout', methods=['GET'])
def logout():
    return {'':''}, 200

# user #
@app.route('/api/v1/user/', methods=['POST'])
def add_user():
    return {'':''}, 200

@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return {'':''}, 200

@app.route('/api/v1/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return {'':''}, 200

@app.route('/api/v1/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
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

