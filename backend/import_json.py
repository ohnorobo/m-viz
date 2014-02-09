import json
from chord_analysis import *
from pprint import pprint


fileBaseName = "circle_of_life"
json_data = open('C:/Users/James/workspace/echo/m-viz/frontend/templates/jsonfiles/' + fileBaseName + '.json')

def topThree(v):
	""" SPEED ME UP! Gets the biggest three elements of a vector and their indices"""
	u = sorted(zip(v,range(12)))
	
	return u[-3:]
	



data = json.load(json_data)

binaryMask = []
songPitch = [0]*12
accentedNotes = []


for section in data:
	sectionBinaryMask = []
	
	songPitch = [a+b for a,b in (zip(songPitch, section["pitch"]))]
	
	
	for bar in section["bars"]:
		measureNotes = []
		binaryLoudnessMask = []
		binaryTimbreMask = []
		measureBinaryMask = [] ### Binary Mask for a measure
		
		
		for beat in bar["beats"]:
			beatNotes = []
			beatBinaryMask = [] ### Binary Mask for a beak
			
			for tatum in beat["tatums"]:
				if (tatum["loudness"] > bar["loudness"]):
					l = 1
				else:
					l = 0
				binaryLoudnessMask.append(l)
				
				if (tatum["timbre"][3] > bar["timbre"][3]):
					t = 1
				else: 
					t = 0
				binaryTimbreMask.append(t)
					
				if (tatum["timbre"][7] > bar["timbre"][7]):
					r = 1
				else: 
					r = 0
					
				d = r# max(l, t)
				beatBinaryMask.append(d)
				
				if (d == 1): 
					tatum["onBeat"] = True
					
					chord = getChordType(topThree(tatum["pitch"]))
					if (chord == "Nope!"):
						tatum["chord"] = "None"
					else:
						tatum["chord"] = intToNote(chord[0][1]) + str(chord[1])
					
					measureNotes.append(tatum["pitch"])
					
				else:
					tatum["onBeat"] = False
					tatum["chord"] = "None"
			
			measureBinaryMask.append(beatBinaryMask)
			#measureNotes.append(beatNotes)
			
		sectionBinaryMask.append(measureBinaryMask)	
		b = [0]*12
		
		for a in measureNotes:
			b = map(sum, zip(a, b))
		
		pprint(getChordType(topThree(list(b))))
		
	binaryMask.append(sectionBinaryMask)	
		
pprint(songPitch)
pprint(topThree(songPitch))
pprint(getChordType(topThree(songPitch)))

f2 = open("C:/Users/James/workspace/echo/m-viz/frontend/templates/jsonfiles/newqueen.json", "w+")
data2 = json.dumps(data, indent=4)
f2.write(data2)
f2.close()

f.close()

json_data.close()

pprint(binaryMask)

