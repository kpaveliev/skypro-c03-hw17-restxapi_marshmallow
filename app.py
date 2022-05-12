from flask import Flask, request
from flask_restx import Api, Resource
from marshmallow.exceptions import ValidationError
from models import db, Movie, Director, Genre, MovieSchema, DirectorSchema, GenreSchema

# Initiate app, load config, connect database
app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


# Define namespaces
api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

# Define marshmallow schemas
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
genre_schema = GenreSchema()


# Define routes and class-based view functions for Movies
@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        # Get arguments from request
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        # Respond with the movies with the specified director_id and genre_id if found
        if director_id and genre_id:
            movies_found = Movie.query.filter(Movie.director_id == int(director_id),
                                              Movie.genre_id == int(genre_id)).all()
            if not movies_found:
                return f"No movies found with the director_id: {director_id}" \
                       f" and the genre_id: {genre_id}", 204
            else:
                return movies_schema.dump(movies_found), 200

        # Respond with the movies with the specified director_id if found
        if director_id:
            movies_found = Movie.query.filter(Movie.director_id == int(director_id)).all()
            if not movies_found:
                return f"No movies found with the director_id: {director_id}", 204
            else:
                return movies_schema.dump(movies_found), 200

        # Respond with the movies with the specified genre_id if found
        if genre_id:
            movies_found = Movie.query.filter(Movie.genre_id == int(genre_id)).all()
            if not movies_found:
                return f"No movies found with the genre_id: {genre_id}", 204
            else:
                return movies_schema.dump(movies_found), 200

        # Respond with all the movies if no arguments passed
        else:
            movies_all = Movie.query.all()
            return movies_schema.dump(movies_all), 200


@movies_ns.route('/<int:uid>')
class MovieView(Resource):

    def get(self, uid):
        movie_uid = Movie.query.get(uid)
        return movie_schema.dump(movie_uid), 200


# Define routes and class-based view functions for Directors
@directors_ns.route('/')
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


@directors_ns.route('/<int:uid>')
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


# Define routes and class-based view functions for Genres
@genres_ns.route('/')
class GenresView(Resource):

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


@genres_ns.route('/<int:uid>')
class GenreView(Resource):

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
            return f"Genre with id: {uid} successfully deleted", 201


if __name__ == '__main__':
    app.run()
