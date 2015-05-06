import os
import json
from flask import Flask
from flask_jwt import JWT
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')

app.config.from_object('server.settings')
db = SQLAlchemy(app)
session = db.session
jwt = JWT(app)
app.url_map.strict_slashes = False

import server.models
import server.controllers

if __name__ == "__main__":
    app.run()
