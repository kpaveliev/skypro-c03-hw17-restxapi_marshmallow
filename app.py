from flask import Flask, request
from flask_restx import Api, Resource
from models import db, Movie, Director, Genre, MovieSchema

# Initiate app, load config, connect database
app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

# Define namespaces
api = Api(app)
movies_ns = api.namespace('movies')

# Define marshmallow schemas
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# Define routes and class-based view functions
@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        # Get arguments from request
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        # Respond with movies with the specified director_id if found
        if director_id:
            movies_found = Movie.query.filter(Movie.director_id == int(director_id)).all()
            if movies_found:
                return movies_schema.dump(movies_found), 200
            else:
                return "", 204

        # Respond with movies with the specified genre_id if found
        if genre_id:
            movies_found = Movie.query.filter(Movie.genre_id == int(genre_id)).all()
            if movies_found:
                return movies_schema.dump(movies_found), 200
            else:
                return "", 204

        # Respond with all the movies if no arguments passed
        else:
            movies_all = Movie.query.all()
            return movies_schema.dump(movies_all), 200


@movies_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        movie_uid = Movie.query.get(uid)
        return movie_schema.dump(movie_uid), 200


if __name__ == '__main__':
    app.run()
