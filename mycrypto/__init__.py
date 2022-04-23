from flask import Flask
from config import SECRET_KEY

URL_CONVERSION= "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}"

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.secret_key= SECRET_KEY

from mycrypto import routes
