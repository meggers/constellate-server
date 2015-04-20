import os
import json
from flask import Flask
from flask.ext.restful import Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('server.settings')
db = SQLAlchemy(app)
session = db.session
app.url_map.strict_slashes = False

import server.models
import server.controllers
