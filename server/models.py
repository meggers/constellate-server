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
        return self.username

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

class Star(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ra = db.Column(db.Float)
    dec = db.Column(db.Float)
    mag = db.Column(db.Float)

    def __init__(self, id, ra, dec, mag):
        self.id = id
        self.ra = ra
        self.dec = dec
        self.mag = mag
