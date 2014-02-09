#!/usr/bin/python
from pprint import pprint
import sys
import json

#sys.path.append("/Users/slaplante/projects/m-viz/")

import echonest.remix.audio as audio





def analyze_to_json(song_audio):
  song = []

  for section in song_audio.analysis.sections:
    section_dict = {}
    section_dict['bars'] = []

    section_dict['pitch'] = section.mean_pitches()
    section_dict['timbre'] = section.mean_timbre()
    section_dict['loudness'] = section.mean_loudness()
    section_dict['start_time'] = section.start
    section_dict['end_time'] = section.end

    for bar in section.children():
      bar_dict = {}
      bar_dict['beats'] = []

      bar_dict['pitch'] = bar.mean_pitches()
      bar_dict['timbre'] = bar.mean_timbre()
      bar_dict['loudness'] = bar.mean_loudness()
      bar_dict['start_time'] = bar.start
      bar_dict['end_time'] = bar.end

      for beat in bar.children():
        beat_dict = {}
        beat_dict['tatums'] = []

        beat_dict['pitch'] = beat.mean_pitches()
        beat_dict['timbre'] = beat.mean_timbre()
        beat_dict['loudness'] = beat.mean_loudness()
        beat_dict['start_time'] = beat.start
        beat_dict['end_time'] = beat.end

        for tatum in beat.children():
          tatum_dict = {}

          tatum_dict['pitch'] = tatum.mean_pitches()
          tatum_dict['timbre'] = tatum.mean_timbre()
          tatum_dict['loudness'] = tatum.mean_loudness()
          tatum_dict['start_time'] = tatum.start
          tatum_dict['end_time'] = tatum.end

          beat_dict['tatums'].append(tatum_dict)
        bar_dict['beats'].append(beat_dict)
      section_dict['bars'].append(bar_dict)
    song.append(section_dict)

  return json.dumps(song, indent=4)








if __name__ == "__main__":
  inputfile = sys.argv[1]
  outputfile = sys.argv[2]

  #export ECHO_NEST_API_KEY="NSZIGB4XJ7TDKEA6P"

  song_filename = inputfile
  song = audio.LocalAudioFile(song_filename)

  j = analyze_to_json(song)
  f = open(outputfile, 'w')
  f.write(j)
