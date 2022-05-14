from flask import request
from flask_restx import Namespace, Resource
from marshmallow import ValidationError
from models import db, Director, DirectorSchema

# Declare namespace object
directors_ns = Namespace('directors', description='Views for directors')

# Define marshmallow schemas
director_schema = DirectorSchema()


# Define routes and class-based view functions for Directors
@directors_ns.route('')
class DirectorsView(Resource):

    def post(self):
        # Get data from request and create object
        try:
            data = request.json
            director = Director(**director_schema.load(data))

        # Throw bad request wrong fields passed
        except ValidationError as e:
            return f"{e}", 400

        # Add data to the database
        else:
            with db.session.begin():
                db.session.add(director)
            return "Data added", 201


@directors_ns.route('<int:uid>')
class DirectorView(Resource):

    def get(self, uid):
        # Find required row
        director = Director.query.get(uid)
        db.session.close()

        # Throw not found if uid not found
        if not director:
            return f"Director with the id: {uid} not found", 404
        # Display found object
        else:
            return director_schema.dump(director), 200

    def put(self, uid):
        # Get data from request and load object
        try:
            data = director_schema.load(request.json)
            director = Director.query.get(uid)
            # Throw not found if uid not found
            if not director:
                return f"Genre with the id: {uid} not found", 404

        # Throw bad request if wrong fields were passed
        except ValidationError as e:
            return f"{e}", 400

        # Update object
        else:
            director.name = data['name']
            db.session.commit()
            db.session.close()
            return f"Director with id: {uid} successfully updated", 201

    def delete(self, uid):
        # Find required row
        director = Director.query.get(uid)
        # Throw not found if uid not found
        if not director:
            return f"Director with the id: {uid} not found", 404
        # Write deletion
        else:
            db.session.delete(director)
            db.session.commit()
            db.session.close()
            return f"Director with id: {uid} successfully deleted", 201
