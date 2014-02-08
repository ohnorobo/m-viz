#!/usr/bin/python

import json
from pprint import pprint
import numpy
import pygal


def normalize(array):
  mx = max(array)
  mn = min(array)

  array = map(lambda x: x/mx, array)
  array = map(remove_lows, array)
  return array

def remove_lows(element):
  if element > .1:
    return element
  else:
    return None



note_labels = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']

json_data = open('out.json')
data = json.load(json_data)
notes = numpy.matrix(numpy.zeros(12)).T


for section in data:
  for bar in section['bars']:
    for beat in bar['beats']:
      pitch = beat['pitch']
      pitch = normalize(pitch)
      pitch = numpy.matrix(pitch).T
      notes = numpy.hstack((notes, pitch))

notes = notes[:,1:]
pprint(notes)

line_chart = pygal.Line(stroke=False)
for i, note_data in enumerate(notes[:,:100]):
  line_chart.add(note_labels[i], note_data.A1)

line_chart.render_to_file('line_chart.svg')


