from flask import Flask
from flask_restx.representations import output_json
from models import db
from apis import api

# Initiate app, load config
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Register db and api
db.init_app(app)
api.init_app(app)
api.representations = {'application/json; charset=utf-8': output_json}

if __name__ == '__main__':
    app.run()
