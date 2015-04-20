from server import app, db, session
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String)

    def __init__(self, username, password, email):
        self.username = username
        self.hash_password(password);
        self.email = email

    def __repr__(self):
        return "<user: {}>".format(self.id)

    def __str__(self):
        return "User: {}".format(self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token

        user = User.query.get(data['id'])
        return user

class Constellation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<constellation: {}>".format(self.id)

    def __str__(self):
        return "Constellation: {}".format(self.name)

class Vector(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    constellation = db.relationship('Constellation', backref='vector', lazy='dynamic')
    star = db.relationship('Star', backref='vector', lazy='dynamic')

    constellation_id = db.Column(db.Integer, db.ForeignKey('constellation.id'))
    a = db.Column(db.Integer, db.ForeignKey('star.id'))
    b = db.Column(db.Integer, db.ForeignKey('star.id'))

    def __init__(self, constellation_id, a, b):
            self.constellation_id = constellation_id
            self.a = a
            self.b = b

    def __repr__(self):
        return "<vector: {}>".format(self.id)

    def __str__(self):
        return "Vector: {} to {} from constellation {}".format(self.a, self.b, self.constellation)

class Star(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ra = db.Column(db.Float)
    dec = db.Column(db.Float)
    mag = db.Column(db.Float)

    def __init__(self, id, name, ra, dec, mag):
        self.id = id
        self.name = name
        self.ra = ra
        self.dec = dec
        self.mag = mag

    def __repr__(self):
        return "<star: {}>".format(self.id)

    def __str__(self):
        return "Star: {}".format(self.name)
