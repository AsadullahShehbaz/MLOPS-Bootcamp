from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome, Asadullah AI!</p>"

@app.route("/index")
def index():
    return "<p>Welcome to index page!</p>"

app.run(debug=True)