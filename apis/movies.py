from flask import request
from flask_restx import Namespace, Resource, fields
from models import db, Movie, Director, Genre, MovieSchema

# Declare namespace object
api = Namespace('movies', description='Views for movies')

# Define marshmallow schemas
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

# Define api model for documentation
movie_model = api.model('Movie', {
    'id': fields.Integer(required=True, description="Movie identifier"),
    'title': fields.String(required=True, description="Movie title"),
    'description': fields.String(required=True, description="Short description"),
    'trailer': fields.String(required=True, description="Link to a trailer"),
    'year': fields.Integer(required=True, description="Release year"),
    'rating': fields.Float(required=True, description="Short description"),
    'genre_id': fields.String(required=True, description="Genre identifier"),
    'director_id': fields.String(required=True, description="Director identifier"),
    'genre': fields.String(required=False, description="Genre name"),
    'director': fields.String(required=False, description="Director name"),
})


# Define routes and class-based view functions for Movies
@api.route('')
@api.param('director_id', 'Director identifier')
@api.param('genre_id', 'Genre identifier')
class MoviesView(Resource):
    @api.doc(description='Get movies for the specified director and genre (params not required)')
    @api.response(200, 'Success', movie_model)
    @api.response(404, 'Not found')
    def get(self):
        # Get arguments from request
        director_id = request.args.get('director_id', type=int)
        genre_id = request.args.get('genre_id', type=int)

        # Respond with the movies with the specified director_id and genre_id if found
        if director_id and genre_id:
            movies_found = db.session\
                .query(Movie.id,
                       Movie.title,
                       Movie.description,
                       Movie.trailer,
                       Movie.rating,
                       Genre.name.label('genre'),
                       Director.name.label('director'))\
                .join(Movie.genre)\
                .join(Movie.director)\
                .filter(Movie.genre_id == genre_id, Movie.director_id == director_id)\
                .all()
            if not movies_found:
                return f"No movies found with the director_id: {director_id}" \
                       f" and the genre_id: {genre_id}", 404
            else:
                return movies_schema.dump(movies_found), 200

        # Respond with the movies with the specified director_id if found
        if director_id:
            movies_found = db.session \
                .query(Movie.id,
                       Movie.title,
                       Movie.description,
                       Movie.trailer,
                       Movie.rating,
                       Genre.name.label('genre'),
                       Director.name.label('director')) \
                .join(Movie.genre) \
                .join(Movie.director) \
                .filter(Movie.director_id == director_id) \
                .all()
            if not movies_found:
                return f"No movies found with the director_id: {director_id}", 404
            else:
                return movies_schema.dump(movies_found), 200

        # Respond with the movies with the specified genre_id if found
        if genre_id:
            movies_found = db.session\
                .query(Movie.id,
                       Movie.title,
                       Movie.description,
                       Movie.trailer,
                       Movie.rating,
                       Genre.name.label('genre'),
                       Director.name.label('director'))\
                .join(Movie.genre)\
                .join(Movie.director)\
                .filter(Movie.genre_id == genre_id)\
                .all()
            if not movies_found:
                return f"No movies found with the genre_id: {genre_id}", 404
            else:
                return movies_schema.dump(movies_found), 200

        # Respond with all the movies if no arguments passed
        else:
            movies_all = db.session\
                .query(Movie.id,
                       Movie.title,
                       Movie.description,
                       Movie.trailer,
                       Movie.rating,
                       Genre.name.label('genre'),
                       Director.name.label('director'))\
                .join(Movie.genre)\
                .join(Movie.director)\
                .all()
            return movies_schema.dump(movies_all), 200


@api.route('<int:uid>')
@api.param('uid', 'Movie identifier')
class MovieView(Resource):
    @api.doc(description='Get movie by id')
    @api.response(200, 'Success', movie_model)
    @api.response(404, 'Not found')
    def get(self, uid):
        movie_found = Movie.query.get(uid)

        if not movie_found:
            return f"Movie with the id: {uid} not found", 404

        return movie_schema.dump(movie_found), 200
