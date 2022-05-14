from flask_restx import Api
from .movies import api as movies
from .directors import api as directors
from .genres import api as genres

api = Api(
    title='Movies API',
    version='1.0',
    description='Show pages for movies'
)

api.add_namespace(movies, path='/movies/')
api.add_namespace(directors, path='/directors/')
api.add_namespace(genres, path='/genres/')
