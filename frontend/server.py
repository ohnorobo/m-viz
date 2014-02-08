#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, flask, os
from glob import glob
from pprint import pprint
import numpy
import pygal
import json
from unidecode import unidecode

app = flask.Flask(__name__)


def normalize(array):
  mx = max(array)
  mn = min(array)

  array = map(lambda x: x/mx, array)
  array = map(remove_lows, array)
  return array

def remove_lows(element):
  if element > .2:
    return element
  else:
    return None


colors = colors=['#539a2f', #0
                 '#942d8b', #7
                 '#aca135', #2
                 '#2d3894', #9
                 '#ac7135', #4
                 '#2d946c', #11
                 '#a13143', #6
                 '#9aa633', #1
                 '#592d94', #8
                 '#ac8935', #3
                 '#2d6994', #10
                 '#ac4d35', #5
                 '#56c2d6', #not used
                 '#808384', #not used
                 '#8c54fe', #not used
                 '#465457'] #not used

RainbowStyle = pygal.style.Style(opacity_hover='.4', opacity='.8', colors=colors)

note_labels = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']





@app.route("/json/<filename>")
def get_json(filename):
  #filenames = glob("jsonfiles/*.json")
  return flask.render_template("jsonfiles/" + filename)

@app.route("/viz/notes/<name>")
def get_viz(name):
  return flask.render_template("notes.html", songjson=name+".json")

@app.route("/viz/pygal/<name>/<start>/<end>")
def pygal_graph(name, start, end):
  json_data = open("./templates/jsonfiles/" + name + ".json")
  data = json.load(json_data)
  notes = numpy.matrix(numpy.zeros(12)).T
  times = []

  for section in data:
    for bar in section['bars']:
      for beat in bar['beats']:
        for tatum in beat['tantums']:
          pitch = tatum['pitch']
          pitch = normalize(pitch)
          pitch = numpy.matrix(pitch).T
          notes = numpy.hstack((notes, pitch))

          time = tatum['start_time']
          times.append(time)

  notes = notes[:,1:]
  pprint(notes)

  START = int(start)
  FINISH = int(end)

  chart = pygal.XY(stroke=False, style=RainbowStyle)
  for i, note_data in enumerate(notes[:,START:FINISH]):
    chart.add(note_labels[i], zip(times[START:FINISH], note_data.A1))

  rendered = chart.render()
  encoded = unidecode(rendered)
  markup = flask.Markup(encoded)
  return flask.render_template("graph.html", graph=markup)





if __name__ == "__main__":
  app.debug = True
  host="127.0.0.1"
  port=3002    #run on 80 by default

  app.run(host=host, port=int(port))
