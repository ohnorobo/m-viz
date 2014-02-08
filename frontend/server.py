#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, flask, os
from glob import glob

app = flask.Flask(__name__)

@app.route("/json/<filename>")
def get_json(filename):
  #filenames = glob("jsonfiles/*.json")
  return flask.render_template("jsonfiles/" + filename)

@app.route("/viz/notes/<name>")
def get_viz(name):
  return flask.render_template("notes.html", songjson=name+".json")


if __name__ == "__main__":
  app.debug = True
  host="127.0.0.1"
  port=3002    #run on 80 by default

  app.run(host=host, port=int(port))
