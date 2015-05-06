from server import app, db, session
from flask import jsonify
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String)

    constellations = db.relationship('Constellation', backref='user', lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.hash_password(password);
        self.email = email

    def __repr__(self):
        return "<user: {}>".format(self.id)

    def __str__(self):
        return "User: {}".format(self.username)

    def to_JSON(self):
        return jsonify(id=self.id, username=self.username, email=self.email)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Constellation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String)

    vectors = db.relationship('Vector', backref='constellation', lazy='dynamic')

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return "<constellation: {}>".format(self.id)

    def __str__(self):
        return "Constellation: {}".format(self.name)

    def to_obj(self):
        return {"id":self.id, "name":self.name}

stars = db.Table('stars',
    db.Column('vector_id', db.Integer, db.ForeignKey('vector.id')),
    db.Column('star_id', db.Integer, db.ForeignKey('star.id'))
)

class Vector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    constellation_id = db.Column(db.Integer, db.ForeignKey('constellation.id'))

    stars = db.relationship('Star', secondary=stars, backref=db.backref('vectors', lazy='dynamic'))

    a = db.Column(db.Integer, db.ForeignKey('star.id'))
    b = db.Column(db.Integer, db.ForeignKey('star.id'))

    def __init__(self, constellation_id, a, b):
            self.constellation_id = constellation_id
            self.a = a
            self.b = b

    def __repr__(self):
        return "<vector: {}>".format(self.id)

    def __str__(self):
        return "Vector: {} to {} from constellation {}".format(self.a, self.b, self.constellation_id)

    def to_array(self):
        return [self.a, self.b]

class Star(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ra = db.Column(db.Float)
    dec = db.Column(db.Float)
    mag = db.Column(db.Float)

    def __init__(self, id, ra, dec, mag):
        self.id = id
        self.name = "star {}".format(self.id)
        self.ra = ra
        self.dec = dec
        self.mag = mag

    def __repr__(self):
        return "<star: {}>".format(self.id)

    def __str__(self):
        return "Star: {}".format(self.name)
