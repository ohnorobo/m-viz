#!/usr/bin/python
from pprint import pprint
import sys

#sys.path.append("/Users/slaplante/projects/m-viz/")

import echonest.remix.audio as audio





def analyze(song):

  for section in song.analysis.sections:
    pprint(section)
    for bar in section.children():
      pprint("  " + str(bar))
      for beat in bar.children():
        pprint("    " + str(beat))
        for tantum in beat.children():
          pprint("      " + str(tantum))
          pitch = tantum.mean_pitches()
          timbre = tantum.mean_timbre()
          loudness = tantum.mean_loudness()

          pprint("      " + str((pitch, timbre, loudness)))

def analyze_2(song):
  pprint("analyzing...")
  for section in song.analysis.sections:
    pitch = section.pitches
    timbre = section.timbre
    loudness = section.loudness_max



if __name__ == "__main__":
  #export ECHO_NEST_API_KEY="NSZIGB4XJ7TDKEA6P"

  song_filename = "../data/ketto.mp3"
  song = audio.LocalAudioFile(song_filename)

  pprint(song)

  analyze(song)
