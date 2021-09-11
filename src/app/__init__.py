import os
import sqlalchemy
from flask import Flask
from dotenv import load_dotenv
from flask_talisman import Talisman
from whitenoise import WhiteNoise

load_dotenv()

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
_database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{_database}'

app = Flask(__name__)
Talisman(app)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='src/app/static/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SECRET_KEY")
app.app_context().push()

db = sqlalchemy.create_engine(DATABASE_CONNECTION_URI)

from app import routes