from flask import request
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError
from models import db, Genre, GenreSchema

# Declare namespace object
api = Namespace('genres', description='Views for genres')

# Define marshmallow schemas
genre_schema = GenreSchema()

# Define api model for documentation
genres_model = api.model('Genre', {
    'id': fields.Integer(required=True, description="Identifier"),
    'name': fields.String(required=True, description="Genre name")
})


# Define routes and class-based view functions for Genres
@api.route('')
class GenresView(Resource):
    @api.doc(description='Add new genre', body=genres_model)
    @api.response(201, 'Created')
    @api.response(400, 'ValidationError')
    def post(self):
        # Get data from request and create object
        try:
            data = request.json
            genre = Genre(**genre_schema.load(data))

        # Throw bad request wrong fields passed
        except ValidationError as e:
            return f"{e}", 400

        # Add data to the database
        else:
            with db.session.begin():
                db.session.add(genre)
            return "Data added", 201


@api.route('<int:uid>')
class GenreView(Resource):
    @api.doc(description='Get genre by id')
    @api.response(200, 'Success', genres_model)
    @api.response(404, 'Not found')
    def get(self, uid):
        # Find required row
        genre = Genre.query.get(uid)
        db.session.close()

        # Throw not found if uid not found
        if not genre:
            return f"Genre with the id: {uid} not found", 404
        # Display found object
        else:
            return genre_schema.dump(genre), 200

    @api.doc(description='Update genre by id', body=genres_model)
    @api.response(200, 'Success')
    @api.response(400, 'Validation error')
    @api.response(404, 'Not found')
    def put(self, uid):
        # Get data from request and load object
        try:
            data = genre_schema.load(request.json)
            genre = Genre.query.get(uid)
            # Throw not found if uid not found
            if not genre:
                return f"Genre with the id: {uid} not found", 404

        # Throw bad request if wrong fields were passed
        except ValidationError as e:
            return f"{e}", 400

        # Update object
        else:
            genre.name = data['name']
            db.session.commit()
            db.session.close()
            return f"Genre with id: {uid} successfully updated", 201

    @api.doc(description='Remove genre by id')
    @api.response(204, 'No content')
    @api.response(404, 'Not found')
    def delete(self, uid):
        # Find required row
        genre = Genre.query.get(uid)
        # Throw not found if uid not found
        if not genre:
            return f"Genre with the id: {uid} not found", 404
        # Write deletion
        else:
            db.session.delete(genre)
            db.session.commit()
            db.session.close()
            return f"", 204
