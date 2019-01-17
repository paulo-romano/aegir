from decouple import config

SERVER_ADDRESS = config('SERVER_ADDRESS')
SERVER_PORT = config('SERVER_PORT')

DEBUG = config('DEBUG', cast=bool)

POSTGRES_HOST = config('POSTGRES_HOST')
POSTGRES_DATABASE = config('POSTGRES_DATABASE')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
