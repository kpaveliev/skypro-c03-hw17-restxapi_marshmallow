from flask import request
from flask_restx import Namespace, Resource
from models import db, Movie, Director, Genre, MovieSchema

# Declare namespace object
movies_ns = Namespace('movies', description='Views for movies')

# Define marshmallow schemas
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

# Define routes and class-based view functions for Movies
@movies_ns.route('')
class MoviesView(Resource):

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
                       f" and the genre_id: {genre_id}", 204
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
                return f"No movies found with the director_id: {director_id}", 204
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
                return f"No movies found with the genre_id: {genre_id}", 204
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


@movies_ns.route('<int:uid>')
class MovieView(Resource):

    def get(self, uid):
        movie_uid = Movie.query.get(uid)
        return movie_schema.dump(movie_uid), 200
