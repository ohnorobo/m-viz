#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, flask, os, math
from glob import glob
from pprint import pprint
import pygal
import json
from unidecode import unidecode

app = flask.Flask(__name__)


def normalize(array):
  mx = max(array)
  mn = min(array)

  array = map(norm, array)
  array = map(remove_lows, array)
  return array

def norm(x):
  x += 1
  if x == 0:
    return 0
  else:
    return math.log(x, 2)

def remove_lows(element):
  if element > 0.4:
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
  json_data = open("./templates/jsonfiles/" + name + ".json")
  data = json.load(json_data)

  #change format of data
  new_data = [{"key":"c", "values":[]},
              {"key":"c#", "values":[]},
              {"key":"d", "values":[]},
              {"key":"d#", "values":[]},
              {"key":"e", "values":[]},
              {"key":"f", "values":[]},
              {"key":"f#", "values":[]},
              {"key":"g", "values":[]},
              {"key":"g#", "values":[]},
              {"key":"a", "values":[]},
              {"key":"a#", "values":[]},
              {"key":"b", "values":[]}]

  for section in data:
    for bar in section['bars']:
      for beat in bar['beats']:
        for tatum in beat['tatums']:
          pitches = tatum['pitch']
          pitches = normalize(pitches)
          time = tatum['start_time']

          for dat, pitch in zip(new_data, pitches):
            dat['values'].append({"size":1, "x":time, "y":pitch})

  encoded = unidecode(json.dumps(new_data))
  markup = flask.Markup(encoded)
  return flask.render_template("notes.html", songjson=markup)

@app.route("/viz/pygal/<name>/<start>/<end>")
def pygal_graph(name, start, end):
  json_data = open("./templates/jsonfiles/" + name + ".json")
  data = json.load(json_data)
  notes = [[],[],[],[],[],[],[],[],[],[],[],[]] # notes c to b
  times = []

  for section in data:
    for bar in section['bars']:
      for beat in bar['beats']:
        for tatum in beat['tatums']:
          pitches = tatum['pitch']
          pitches = normalize(pitches)

          for all_note, pitch in zip(notes, pitches):
            all_note.append(pitch)

          time = tatum['start_time']
          times.append(time)

  #pprint(notes)

  START = int(start)
  FINISH = int(end)

  chart = pygal.XY(stroke=False, style=RainbowStyle)
  for i, note_data in enumerate(notes):
    chart.add(note_labels[i], zip(times[START:FINISH], note_data[START:FINISH]))

  rendered = chart.render()
  encoded = unidecode(rendered)
  markup = flask.Markup(encoded)
  return flask.render_template("graph.html", graph=markup)





if __name__ == "__main__":
  app.debug = True
  host="127.0.0.1"
  port=3002    #run on 80 by default

  if sys.argv[1]: #run on port given from heroku
    host = sys.argv[1]
  if sys.argv[2]: #run on host given from heroku
    port = sys.argv[2]

  app.run(host=host, port=int(port))
