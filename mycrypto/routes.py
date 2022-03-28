from mycrypto import app

@app.route("/")
def start():
    return "I'm working"
