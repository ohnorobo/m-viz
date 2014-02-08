#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, flask, os
from glob import glob

app = flask.Flask(__name__)



@app.route("json/<filename>")
def get_json(filename):
  filenames = glob("jsonfiles/*.json")

  return flask.render_template("jsonfiles/" + filename + ".json")




@app.route("viz/<name>")
def get_viz(name):
  pass



if __name__ == "__main__":
  app.debug = True
  host="127.0.0.1"
  port=80    #run on 80 by default

  app.run(host=host, port=int(port))
