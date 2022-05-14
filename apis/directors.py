from flask import request
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError
from models import db, Director, DirectorSchema

# Declare namespace object
api = Namespace('directors', description='Views for directors')

# Define marshmallow schemas
director_schema = DirectorSchema()

# Define api model for documentation
director_model = api.model('Director', {
    'id': fields.Integer(required=True, description="Identifier"),
    'name': fields.String(required=True, description="Full name")
})


# Define routes and class-based view functions for Directors
@api.route('')
class DirectorsView(Resource):
    @api.doc(description='Add new director', body=director_model)
    @api.response(201, 'Created')
    @api.response(400, 'ValidationError')
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


@api.route('<int:uid>')
class DirectorView(Resource):
    @api.doc(description='Get director by id')
    @api.response(200, 'Success', director_model)
    @api.response(404, 'Not found')
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

    @api.doc(description='Update director by id', body=director_model)
    @api.response(200, 'Success')
    @api.response(400, 'Validation error')
    @api.response(404, 'Not found')
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

    @api.doc(description='Remove director by id')
    @api.response(204, 'No content')
    @api.response(404, 'Not found')
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
            return "", 204
