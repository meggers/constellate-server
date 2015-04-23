import os
import json
from flask import Flask
from flask.ext.restful import Api, Resource
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('server.settings')
db = SQLAlchemy(app)
session = db.session
auth = HTTPBasicAuth()
app.url_map.strict_slashes = False

import server.models
import server.controllers

if __name__ == "__main__":
    application.run(host='0.0.0.0')
