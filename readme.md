## myCRYPTO
#### myCRYPTO is a web application developed with Python. You can simulate the purchase, sale and exchange of crypto currencies. You can play with values and see if you are able to increase your initial investment.
---

### Please follow these steps in order to currently run the app.

### Start by creating a virtual environment
```
 python -m venv venv
```
### Activate your virtual environment
```
. venv/bin/activate
```
### Installed all the requirements
```
pip install -r requirements.txt
```
### Create a Database
### Rename the file .env_template to .env
```
FLASK_APP=run.py
FLASK_ENV=development
```
### Rename the file config_template.py to config.py
* Insert your secret key
* Insert the path to the database you have created
* Insert your API key. You can get you free API key on https://www.coinapi.io. Choose "Get a free api key". You will have 100 daily requests.

### If you have followed all the previous steps, just type on your terminal
```
flask run
```

