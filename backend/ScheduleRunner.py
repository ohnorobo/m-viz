import time
from pprint import pprint
import sched
import json
import winsound


fileBaseName = "queen"
json_data = open('C:/Users/James/workspace/echo/m-viz/frontend/templates/jsonfiles/' + fileBaseName + '.json')
data = json.load(json_data)

t0 = time.time()
sch = sched.scheduler(time.time , time.sleep)

for section in data:
	for bar in section["bars"]:
		#sch.enterabs(bar["start_time"] + t0, 1, (lambda x: winsound.Beep(800, 150)), [1])
		for beat in bar["beats"]:
		#	sch.enterabs(beat["start_time"] + t0, 1, (lambda x: winsound.Beep(200, 50)), [1])
			for tatum in beat["tatums"]:
				if (tatum["onBeat"]):
					sch.enterabs(tatum["start_time"] + t0, 1, (lambda x: winsound.Beep(400, 50)), [1])
					pprint(time.time())

		
winsound.PlaySound("C:/Users/James/workspace/echo/mp3s/queen.wav", winsound.SND_ASYNC)
sch.run()

#t0 = time.clock()
