from datetime import timedelta

DEBUG = True

SECRET_KEY = 'temporary_secret_key'
JWT_AUTH_URL_RULE = '/api/authenticate'
JWT_EXPIRATION_DELTA = timedelta(hours=24)
SQLALCHEMY_DATABASE_URI = 'sqlite:///server.db'
STAR_FILE = 'server/data/hygdata_v3.csv'

ID_INDEX = 0
RA_INDEX = 7
DEC_INDEX = 8
MAG_INDEX = 13
