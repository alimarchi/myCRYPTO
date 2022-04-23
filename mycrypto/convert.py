import requests
from mycrypto import URL_CONVERSION
from config import API_KEY

class APIError(Exception):
    pass 

class CriptoConvert:
    def __init__(self, coin_from, coin_to, quantity):
        self.coin_from = coin_from
        self.coin_to = coin_to
        self.quantity = quantity

        self.rate = 0.0
    
    def get_conversion(self):
        try: 
            self.respuesta = requests.get(URL_CONVERSION.format(
            self.coin_from,
            self.coin_to,
            API_KEY))

            self.rate = (self.respuesta.json()["rate"])
            self.result = self.rate * self.quantity
            return round(self.result, 9)
        except:
            raise APIError()

