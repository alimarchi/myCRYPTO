from flask import Flask

URL_CONVERSION= "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}"

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.secret_key='this is a secret key'

from mycrypto import routes
