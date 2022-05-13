# App configuration
DEBUG = True
RESTX_JSON = {'ensure_ascii': False, 'indent': 2}
# Database settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/movies.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False