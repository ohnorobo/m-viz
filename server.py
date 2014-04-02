#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, math, random
import flask
from glob import glob
from pprint import pprint
import pygal
import json
from unidecode import unidecode

app = flask.Flask(__name__)


def normalize(array):
  mx = max(array)
  mn = min(array)

  array = map(jitter, array)
  array = map(lambda x: norm(x, mx), array)
  array = map(remove_lows, array)
  return array


def jitter(x):
  x += random.gauss(0, 0.005)
  return x

def norm(x, mx):
  return x/(mx + 0.2)
  #x += 1
  #return math.log(x, 2)

def remove_lows(element):
  if element > 0.2:
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

  for section in data[:5]:
    for bar in section['bars']:
      for beat in bar['beats']:
        for tatum in beat['tatums']:
          if 'onBeat' in tatum:
            onBeat = tatum['onBeat']
          else:
            onBeat = True

          pitches = tatum['pitch']
          pitches = normalize(pitches)
          time = tatum['start_time']
          loudness = 10 ** ( -0.01 * tatum['loudness'])

          if onBeat:
            for dat, pitch in zip(new_data, pitches):
              dat['values'].append({"size":loudness, "x":time, "y":pitch})
          else:
            for dat, pitch in zip(new_data, pitches):
              dat['values'].append({"size":loudness * 0.5, "x":time, "y":pitch})

  encoded = unidecode(json.dumps(new_data))
  markup = flask.Markup(encoded)
  return flask.render_template("notes.html", songjson=markup, name=name)

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

@app.route("/viz/beats/<name>/<start>/<end>")
def pygal_beats(name, start, end):
  json_data = open("./templates/jsonfiles/" + name + ".json")
  data = json.load(json_data)
  labels = ["on", "off"]
  notes = [[],[]] # notes on / off beat
  times = []

  for section in data:
    for bar in section['bars']:
      for beat in bar['beats']:
        for tatum in beat['tatums']:
          pitches = tatum['pitch']
          pitches = normalize(pitches)

          loudness = 10 ** ( -0.01 * tatum['loudness'])

          if tatum['onBeat']:
            notes[0].append(loudness)
            notes[1].append(None)
          else:
            notes[1].append(loudness)
            notes[0].append(None)

          time = tatum['start_time']
          times.append(time)

  #pprint(notes)

  START = int(start)
  FINISH = int(end)

  chart = pygal.XY(stroke=False, style=RainbowStyle)
  for i, note_data in enumerate(notes):
    chart.add(labels[i], zip(times[START:FINISH], note_data[START:FINISH]))

  rendered = chart.render()
  encoded = unidecode(rendered)
  markup = flask.Markup(encoded)
  return flask.render_template("graph.html", graph=markup)



@app.route("/viz/chord/<name>")
def chord_clusters(name):
  json_data = open("./templates/jsonfiles/" + name + ".json")
  data = json.load(json_data)
  new_data = []

  for section in data:
    for bar in section['bars']:
      for beat in bar['beats']:
        for tatum in beat['tatums']:
          pitches = tatum['pitch']
          #pitches = normalize(pitches)
          loudness = tatum['loudness']

          if 'chord' in tatum and tatum['chord'] != "None":
            chord = tatum['chord']
            for category, pitch in zip(note_labels, pitches):
              new_data.append({'cluster': chord, 'radius':loudness * pitch, 'pitch': category})

  encoded = unidecode(json.dumps(new_data, indent=4))
  markup = flask.Markup(encoded)
  return flask.render_template("chord.html", datajson=markup)





if __name__ == "__main__":
  app.debug = True
  host="127.0.0.1"
  port=3002    #run on 80 by default

  if sys.argv[1]: #run on port given from heroku
    host = sys.argv[1]
  if sys.argv[2]: #run on host given from heroku
    port = sys.argv[2]

  app.run(host=host, port=int(port))
