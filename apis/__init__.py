from flask_restx import Api
from .movies import movies_ns
from .directors import directors_ns
from .genres import genres_ns

api = Api(
    title='Movies API',
    version='1.0',
    description='Show pages for movies'
)

api.add_namespace(movies_ns, path='/movies/')
api.add_namespace(directors_ns, path='/directors/')
api.add_namespace(genres_ns, path='/genres/')
