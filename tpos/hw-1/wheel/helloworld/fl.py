#! /usr/bin/env python3

import flask 
from helloworld.main import get_message 

app = flask.Flask(__name__)

@app.route("/")
def hello():
    return flask.render_template("index.html", message=get_message())
    

def run_server():
    app.run()